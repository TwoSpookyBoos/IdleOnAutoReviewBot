from models.models import Advice, AdviceGroup, AdviceSection
from consts import lavaFunc, max_card_stars, maxFarmingCrops, max_land_rank_level, max_IndexOfSigils, stampsDict
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)

def get_drop_rate_account_advice_group() -> AdviceGroup:
    drop_rate_shiny_base = 1
    sigils_trove_base = 10

    cards = session_data.account.cards
    bnn_cardset = []
    events_cardset = []
    for card in cards:
        if card.cardset == 'Bosses n Nightmares':
            bnn_cardset.append(card)
        if card.cardset == 'Events':
            events_cardset.append(card)

    cards = 'Cards'
    misc = 'Miscellaneous'
    multi = 'Multipliers'
    drop_rate_advice = {
        cards: [],
        misc: [],
        multi: []
    }

    drop_rate_cards = [
        {
            'Name': 'Emperor',
            'Stars': (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Emperor')),
            'Base': 12,
            "Max": 12 * (1 + max_card_stars),
            'Bonus': 'Total Drop Rate',
            'Picture': 'emperor-card'
        },
        {
            'Name': 'W6 Minichief Spirit',
            'Stars': (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Minichief Spirit')),
            'Base': 8,
            'Bonus': 'Total Drop Rate',
            'Picture': 'minichief-spirit-card'
        },
        {
            'Name': 'King Doot',
            'Stars': (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'King Doot')),
            'Base': 6,
            'Bonus': 'Total Drop Rate',
            'Picture': 'king-doot-card'
        },
        {
            'Name': 'W5 Mister Brightside',
            'Stars': (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Mister Brightside')),
            'Base': 6,
            'Bonus': 'Total Drop Rate',
            'Picture': 'mister-brightside-card'
        },
        {
            'Name': 'W1 Crystal Carrot',
            'Stars': (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Crystal Carrot')),
            'Base': 5,
            'Bonus': 'Total Drop Rate',
            'Picture': 'crystal-carrot-card'
        },
        {
            'Name': 'W3 Bop Box',
            'Stars': (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Bop Box')),
            'Base': 3.5,
            'Bonus': 'Total Drop Rate',
            'Picture': 'bop-box-card'
        },
        {
            'Name': 'Events Mr Blueberry',
            'Stars': (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Mr Blueberry')),
            'Base': 3,
            'Bonus': 'Total Drop Rate',
            'Picture': 'mr-blueberry-card'
        },
        {
            'Name': 'Events Giftmas Blobulyte',
            'Stars': (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Giftmas Blobulyte')),
            'Base': 3,
            'Bonus': 'Total Drop Rate',
            'Picture': 'giftmas-blobulyte-card'
        },
        {
            'Name': 'W2 Mimic',
            'Stars': (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Mimic')),
            'Base': 3,
            'Bonus': 'Total Drop Rate',
            'Picture': 'mimic-card'
        },
        {
            'Name': 'Domeo Magmus',
            'Stars': (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Domeo Magmus')),
            'Base': 1.5,
            'Bonus': 'PASSIVE Total Drop Rate',
            'Picture': 'domeo-magmus-card'
        }
    ]
    #########################################
    # Account Wide
    #########################################

    # Cards
    #########################################
    # TODO: Add temp line for +ruby level cards
    for card in drop_rate_cards:
        drop_rate_advice[cards].append(Advice(
            label=f"{card['Name']}'card: +{card['Base'] * card['Stars']:g}/{card['Base'] * (1 + max_card_stars):g} {card['Bonus']}",
            picture_class=card['Picture'],
            progression=card['Stars'],
            goal=(1 + max_card_stars)
        ))

    bnn_stars_sum = sum(min(card.star, max_card_stars) + 1 for card in bnn_cardset)
    bnn_star, _ = divmod(bnn_stars_sum, len(bnn_cardset))
    bnn_star = min(bnn_star, max_card_stars)
    bnn_star_next = (bnn_star + 1) * len(bnn_cardset)
    drop_rate_advice[cards].append(Advice(
        label=f"Bosses n Nightmares card set: +{6 * bnn_star}"
              f"/{6 * (1 + max_card_stars)} Drop Rate | Cards until next set level {bnn_stars_sum}/{bnn_star_next}",
        picture_class='bosses-n-nightmares',
        progression=bnn_star,
        goal=6
    ))

    events_stars_sum = sum(min(card.star, max_card_stars) + 1 for card in events_cardset)
    events_star, _ = divmod(events_stars_sum, len(events_cardset))
    events_star = min(events_star, max_card_stars)
    events_star_next = (events_star + 1) * len(events_cardset)
    drop_rate_advice[cards].append(Advice(
        label=f"Events card set: +{7 * events_star}"
              f"/{7 * (1 + max_card_stars)} Drop Rate | Cards until next set level {events_stars_sum}/{events_star_next}",
        picture_class='events',
        progression=events_star,
        goal=6
    ))

    # Misc
    #########################################
    drop_rate_advice[misc].append(Advice(
        label='W6 Big Big Hampter achievement +4% Drop Rate',
        picture_class='big-big-hampter',
        progression=1 if session_data.account.achievements['Big Big Hampter']['Complete'] else 0,
        goal=1
    ))
    drop_rate_advice[misc].append(Advice(
        label='W6 Summoning GM achievement +6% Drop Rate',
        picture_class='summoning-gm',
        progression=int(session_data.account.achievements['Summoning GM']['Complete']),
        goal=1
    ))

    drop_rate_arcade_bonus_id = 27
    _, drop_rate_arcade  = list(session_data.account.arcade.items())[drop_rate_arcade_bonus_id]
    drop_rate_advice[misc].append(Advice(
        label=f"Arcade Bonus {drop_rate_arcade_bonus_id}: {drop_rate_arcade['Display']}",
        picture_class=drop_rate_arcade['Image'],
        progression=drop_rate_arcade['Level'],
        resource=drop_rate_arcade['Material'],
        goal=101
    ))

    # Maybe up the goal to 6930 for +39.6% at 99% or 2730 for a nice round +39%?
    dropin_loads_bubble = session_data.account.alchemy_bubbles['Droppin Loads']
    drop_rate_advice[misc].append(Advice(
        label=f"Alchemy Bubble Droppin Loads +{round(dropin_loads_bubble['BaseValue'], 2):g}% Drop Rate",
        picture_class='droppin-loads',
        progression=dropin_loads_bubble['Level'],
        goal=1330
    ))

    grotto_cavern = session_data.account.caverns['Caverns']['Grotto']
    gloomie_lootie_schematic = session_data.account.caverns['Schematics']['Gloomie Lootie']
    drop_rate_advice[misc].append(Advice(
        label=f"Engineer Schematic Gloomie Lootie +{5 * grotto_cavern['OpalsFound']}% Drop Rate",
        picture_class=gloomie_lootie_schematic['Image'],
        progression=grotto_cavern['OpalsFound'] if gloomie_lootie_schematic['Purchased'] else 0,
        goal='∞'
    ))

    crops_unlocked = session_data.account.farming['CropsUnlocked']
    drop_rate_advice[misc].append(Advice(
        label=f"Crop Depot Highlighter +{(crops_unlocked - 100) if (crops_unlocked > 100) else 0}/{maxFarmingCrops-100}%"
              f" Drop Rate {' (value only increases after 100 crops found)' if (crops_unlocked <= 100) else ''}",
        picture_class='depot-highlighter',
        progression=crops_unlocked,
        goal=maxFarmingCrops
    ))

    # Companions - Crystal Custard
    has_crystal_custard= session_data.account.companions['Crystal Custard']
    drop_rate_advice[misc].append(Advice(
        label=f"Crystal Custard companion +{100 if has_crystal_custard else 0}/100% Drop Rate",
        picture_class='crystal-custard',
        progression=int(has_crystal_custard),
        goal=1
    ))

    # Equinox - Faux Jewels
    # Will show additional info if player is maxed out for their currently available levels
    faux_jewels_bonus = session_data.account.equinox_bonuses['Faux Jewels']
    faux_jewels_level = faux_jewels_bonus['CurrentLevel']
    drop_rate_advice[misc].append(Advice(
        label=f"Equinox Faux Jewels +{5 * faux_jewels_level}% Drop Rate"
              f"{' (increase Faux Jewels max with Endless Summoning)' if faux_jewels_level == faux_jewels_bonus['PlayerMaxLevel'] else ''}",
        picture_class='faux-jewels',
        progression=faux_jewels_level,
        goal='∞' # This is technically Endless, since Endless Summoning increases the max level
    ))

    # Beanstalk - Golden Cake
    cake_beanstalk_name ='FoodG13'
    cake_beanstalk = session_data.account.sneaking['Beanstalk'][cake_beanstalk_name]
    cake_beanstalk_level = int(cake_beanstalk['Beanstacked']) + int(cake_beanstalk['SuperBeanstacked'])
    if cake_beanstalk_level == 2:
        cake_beanstalk_bonus = '+6.67'
    elif cake_beanstalk_level == 1:
        cake_beanstalk_bonus = '+4.59'
    else:
        cake_beanstalk_bonus = '0%'
    drop_rate_advice[misc].append(Advice(
        label=f"Beanstalk Golden Cake {cake_beanstalk_bonus}/6.67% Drop Rate (further increased by Golden Food multi)",
        picture_class='golden-cake',
        progression=cake_beanstalk_level,
        goal=2
    ))

    # Guild Bonus - Gold Charm
    gold_charm_bonus = session_data.account.guild_bonuses['Gold Charm']
    drop_rate_advice[misc].append(Advice(
        label=f"Guild Bonus Gold Charm +{gold_charm_bonus['Value']:g}"
              f"/{gold_charm_bonus['MaxValue']:g}% Drop Rate",
        picture_class=gold_charm_bonus['Picture'],
        progression=gold_charm_bonus['Level'],
        goal=gold_charm_bonus['MaxLevel']
    ))

    # TODO: Add temporary line for + Land Rank Level
    # Land Rank - Seed of Loot
    # Will show additional info if the player does not have the current max number of available land rank levels
    seed_of_loot_land_rank = session_data.account.farming['LandRankDatabase']['Seed of Loot']
    drop_rate_advice[misc].append(Advice(
        label=f"Land Rank Seed of Loot +{seed_of_loot_land_rank['BaseValue'] * seed_of_loot_land_rank['Level']}"
              f"/{seed_of_loot_land_rank['BaseValue'] * max_land_rank_level}% Drop Rate"
              f"{' (increase Land Rank max with Grimoire)' if seed_of_loot_land_rank['Level'] < max_land_rank_level else ''}",
        picture_class='seed-of-loot',
        progression=seed_of_loot_land_rank['Level'],
        goal=max_land_rank_level
    ))

    # Rift - Sneak Mastery 1
    sneak_mastery_level = session_data.account.sneaking['MaxMastery']
    drop_rate_advice[misc].append(Advice(
        label=f"Rift Sneaking Mastery +{30 if (sneak_mastery_level > 0) else 0}/30% Drop Rate",
        picture_class='sneaking-mastery',
        progression=sneak_mastery_level,
        goal=1
    ))

    # Owl Bonuses
    drop_rate_owl_bonuses = session_data.account.owl['Bonuses']['Drop Rate']
    drop_rate_advice[misc].append(Advice(
        label=f"Bonuses of Orion +{drop_rate_owl_bonuses['Value']}% Drop Rate",
        picture_class='drop-rate',
        progression=drop_rate_owl_bonuses['NumUnlocked'],
        goal='∞'
    ))

    # Gem Shop - Deathbringer Pack
    has_db_pack = 'Deathbringer Pack' in session_data.account.gemshop['Bundles']
    drop_rate_advice[misc].append(Advice(
        label=f"Gemshop Deathbringer Pack +{200 if has_db_pack else 0}/200% Drop Rate",
        picture_class='gem',
        progression=int(has_db_pack),
        goal=1
    ))

    # Breeding - Shiny Pets
    drop_rate_shiny_level = 0
    drop_rate_shiny_value = 0
    for name, shiny in session_data.account.breeding['Species'][1].items():
        if shiny['ShinyBonus'] == 'Drop Rate':
            drop_rate_shiny_level += shiny['ShinyLevel']
            drop_rate_shiny_value += drop_rate_shiny_base * shiny['ShinyLevel']
    drop_rate_advice[misc].append(Advice(
        label=f"Total Shiny Critter +{drop_rate_shiny_value}% Drop Rate",
        picture_class='breeding',
        progression=drop_rate_shiny_level,
        goal='∞'
    ))

    # Shrine - Clover Shrine
    drop_rate_advice[misc].append(Advice(
        label=f"Shrine +{session_data.account.shrines['Clover Shrine']['Value']:g}% Drop Rate",
        picture_class='clover-shrine',
        progression=session_data.account.shrines['Clover Shrine']['Level'],
        goal='∞'
    ))

    # Sigil
    trove_sigil_level = session_data.account.alchemy_p2w['Sigils']['Trove']['Level']
    drop_rate_advice[misc].append(Advice(
        label=f"Clover Sigil +{sigils_trove_base * trove_sigil_level}"
              f"/{sigils_trove_base * max_IndexOfSigils}% Drop Rate",
        picture_class='trove',
        progression=trove_sigil_level,
        goal=max_IndexOfSigils
    ))

    # Stamps - Golden Sixes + (Lab + Pristine Charm + Exalted Stamp)
    # We show an extra line for Lab and Pristine Charm if they aren't unlocked already
    golden_sixes_buffs = []
    has_certified_stamp_book = session_data.account.labBonuses['Certified Stamp Book']['Enabled']
    if not has_certified_stamp_book:
        golden_sixes_buffs.append('Lab')
        drop_rate_advice[misc].append(Advice(
            label=f"Certified Stamp Book lab node (x2 the Drop Rate stamp below)",
            picture_class='certified-stamp-book',
            progression=0, # we're only showing if it's missing, so just assume 0
            goal=1
        ))
    has_liqorice_rolle = session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained']
    if not has_liqorice_rolle:
        golden_sixes_buffs.append('Pristine Charm')
        drop_rate_advice[misc].append(Advice(
            label=f"Liqorice Rolle pristine charm (x1.35 the Drop Rate stamp below)",
            picture_class='liqorice-rolle',
            progression=0, # we're only showing if it's missing, so just assume 0
            goal=1
        ))
    golden_sixes_stamp = session_data.account.stamps['Golden Sixes Stamp']
    has_exalted_golden_sixes = golden_sixes_stamp['Exalted']
    if not has_exalted_golden_sixes:
        golden_sixes_buffs.append('Exalted Stamps')
    match len(golden_sixes_buffs):
        case 0:
            golden_sixes_addl_text = f" (can be further increased by the Abomination Slayer XVII compass bonus)"
        case 1:
            golden_sixes_addl_text = f" (can be increased by {golden_sixes_buffs[0]})"
        case 2:
            golden_sixes_addl_text = f" (can be increased by {golden_sixes_buffs[0]} and {golden_sixes_buffs[1]})"
        case 3:
            golden_sixes_addl_text = f" (can be increased by {golden_sixes_buffs[0]}, {golden_sixes_buffs[1]}, and {golden_sixes_buffs[2]})"
    abomination_slayer_17 = session_data.account.compass['Upgrades']['Abomination Slayer XVII']
    exalted_stamp_bonus_value = ((abomination_slayer_17['Level'] * abomination_slayer_17['Value Per Level'])/100)
    exalted_stamp_multi = 2 + exalted_stamp_bonus_value
    # The exalted multiplier is the only multiplier that actually changes the base value on the stamp, we have to add the other 2 manually
    golden_sixes_value = round(golden_sixes_stamp['Value'] * \
            (2 if has_certified_stamp_book else 1) * \
            (1.35 if has_liqorice_rolle else 1) \
        , 2)
    golden_sixes_stamp_data = stampsDict['Combat'][37]
    golden_sixes_base_max = lavaFunc(golden_sixes_stamp_data['funcType'], golden_sixes_stamp['Max'], golden_sixes_stamp_data['x1'], golden_sixes_stamp_data['x2'])
    golden_sixes_value_max = round((golden_sixes_base_max * 2 * 1.35 * exalted_stamp_multi), 2)
    drop_rate_advice[misc].append(Advice(
        label=f"Golden Sixes stamp +{golden_sixes_value:g}/{golden_sixes_value_max}%{golden_sixes_addl_text}",
        picture_class='golden-sixes-stamp',
        progression=golden_sixes_stamp['Level'],
        resource=golden_sixes_stamp['Material'],
        goal=golden_sixes_stamp['Max']
    ))

    # Summoning 
    # drop_rate_advice[multi].append(Advice(
    #     label=f"Cotton Candy pristine charm {'1.15x' if cotton_candy_obtained else '0%'} Drop Rate MULTI",
    #     picture_class='cotton-candy-charm',
    #     progression=int(session_data.account.sneaking['PristineCharms']['Cotton Candy']['Obtained']),
    #     goal=1
    # ))

    # Sneaking Pristine Charm - Cotton Candy
    cotton_candy_obtained = session_data.account.sneaking['PristineCharms']['Cotton Candy']['Obtained']
    drop_rate_advice[multi].append(Advice(
        label=f"Cotton Candy pristine charm {'1.15x' if cotton_candy_obtained else '0%'} Drop Rate MULTI",
        picture_class='cotton-candy-charm',
        progression=int(session_data.account.sneaking['PristineCharms']['Cotton Candy']['Obtained']),
        goal=1
    ))

    # TODO: Account wide bonuses
    # Family Obols
    # Summoning
    # Tome
    # $$ Island Explorer Pack
    # Archlord of the Pirates

    for subgroup in drop_rate_advice:
        for advice in drop_rate_advice[subgroup]:
            mark_advice_completed(advice)

    drop_rate_ag = AdviceGroup(
        tier="",
        pre_string="Info- Account wide sources of Drop Rate",
        advices=drop_rate_advice,
        informational=True,
    )
    return drop_rate_ag

def get_progression_tiers_advice_group() -> tuple[AdviceGroup, int, int, int]:
    template_advice_dict = {
        'Tiers': {},
    }
    info_tiers = 0
    max_tier = 0 - info_tiers
    tier_Active = 0

    #Assess Tiers
    tiers_ag = AdviceGroup(
        tier=tier_Active,
        pre_string="Progression Tiers",
        advices=template_advice_dict['Tiers']
    )
    overall_section_tier = min(max_tier + info_tiers, tier_Active)
    return tiers_ag, overall_section_tier, max_tier, max_tier + info_tiers

def get_drop_rate_advice_section() -> AdviceSection:
    # Generate AdviceGroups
    drop_rate_advice_group_dict = {}
    drop_rate_advice_group_dict['Tiers'], overall_section_tier, max_tier, true_max = get_progression_tiers_advice_group()
    drop_rate_advice_group_dict['Account'] = get_drop_rate_account_advice_group()

    # Generate AdviceSection

    tier_section = f"{overall_section_tier}/{max_tier}"
    drop_rate_advice_section = AdviceSection(
        name="Drop Rate",
        tier=tier_section,
        pinchy_rating=overall_section_tier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Drop Rate Information",
        picture='wiki/Orion_DR.png',
        groups=drop_rate_advice_group_dict.values(),
        unrated=True,
    )
    return drop_rate_advice_section
