import copy

from consts.idleon.lava_func import lava_func
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.advice.generators.w6 import get_summoning_bonus_advice
from models.advice.generators.general import get_upgrade_vault_advice
from models.advice.generators.w2 import get_arcade_advice

from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.all_talentsDict import all_talentsDict
from utils.text_formatting import pl, notateNumber
from utils.logging import get_logger

from consts.consts_autoreview import break_you_best, build_subgroup_label, EmojiType, ValueToMulti
from consts.consts_w5 import max_sailing_artifact_level, sailing_artifacts_count
from consts.consts_w4 import territory_names, shiny_days_list, breedabilityDaysList, max_breeding_territories, max_meal_level, breeding_last_arena_bonus_unlock_wave, breeding_total_pets
from consts.consts_w2 import maxable_critter_vials_list, max_vial_level
from consts.progression_tiers import breeding_progressionTiers, true_max_tiers

logger = get_logger(__name__)

def getShinyExclusions(breeding_dict, progression_tiers_breeding):
    shinyExclusionsDict = {
        "Infinite Star Signs": True,
        "Lower Minimum Travel Time for Sailing": False,
        "Higher Artifact Find Chance": False,
        "Base Critter Per Trap": False,
        "Faster Shiny Pet Lv Up Rate": False
        }

    # If Infinite Star Signs are unlocked and the player has less than the highest number required in the tiers,
    # Set False (as in False, the recommendation should NOT be excluded), otherwise keep the default True
    highest_iss_in_tiers = max([requirements.get('Shinies', {}).get('Infinite Star Signs', [0])[0] for requirements in progression_tiers_breeding.values()])
    if (
        session_data.account.rift['InfiniteStars']
        and sum([shiny_pet[1] for shiny_pet in breeding_dict['Grouped Bonus']['Infinite Star Signs']]) < highest_iss_in_tiers
    ):
        shinyExclusionsDict['Infinite Star Signs'] = False

    # if all artifacts are Eldritch tier, append True (as in True, the recommendation SHOULD be excluded), otherwise False
    if session_data.account.sum_artifact_tiers >= (sailing_artifacts_count * max_sailing_artifact_level):
        shinyExclusionsDict['Lower Minimum Travel Time for Sailing'] = True
        shinyExclusionsDict['Higher Artifact Find Chance'] = True

    if all([session_data.account.alchemy_vials[vial_name]['Level'] >= max_vial_level for vial_name in maxable_critter_vials_list]):
        shinyExclusionsDict['Base Critter Per Trap'] = True

    shinyExclusionsDict['Faster Shiny Pet Lv Up Rate'] = session_data.account.sneaking.emporium["Science Crayon"].obtained

    return shinyExclusionsDict

def getTerritoryName(territory_index: int) -> str:
    try:
        return territory_names[int(territory_index)]
    except:
        return f"UnknownTerritory-{territory_index}"

def getSpiceImage(territory_index: int) -> str:
    try:
        return f"{territory_names[int(territory_index)]}-spice"
    except:
        return f"UnknownSpice-{territory_index}"

def getShinySpeedSourcesAdviceGroup(faster_shiny_pet_total_levels) -> AdviceGroup:
    mga = 'Multi Group A- Summoning Winner Bonus'
    mgb = 'Multi Group B- Lamp Wish'
    mgc = 'Multi Group C- Everything Else'
    sps_adviceDict = {
        mga: [],
        mgb: [],
        mgc: []
    }

#Multi Group A
    sps_adviceDict[mga].append(get_summoning_bonus_advice('<x Shiny EXP'))

#Multi Group B
    lamp_cavern = session_data.account.caverns['Caverns']['The Lamp']
    sps_adviceDict[mgb].append(Advice(
        label=f"{{{{Lamp|#glowshroom-tunnels}}}} Wish: World 4 Stuff: +{lamp_cavern['WishTypes'][4]['BonusList'][1]}%",
        picture_class=f"cavern-{lamp_cavern['CavernNumber']}",
        progression=lamp_cavern['WishTypes'][4]['BonusList'][1],
        goal=EmojiType.INFINITY.value
    ))

#Multi Group C
    sps_adviceDict[mgc].append(
        session_data.account.farming.depot["Crayon"].get_bonus_advice()
    )
    sps_adviceDict[mgc].append(Advice(
        label=f"Lab Jewel: Emerald Ulthurite",
        picture_class='emerald-ulthurite',
        progression=int(session_data.account.labJewels['Emerald Ulthurite']['Enabled']),
        goal=1
    ))
    sps_adviceDict[mgc].append(Advice(
        label=f"Faster Shiny Pet Lv Up Rate Shiny Pets: +{3 * faster_shiny_pet_total_levels}% total",
        picture_class='green-mushroom-shiny'
    ))
    sps_adviceDict[mgc].append(Advice(
        label=f"Breeding Upgrade: Grand Martial of Shinytown: "
              f"+{session_data.account.breeding['Upgrades']['Grand Martial of Shinytown']['Value']}%",
        picture_class='breeding-bonus-11',
        progression=session_data.account.breeding['Upgrades']['Grand Martial of Shinytown']['Level'],
        goal=session_data.account.breeding['Upgrades']['Grand Martial of Shinytown']['MaxLevel'],
    ))

    sps_adviceDict[mgc].append(Advice(
        label=f"Star Sign: Breedabilli: "
              f"+{15 * session_data.account.star_signs.get('Breedabilli', {}).get('Unlocked', False)}/15%",
        picture_class='breedabilli',
        progression=int(session_data.account.star_signs.get('Breedabilli', {}).get('Unlocked', 0)),
        goal=1
    ))
    sps_adviceDict[mgc].append(session_data.account.star_sign_extras['SeraphAdvice'])
    sps_adviceDict[mgc].append(session_data.account.star_sign_extras['SilkrodeNanoAdvice'])

    for group_name in sps_adviceDict:
        for advice in sps_adviceDict[group_name]:
            advice.mark_advice_completed()

    sps_AdviceGroup = AdviceGroup(
        tier='',
        pre_string='Sources of Shiny Pet Level Rate',
        advices=sps_adviceDict,
        informational=True
    )
    return sps_AdviceGroup

def getBreedabilityAdviceGroup():
    b_advices = []
    all_breedability = {}
    for world_index in session_data.account.breeding['Species'].keys():
        for k, v in session_data.account.breeding['Species'][world_index].items():
            all_breedability[k] = v
            all_breedability[k]['World'] = world_index
    # all_breedability = {
    #     k:v
    #     for worldIndex in session_data.account.breeding['Species'].keys()
    #     for k,v in session_data.account.breeding['Species'][worldIndex].items()
    # }
    sorted_breedability = sorted(
        all_breedability.items(),
        key=lambda pet: pet[1]['BreedabilityDays'],
        reverse=True
    )
    total_7s = 0
    achievement_7s = 0
    for pet in sorted_breedability:
        total_7s += 1 if pet[1]['BreedabilityDays'] >= breedabilityDaysList[-4] else 0
        achievement_7s += 1 if pet[1]['BreedabilityDays'] >= breedabilityDaysList[-4] and pet[1]['World'] != 4 else 0
        b_advices.append(Advice(
            label=f"W{pet[1]['World']} {pet[0]}"
                  f"<br>Breedability Multi: {pet[1]['BreedabilityMulti']:.3f}x"
                  f"<br>Heart VII: {notateNumber('Match', pet[1]['BreedabilityDays'], 0, 'K' if pet[1]['BreedabilityDays'] >= 1000 else '')} / "
                  f"{notateNumber('Match', breedabilityDaysList[-4], 0, 'K')}",
            picture_class=pet[0],
            progression=f"{min(1, pet[1]['BreedabilityDays'] / breedabilityDaysList[-4]):.2%}",
            goal='100%',
            resource=pet[1]['BreedabilityHeart']
        ))
    b_advices.insert(0, Advice(
        label=f"Total Heart VII+ pets: {total_7s}/{len(sorted_breedability)}",
        picture_class='breedability-heart-7',
        progression=total_7s,
        goal=len(sorted_breedability),
    ))
    b_advices.insert(1, Advice(
        label=f"I LOVE These Pets achievement: {achievement_7s}/15",
        picture_class='i-love-these-pets',
        progression=int(session_data.account.achievements['I LOVE These Pets']['Complete']),
        goal=1,
    ))

    for advice in b_advices:
        advice.mark_advice_completed()
    
    b_ag = AdviceGroup(
        tier='',
        pre_string="Breedability Multi and Heart VII Progress",
        post_string=(
            f"Note: W4 pets don't count toward the achievement {EmojiType.FROWN.value}"
            if not session_data.account.achievements['I LOVE These Pets']['Complete'] else
            ''
        ),
        advices=b_advices,
        informational=True
    )
    return b_ag

def getActiveBMAdviceGroup() -> AdviceGroup:
    abm_adviceDict = {
        'Prerequisites': [],
        'Equipment': [],
        'Cards': [],
        'Lab Chips': [],
        'Active Fight': []
    }
    # Active BM Prerequisites
    abm_adviceDict['Prerequisites'].append(Advice(
        label='Step 1: Have a Voidwalker in your family',
        picture_class='voidwalker-icon',
        progression=int('Voidwalker' in session_data.account.classes),
        goal=1
    ))
    abm_adviceDict['Prerequisites'].append(Advice(
        label='Step 2: Voidwalker: Enhancement Eclipse talent leveled to 150+',
        picture_class='enhancement-eclipse',
        progression=max([vman.max_talents.get("49", 0) for vman in session_data.account.vmans], default=0),
        goal=150
    ))
    abm_adviceDict['Prerequisites'].append(Advice(
        label="Step 3: Have a Wind Walker in your family for 12-18x Breeding speed"
              "<br>Beast Master will only be about 1/3rd that value: 4-6x",
        picture_class='wind-walker-icon',
        progression=int('Beast Master' in session_data.account.classes),
        goal=1
    ))
    all_prereqs_met = all([
        'Voidwalker' in session_data.account.classes,
        max([vman.max_talents.get("49", 0) for vman in session_data.account.vmans], default=0) >= 150,
        'Beast Master' in session_data.account.classes
    ])
    abm_adviceDict['Prerequisites'].append(Advice(
        label=(
            f"All ACTIVE-ONLY kills with your BM/WW now have a 50% chance to speed up progress for the "
            f"Fenceyard, Spice collection, and Egg production! Crystal Mobs count {EmojiType.HAPPY.value}"
        ),
        picture_class='whale-wallop',
        progression=int(all_prereqs_met),
        goal=1
    ))

    # Equipment
    abm_adviceDict['Equipment'].append(Advice(
        label='Respawn Keychains: +6% respawn per roll (Or +10% from FOMO shop)',
        picture_class='negative-7-chain'
    ))
    abm_adviceDict['Equipment'].append(Advice(
        label='The Divine Scarf: +20% respawn',
        picture_class='the-divine-scarf'
    ))
    abm_adviceDict['Equipment'].append(Advice(
        label='Spine Tingler Sniper: +12% respawn',
        picture_class='spine-tingler-sniper'
    ))
    abm_adviceDict['Equipment'].append(Advice(
        label='Serrated Chest of the Divine: +8% respawn',
        picture_class='serrated-chest-of-the-divine'
    ))
    abm_adviceDict['Equipment'].append(Advice(
        label='Spiked Leggings of the Divine: +4% respawn',
        picture_class='spiked-leggings-of-the-divine'
    ))
    abm_adviceDict['Equipment'].append(Advice(
        label=f'Star Sign: Breedabilli: +15% Shiny Pet Level Speed',
        picture_class='breedabilli'
    ))
    abm_adviceDict['Equipment'].append(Advice(
        label=f'Star Sign: Grim Reaper Major: +4% respawn',
        picture_class='grim-reaper-major'
    ))
    abm_adviceDict['Equipment'].append(Advice(
        label=f'Star Sign: Grim Reaper: +2% respawn',
        picture_class='grim-reaper'
    ))

    # Cards
    cards = ['Demon Genie', 'Poop']
    for card_name in cards:
        abm_adviceDict["Cards"].append(next(c for c in session_data.account.cards if c.name == card_name).getAdvice())

    abm_adviceDict["Cards"].append(Advice(
        label=f"Fill the rest with: Drop Rate, Active EXP, or Damage Cards if needed.",
        picture_class="locked-card"
    ))

    # Lab Chips
    abm_adviceDict['Lab Chips'].append(Advice(
        label='Chocolatey Chip for more Crystal Mobs',
        picture_class="chocolatey-chip",
        progression=session_data.account.labChips.get('Chocolatey Chip', 0),
        goal=1
    ))
    abm_adviceDict['Lab Chips'].append(Advice(
        label='Omega Nanochip: Top Left card doubler',
        picture_class="omega-nanochip",
        progression=session_data.account.labChips.get('Omega Nanochip', 0),
        goal=1
    ))
    abm_adviceDict['Lab Chips'].append(Advice(
        label='Omega Motherboard: Bottom Right card doubler',
        picture_class='omega-motherboard',
        progression=session_data.account.labChips.get('Omega Motherboard', 0),
        goal=1
    ))
    abm_adviceDict['Lab Chips'].append(Advice(
        label='Silkrode Software aka Keychain Doubler ONLY IF your top Keychain gives more than 10% total respawn',
        picture_class='silkrode-software',
        progression=session_data.account.labChips.get('Silkrode Software', 0),
        goal=1
    ))
    abm_adviceDict['Lab Chips'].append(Advice(
        label='Silkrode Processor aka Pendant Doubler ONLY IF your Pendant gives more than 10% total respawn',
        picture_class='silkrode-processor',
        progression=session_data.account.labChips.get('Silkrode Processor', 0),
        goal=1
    ))
    abm_adviceDict['Lab Chips'].append(session_data.account.star_sign_extras['SilkrodeNanoAdvice'])
    abm_adviceDict['Lab Chips'].append(Advice(
        label='Fill any remaining slots with Galvanic Nanochip: +10% respawn per chip',
        picture_class='galvanic-nanochip'
    ))

    # Active play
    abm_adviceDict['Active Fight'].append(Advice(
        label="Place UwU Rawrrr first on your attack talent bar. The order of the other attacks doesn't seem to matter.",
        picture_class='uwu-rawrrr'
    ))
    abm_adviceDict['Active Fight'].append(Advice(
        label='Finally, Auto against Samurai Guardians',
        picture_class='samurai-guardian'
    ))
    abm_adviceDict['Active Fight'].append(Advice(
        label=f"W6 Taskboard Merit: +10% W6 respawn if fighting Samurai Guardians",
        picture_class='merit-5-1',
        progression=session_data.account.merits[5][1]['Level'],
        goal=10
    ))

    abm_adviceDict['Active Fight'].append(Advice(
        label='If not ready for Sammys, Auto against Tremor Wurms instead',
        picture_class='tremor-wurm'
    ))
    abm_adviceDict['Active Fight'].append(Advice(
        label=f'W5 Taskboard Merit: +20% W5 respawn if fighting Tremor Wurms',
        picture_class='merit-4-1',
        progression=session_data.account.merits[4][1]['Level'],
        goal=10
    ))

    for subgroupName in abm_adviceDict:
        for advice in abm_adviceDict[subgroupName]:
            advice.mark_advice_completed()

    abm_AdviceGroup = AdviceGroup(
        tier='',
        pre_string='Active Wind Walker setup earns around 12-18x Breeding progress (BM 4-6)',
        advices=abm_adviceDict,
        informational=True
    )
    return abm_AdviceGroup

def getBreedingProgressionTiersAdviceGroups(breeding_dict):
    spice = 'Unlock more Spice Territories'
    terr_team = 'Recommended Territory Team (Left to Right)'
    arena_team = 'Recommended Arena Team (Left to Right)'
    breeding_Advices = {
        'UnlockedTerritories': {
            spice: [],
            terr_team: []
        },
        'MaxArenaWave': {
            arena_team: []
        },
        'ShinyLevels': {},
        'MaxShinyLevels': {}
    }
    breeding_AdviceGroups = {}

    customized_tiers = copy.deepcopy(breeding_progressionTiers)
    optional_tiers = 4
    true_max = true_max_tiers['Breeding']
    max_tier = true_max - optional_tiers
    tier_UnlockedTerritories = 0
    tier_MaxArenaWave = 0
    tier_ShinyLevels = 0
    tier_MaxShinyLevels = 0
    recommended_territory_comps: dict[int, list[list[str]]] = {
        0: [
            [],
            []],
        1: [
            ['Mercenary or Fighter', 'Next Highest Power'],
            ['mercenary', 'fighter']],
        2: [
            ['Mercenary', 'Cursory', 'Defender or Highest Power'],
            ['mercenary', 'cursory', 'defender']],
        3: [
            ['Rattler or Mercenary', 'Cursory', 'Refiller', 'Defender'],
            ['rattler', 'cursory', 'refiller', 'defender']],
        4: [
            ['Rattler', 'Monolithic', 'Refiller', 'Defender', 'Refiller'],
            ['rattler', 'monolithic', 'refiller', 'defender', 'refiller']],
        5: [
            ['Peapeapod or Rattler', 'Looter', 'Peapeapod or Monolithic', 'Refiller', 'Defender', 'Refiller'],
            ['peapeapod', 'looter', 'peapeapod', 'refiller', 'defender', 'refiller']],
        6: [
            ['Peapeapod or Rattler', 'Peapeapod or Rattler', 'Looter', 'Defender', 'Refiller', 'Refiller'],
            ['peapeapod', 'peapeapod', 'looter', 'defender', 'refiller', 'refiller']]
    }
    recommended_arena_comps: dict[int, list[list[str]]] = {
        # 2-pet comp used to beat Wave 3
        0: [
            ['Mercenary or Fighter', 'Next Highest Power'],
            ['mercenary', 'fighter']],
        # 3-pet comp used to beat Wave 15
        1: [
            ['Mercenary', 'Cursory', 'Defender or Highest Power'],
            ['mercenary', 'cursory', 'defender']],
        # 4-pet comp used to beat Wave 50
        2: [
            ['Rattler', 'Monolithic', 'Refiller', 'Borger or Defender'],
            ['rattler', 'monolithic', 'refiller', 'borger']],
        # 5-pet comp used to beat Wave 125
        3: [
            ['Rattler', 'Looter', 'Badumdum', 'Refiller', 'Borger'],
            ['rattler', 'looter', 'badumdum', 'refiller', 'borger']],
        # 6-pet comp used to beat Wave 200
        4: [
            ['Rattler', 'Defender', 'Looter', 'Refiller', 'Badumdum', 'Borger'],
            ['rattler', 'defender', 'looter', 'refiller', 'badumdum', 'borger']]
    }

    shiny_tiers_displayed = []
    shiny_exclusions = getShinyExclusions(breeding_dict, customized_tiers)

    #Assess Tiers
    for tier_number, requirements in customized_tiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)
        # Unlocked Territories
        if tier_UnlockedTerritories >= (tier_number - 1):
            if breeding_dict['Highest Unlocked Territory Number'] >= requirements.get('TerritoriesUnlocked', 0):
                tier_UnlockedTerritories = tier_number
            else:
                for territory_index in range(breeding_dict['Highest Unlocked Territory Number'] + 1, requirements['TerritoriesUnlocked'] + 1):
                    breeding_Advices['UnlockedTerritories'][spice].append(Advice(
                        label=getTerritoryName(territory_index),
                        picture_class=getSpiceImage(territory_index),
                        completed=False
                    ))
                for pet_index in range(0, len(recommended_territory_comps[tier_number][0])):
                    breeding_Advices['UnlockedTerritories'][terr_team].append(Advice(
                        label=recommended_territory_comps[tier_number][0][pet_index],
                        picture_class=recommended_territory_comps[tier_number][1][pet_index],
                        completed=False
                    ))

        # Arena Waves to unlock Pet Slots
        if tier_MaxArenaWave >= (tier_number - 1):
            if breeding_dict['ArenaMaxWave'] >= requirements.get('ArenaWaves', 0):
                tier_MaxArenaWave = tier_number
            else:
                for pet_index in range(0, len(recommended_arena_comps[tier_MaxArenaWave][0])):
                    breeding_Advices['MaxArenaWave'][arena_team].append(Advice(
                        label=recommended_arena_comps[tier_MaxArenaWave][0][pet_index],
                        picture_class=recommended_arena_comps[tier_MaxArenaWave][1][pet_index],
                        completed=False
                    ))

        # Shinies
        failedShinyRequirements = []
        failedShinyBonus = {}
        if 'Shinies' not in requirements:
            if tier_ShinyLevels >= tier_number - 1:
                # free pass
                tier_ShinyLevels = tier_number
        else:
            # if there are actual level requirements
            all_requirements_met = True
            for shiny_type in requirements['Shinies']:
                if breeding_dict['Total Shiny Levels'][shiny_type] < requirements['Shinies'][shiny_type][0]:
                    if shiny_exclusions.get(shiny_type, False) == False:
                        all_requirements_met = False
                    else:
                        continue
                    failedShinyRequirements.append([
                        shiny_type,
                        breeding_dict['Total Shiny Levels'][shiny_type],
                        requirements['Shinies'][shiny_type][0],
                        requirements['Shinies'][shiny_type][1]],
                    )
                    failedShinyBonus[shiny_type] = breeding_dict['Grouped Bonus'][shiny_type]
            if all_requirements_met == True and tier_ShinyLevels >= tier_number - 1:
                tier_ShinyLevels = tier_number
            else:
                if (
                    tier_number not in shiny_tiers_displayed
                    and len(shiny_tiers_displayed) < session_data.account.max_subgroups
                ):
                    shiny_tiers_displayed.append(tier_number)
                if tier_number in shiny_tiers_displayed:
                    for failedRequirement in failedShinyRequirements:
                        shiny_subgroup_label = f"{subgroup_label} - {failedRequirement[0]}: {failedRequirement[1]}/{failedRequirement[2]}"
                        if failedRequirement[0] not in breeding_Advices['ShinyLevels']:
                            breeding_Advices['ShinyLevels'][shiny_subgroup_label] = []
                        for possibleShinyPet in failedShinyBonus[failedRequirement[0]]:
                            breeding_Advices['ShinyLevels'][shiny_subgroup_label].append(Advice(
                                label=f"{possibleShinyPet[0]}: {possibleShinyPet[2]:,.2f} base days to level",
                                picture_class=possibleShinyPet[0],
                                progression=possibleShinyPet[1],
                                goal=max(failedRequirement[3], possibleShinyPet[1]),
                                completed=False
                            ))

        # Max Shinies
        if 'Max Shinies' not in requirements:
            if tier_MaxShinyLevels >= tier_number - 1:
                # free pass
                tier_MaxShinyLevels = tier_number
        else:
            # if there are actual level requirements
            all_requirements_met = True
            if tier_MaxShinyLevels >= (tier_number - 1):
                for shiny_type in requirements['Max Shinies']:
                    for pet_details in breeding_dict['Grouped Bonus'][shiny_type]:
                        if pet_details[1] < len(shiny_days_list):
                            all_requirements_met = False
                            add_subgroup_if_available_slot(breeding_Advices['MaxShinyLevels'], subgroup_label)
                            if subgroup_label in breeding_Advices['MaxShinyLevels']:
                                breeding_Advices['MaxShinyLevels'][subgroup_label].append(Advice(
                                    label=f"{shiny_type}: {pet_details[0]}",
                                    picture_class=pet_details[0],
                                    progression=pet_details[1],
                                    goal=len(shiny_days_list),
                                ))

            if all_requirements_met == True and tier_MaxShinyLevels >= tier_number - 1:
                tier_MaxShinyLevels = tier_number

    overall_SectionTier = min(true_max, tier_MaxArenaWave, tier_UnlockedTerritories, tier_ShinyLevels, tier_MaxShinyLevels)

    # Generate Advice Groups
    territories = customized_tiers.get(tier_UnlockedTerritories + 1, {}).get('TerritoriesUnlocked', max_breeding_territories)
    breeding_AdviceGroups['UnlockedTerritories'] = AdviceGroup(
        tier=tier_UnlockedTerritories,
        pre_string=f"Unlock {territories - breeding_dict['Highest Unlocked Territory Number']}"
                   f" more Spice Territor{pl(breeding_Advices['UnlockedTerritories'], 'y', 'ies')}",
        advices=breeding_Advices['UnlockedTerritories'],
    )
    nextArenaWaveUnlock = customized_tiers.get(tier_MaxArenaWave + 1, {}).get('ArenaWaves', 200)
    breeding_AdviceGroups['MaxArenaWave'] = AdviceGroup(
        tier=tier_MaxArenaWave,
        pre_string=f"Complete Arena Wave {nextArenaWaveUnlock} to unlock "
                   f"{pl(5 - tier_MaxArenaWave, 'the final Arena bonus', 'another pet slot')}",
        advices=breeding_Advices['MaxArenaWave'],
    )

    if max(session_data.account.all_skills['Breeding']) >= 40:
        breeding_AdviceGroups['ShinyLevels'] = AdviceGroup(
            tier=tier_ShinyLevels,
            pre_string='Level Shinies',
            advices=breeding_Advices['ShinyLevels'],
        )
        if len(breeding_Advices['ShinyLevels']) == 0:
            maxed_shinies = [pet_info[0] for bonus_group in breeding_dict['Grouped Bonus'].values() for pet_info in bonus_group if pet_info[1] == 20 ]
            breeding_AdviceGroups['MaxShinyLevels'] = AdviceGroup(
                tier=tier_MaxShinyLevels,
                pre_string=f'Max level Shinies ({len(maxed_shinies)}/{breeding_total_pets})',
                advices=breeding_Advices['MaxShinyLevels'],
            )
    return breeding_AdviceGroups, overall_SectionTier, max_tier, true_max

def getPetDamageAdviceGroup():
    # Multi Group A
    blooming_axe_breeding_upgrade = session_data.account.breeding['Upgrades']['Blooming Axe']
    blooming_axe_breeding_upgrade_bonus = blooming_axe_breeding_upgrade['Value']
    multi_group_a = ValueToMulti(blooming_axe_breeding_upgrade_bonus)

    # Multi Group B
    electrolyte_vial = session_data.account.alchemy_vials['Electrolyte (Condensed Zap)']
    electrolyte_vial_bonus = electrolyte_vial['Value']

    barley_lost_achievement = session_data.account.achievements['Barley Lost']
    barley_lost_achievement_bonus = int(barley_lost_achievement['Complete']) * 5

    croissant_meal = session_data.account.meals['Croissant']
    croissant_meal_bonus = croissant_meal['Value']

    wedding_cake_meal = session_data.account.meals['Wedding Cake']
    wedding_cake_meal_bonus = wedding_cake_meal['Value']

    arena_spirit_talent = next(talent for talent in all_talentsDict.values() if talent['name'] == 'Arena Spirit')
    highest_arena_spirit_level = 0
    highest_arena_spirit_goal_level = 0
    for char in session_data.account.safe_characters:
        talents = char.current_preset_talents
        try:
            arena_spirit_level = talents[str(arena_spirit_talent['skillIndex'])] + char.total_bonus_talent_levels
            if arena_spirit_level > highest_arena_spirit_level:
                highest_arena_spirit_level = arena_spirit_level
                highest_arena_spirit_goal_level = char.max_talents_over_books
        except:
            continue
    arena_spirit_talent_bonus = lava_func(arena_spirit_talent['funcY'], highest_arena_spirit_level, arena_spirit_talent['y1'], arena_spirit_talent['y2'])

    power_bowower_star_sign = session_data.account.star_signs['Power Bowower']
    power_bowower_star_sign_bonus = int(power_bowower_star_sign['Unlocked']) * 30

    pet_damage_arcade_bonus = next(arcade_bonus for arcade_bonus in session_data.account.arcade.values() if arcade_bonus['Stat'] == 'Breeding Pet DMG')
    pet_damage_arcade_bonus_bonus = pet_damage_arcade_bonus['Value']

    pet_punchies_vault_upgrade = session_data.account.vault['Upgrades']['Pet Punchies']
    pet_punchies_vault_upgrade_bonus = pet_punchies_vault_upgrade['Total Value']

    multi_group_b = ValueToMulti(
        electrolyte_vial_bonus +
        barley_lost_achievement_bonus +
        croissant_meal_bonus +
        wedding_cake_meal_bonus +
        arena_spirit_talent_bonus +
        power_bowower_star_sign_bonus +
        pet_damage_arcade_bonus_bonus +
        pet_punchies_vault_upgrade_bonus
        )

    multi_total = round(multi_group_a * multi_group_b, 2)

    pet_damage_advices = {
        f'Total: {multi_total}x': [
            Advice(
                label=f'Total Pet Damage bonus: {multi_total}x',
                picture_class='vault-upgrade-58'
            )
        ],
        f'Multi Group A: {round(multi_group_a, 2)}x': [
            Advice(
                label=f'Breeding Upgrade - Blooming Axe: +{blooming_axe_breeding_upgrade_bonus}%',
                picture_class='breeding-bonus-5',
                progression=blooming_axe_breeding_upgrade['Level'],
                goal=blooming_axe_breeding_upgrade['MaxLevel']
            )
        ],
        f'Multi Group B: {round(multi_group_b, 2)}x': [
            Advice(
                label=f'{{{{ Vial|#vials }}}} - Electrolyte: +{electrolyte_vial_bonus:.2f}%',
                picture_class='condensed-zap',
                progression=electrolyte_vial['Level'],
                goal=max_vial_level
            ),
            Advice(
                label=f'{{{{ Achievement|#achievements }}}} - Barley Lost: +{barley_lost_achievement_bonus}%',
                picture_class='barley-lost',
                progression=int(barley_lost_achievement['Complete']),
                goal=1
            ),
            Advice(
                label=f'{{{{ Meal|#cooking }}}} - Croissant: +{croissant_meal_bonus:.2f}%',
                picture_class=croissant_meal['Image'],
                progression=croissant_meal['Level'],
                goal=max_meal_level
            ),
            Advice(
                label=f'{{{{ Meal|#cooking }}}} - Wedding Cake: +{wedding_cake_meal_bonus:.2f}%',
                picture_class=wedding_cake_meal['Image'],
                progression=wedding_cake_meal['Level'],
                goal=max_meal_level
            ),
            Advice(
                label=f'Beast Master Talent passive- Arena Spirit: +{arena_spirit_talent_bonus:.2f}%',
                picture_class='arena-spirit',
                progression=highest_arena_spirit_level,
                goal=highest_arena_spirit_goal_level
            ),
            Advice(
                label=f"{{{{ Star Sign|#star-signs }}}} -  Power Bowower: {'+30% if equipped' if power_bowower_star_sign['Unlocked'] else 'Locked.'}",
                picture_class='power-bowower',
                progression=int(power_bowower_star_sign['Unlocked']),
                goal=1
            ),
            get_arcade_advice(30),
            get_upgrade_vault_advice('Pet Punchies')
        ]
    }
    for subgroup in pet_damage_advices:
        for advice in pet_damage_advices[subgroup]:
            advice.mark_advice_completed()

    pet_damage_advice_group = AdviceGroup(
        tier='',
        pre_string='Sources of Pet Damage',
        advices=pet_damage_advices,
        informational=True,
        completed=all([territory['Unlocked'] for territory in session_data.account.breeding['Territories'].values()]) and session_data.account.breeding['ArenaMaxWave'] >= breeding_last_arena_bonus_unlock_wave
    )
    return pet_damage_advice_group

def getBreedingAdviceSection() -> AdviceSection:
    highest_breeding_level = max(session_data.account.all_skills['Breeding'])
    if highest_breeding_level < 1:
        breeding_AdviceSection = AdviceSection(
            name='Breeding',
            tier='0/0',
            header='Come back after unlocking the Breeding skill in World 4!',
            picture='Breeding.png',
            unreached=True
        )
        return breeding_AdviceSection

    breedingDict = session_data.account.breeding
    #Generate AdviceGroups
    breeding_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getBreedingProgressionTiersAdviceGroups(breedingDict)
    breeding_AdviceGroupDict['ShinySpeedSources'] = getShinySpeedSourcesAdviceGroup(breedingDict['Total Shiny Levels']['Faster Shiny Pet Lv Up Rate'])
    breeding_AdviceGroupDict['ActiveBM'] = getActiveBMAdviceGroup()
    breeding_AdviceGroupDict['Breedability'] = getBreedabilityAdviceGroup()
    breeding_AdviceGroupDict['PetDamage'] = getPetDamageAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    breeding_AdviceSection = AdviceSection(
        name='Breeding',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Breeding tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Breeding.png',
        groups=breeding_AdviceGroupDict.values()
    )
    return breeding_AdviceSection
