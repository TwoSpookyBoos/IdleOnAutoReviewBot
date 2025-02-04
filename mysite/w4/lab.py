from models.models import AdviceSection, AdviceGroup, Advice, Character
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
import math
from consts import (
    break_you_best, infinity_string, labJewelsDict, breedingSpeciesDict
    #lab_progressionTiers
)

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int]:
    lab_AdviceDict = {
        'Tiers': [],
    }
    info_tiers = 0
    max_tier = 0  #max(lab_progressionTiers.keys(), default=0) - info_tiers
    tier_Lab = 0

    #Assess Tiers
    lab_AdviceDict['Tiers'].append(Advice(
                label=f"Not much to say for now.",
                picture_class=''
            ))

    tiers_ag = AdviceGroup(
        tier="",
        pre_string="Informational",
        advices=lab_AdviceDict['Tiers'],
        informational=True
    )
    overall_SectionTier = min(max_tier + info_tiers, tier_Lab)
    return tiers_ag, overall_SectionTier, max_tier

def getLabAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    if session_data.account.highestWorldReached < 4:
        lab_AdviceSection = AdviceSection(
           name="Lab",
            tier="0",
            pinchy_rating=0,
            header="Come back after unlocking Lab in W4 town!",
            picture="wiki/Laboratory_Mainframe.gif",
            unrated=True,
            unreached=True
        )
        return lab_AdviceSection

    #Generate Alert Advice
    #TODO debug call :
    calculate_players_line_width(session_data.account.all_characters[0], 1, 1, 1, 1)

    #Generate AdviceGroups
    lab_AdviceGroupDict = {}
    lab_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    lab_AdviceSection = AdviceSection(
        name="Lab",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Lab tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="wiki/Laboratory_Mainframe.gif",
        groups=lab_AdviceGroupDict.values(),
        unrated=True,
        extra=session_data.account.all_characters
    )

    return lab_AdviceSection

def get_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def get_character_linewidth(character : Character, px_meal_bonus, line_pct_meal_bonus, passive_card_bonus, pet_arena_bonus, in_gem_tube, bubo_boost, shiny_bonus, jewels, player_cords):
    base_width = 50 + (2 * character.lab_level)

    if jewels[5].available:
        if get_distance(labJewelsDict[5]['Coordinates'][0], labJewelsDict[5]['Coordinates'][1], character.lab_position[0], character.lab_position[1]) < 150:
            base_width *= 1.25

    player_chip_bonus = sum(slot.chip.getBonus() for slot in character.lab_info.chips if slot.chip and slot.chip.name == "Conductive Motherboard")
    
    # 12% per Conductive Motherboard chip equipped
    player_chip_bonus = sum(12 for chip in character.equipped_lab_chips if chip == 6)
    
    bonus_width = 30 if in_gem_tube else 0
    return math.floor(
        (base_width + (px_meal_bonus + min(passive_card_bonus, 50))) *
        (1 + ((bubo_boost + line_pct_meal_bonus + player_chip_bonus + (20 * pet_arena_bonus) + bonus_width + shiny_bonus) / 100))
    )
    

    
def calculate_players_line_width(character : Character, lab, breeding, gem_store, bubo_boost):
    meal_bonus = 0  # 1.59 Change - 16th Jewel no longer impacts meal jewels

    if True: #if lab.players_in_tubes:
        px_meal_bonus = session_data.account.meals["Pancakes"]["Value"] + session_data.account.meals["Wild Boar"]["Value"]
        line_pct_meal_bonus = session_data.account.meals["Eel"]["Value"]
        
        ########################################################### Stopped converting here
        # TODO Parse per-player equipped cards
        passive_card_bonus = sum( card for card in character.equipped_cards) #sum(card.getBonus() for card in (cards or []) if "Line Width" in card.data.effect)
        pet_arena_bonus = 1 if breeding and breeding.hasBonus(13) else 0
        
        for worldIndex in session_data.account.breeding['Species']:
            for petIndex in breedingSpeciesDict.get(worldIndex, {}):
                species_name = breedingSpeciesDict[worldIndex][petIndex]['Name']
                if species_name in session_data.account.breeding['Species'][worldIndex]:
                    for key, value in session_data.account.breeding['Species'][worldIndex][species_name].items():
                        print(f"World {worldIndex}, Pet {petIndex}, {key}: {value}")
                
        shiny_bonus = next((bonus.getBonus() for bonus in (breeding.shinyBonuses if breeding else []) if bonus.data.index == 19), 0)
        shiny_bonus = session_data.account.breeding['Species'][worldIndex][petValuesDict['Name']]
        gem_tubes = ((next((purchase.pucrhased for purchase in (gem_store.purchases if gem_store else []) if purchase.no == 123), 0)) * 2)

        for index, player in enumerate(lab.players_in_tubes):
            if player.playerID in lab.player_cords and lab.best_bubo_playerID in lab.player_cords:
                player_position = lab.player_cords[player.playerID]
                bubo_position = lab.player_cords[lab.best_bubo_playerID]
                right_of_bubo = player_position.x >= bubo_position.x
                
                player.lab_info.line_width = get_character_linewidth(
                    player, px_meal_bonus, line_pct_meal_bonus, passive_card_bonus,
                    pet_arena_bonus, index < gem_tubes, bubo_boost if right_of_bubo else 0, shiny_bonus,
                    lab.jewels, lab.player_cords
                )
                player.lab_info.supped = index < gem_tubes

def find_prism_source(lab):
    for player in lab.players_in_tubes:
        player_cords = lab.player_cords.get(player.playerID)
        if player_cords:
            if get_distance(43, 229, player_cords.x, player_cords.y) < player.lab_info.line_width:
                return player
    return None


def calculate_player_impact(connected_players, chain_index, lab, extra_px_from_bonuses):
    jewel_multiplier = lab.bonuses[8].getBonus()
    jewel_connection_range_bonus = sum(
        jewel.getBonus(jewel_multiplier) for jewel in lab.jewels if jewel.active and jewel.index == 9
    )
    bonus_connection_range_bonus = lab.bonuses[13].getBonus()
    connection_range_bonus = jewel_connection_range_bonus + bonus_connection_range_bonus

    player = connected_players[chain_index]
    player_cords = lab.player_cords[player.playerID]
    has_impact = False

    # Check players in tubes
    for tube_player in lab.players_in_tubes:
        tube_player_coords = lab.player_cords[tube_player.playerID]
        in_range = get_distance(player_cords.x, player_cords.y, tube_player_coords.x, tube_player_coords.y) < tube_player.lab_info.line_width
        if tube_player not in connected_players and in_range:
            connected_players.append(tube_player)
            has_impact = True

    # Activate inactive bonuses in range
    for bonus in filter(lambda b: not b.active, lab.bonuses):
        in_range = get_distance(player_cords.x, player_cords.y, bonus.x, bonus.y) < bonus.getRange(connection_range_bonus, extra_px_from_bonuses)
        if in_range and bonus.unlocked:
            bonus.active = True
            has_impact = True

    # Activate available but inactive jewels in range
    for jewel in filter(lambda j: j.available and not j.active, lab.jewels):
        in_range = get_distance(player_cords.x, player_cords.y, jewel.data.x, jewel.data.y) < jewel.getRange(connection_range_bonus, extra_px_from_bonuses)
        if in_range:
            jewel.active = True
            has_impact = True

    return has_impact

def update_lab(data):
    lab = data.get("lab")
    player_data = data.get("players")
    cooking = data.get("cooking")
    cards = data.get("cards")
    gem_store = data.get("gems")
    breeding = data.get("breeding")
    deathnote = data.get("deathnote")
    storage = data.get("storage")
    task_board = data.get("taskboard")
    divinity = data.get("divinity")
    equinox = data.get("equinox")
    sneaking = data.get("sneaking")
    summoning = data.get("summoning")

    # Sneaking jade upgrades
    lab.bonuses[14].unlocked = next((upgrade.purchased for upgrade in sneaking.jadeUpgrades if upgrade.index == 8), False)
    lab.bonuses[15].unlocked = next((upgrade.purchased for upgrade in sneaking.jadeUpgrades if upgrade.index == 9), False)
    lab.bonuses[16].unlocked = next((upgrade.purchased for upgrade in sneaking.jadeUpgrades if upgrade.index == 10), False)
    lab.bonuses[17].unlocked = next((upgrade.purchased for upgrade in sneaking.jadeUpgrades if upgrade.index == 11), False)

    # Append chip info to players
    for player_index, chips in lab.player_chips.items():
        index = int(player_index)
        for chip_index, chip in enumerate(chips):
            player_data[index].lab_info.chips[chip_index].chip = chip

        # Update card boosts
        if any(chip.data.name == "Omega Nanochip" for chip in chips) and player_data[index].card_info:
            player_data[index].card_info.equipped_cards[0].chip_boost = 2
        if any(chip.data.name == "Omega Motherboard" for chip in chips) and player_data[index].card_info:
            player_data[index].card_info.equipped_cards[7].chip_boost = 2

        # Handle starsign doubler
        if any(chip.data.name == "Silkrode Nanochip" for chip in chips):
            for sign in player_data[index].star_signs:
                if sign.aligned:
                    sign.has_chip = True

    # Determine players in lab
    players_in_lab = sorted(
        (player for player in player_data if player.current_monster and player.current_monster.id == "Laboratory" or (divinity.player_info.get(player.playerID, {}).get("isLinkedToGod", lambda x: False)(1))),
        key=lambda player: player.playerID
    )

    lab.players_in_tubes = players_in_lab

    # Merit extra connection range
    connection_merit = next((merit for merit in task_board.merits if "connection range in the Lab" in merit.descLine1), None)
    extra_px_from_bonuses = (connection_merit.bonusPerLevel * connection_merit.level if connection_merit else 0)
    extra_px_from_bonuses += equinox.upgrades[6].getBonus()
    extra_px_from_bonuses += next((bonus.getBonus() for bonus in summoning.summonBonuses if bonus.index == 4), 0)

    # Determine best bubo
    best_bubo = max(player_data, key=lambda player: (player.talents.find(lambda talent: talent.skillIndex == 535) or {}).get("level", 0) > 0 and player.playerID)
    bubo_px_boost = next((talent.getBonus() for talent in best_bubo.talents if talent.skillIndex == 535), 0)
    lab.bestBuboPlayerID = best_bubo.playerID

    # Loop until no more updates
    connected_players = []
    loop_again = True
    while loop_again:
        loop_again = False
        # Calculate player line widths
        calculate_players_line_width(lab, cooking, breeding, cards, gem_store, bubo_px_boost)

        if lab.players_in_tubes and not connected_players:
            prism_player = find_prism_source(lab)
            if prism_player:
                connected_players.append(prism_player)

        # Calculate player impact
        for chain_index in range(len(lab.players_in_tubes)):
            if len(connected_players) > chain_index:
                loop_again = calculate_player_impact(connected_players, chain_index, lab, extra_px_from_bonuses)

    if lab.jewels[16].available:
        # Temporarily activate jewel 16
        lab.jewels[16].active = True
        calculate_players_line_width(lab, cooking, breeding, cards, gem_store, bubo_px_boost)
        lab.jewels[16].active = False

        if lab.players_in_tubes and not connected_players:
            prism_player = find_prism_source(lab)
            if prism_player:
                connected_players.append(prism_player)

        for chain_index in range(len(lab.players_in_tubes)):
            if len(connected_players) > chain_index:
                loop_again = calculate_player_impact(connected_players, chain_index, lab, extra_px_from_bonuses)

        calculate_players_line_width(lab, cooking, breeding, cards, gem_store, bubo_px_boost)

    # Pure Opal Navette
    lab.bonuses[8].jewelBoost = lab.jewels[19].getBonus() / 100
    jewel_multiplier = lab.bonuses[8].getBonus()

    for jewel in lab.jewels:
        if jewel.index != 19:
            jewel.bonusMultiplier = jewel_multiplier

    # Special Jewel handling
    lab.jewels[0].numberOfActivePurples = len([jewel for jewel in lab.jewels if "Amethyst" in jewel.data.name or "Purple" in jewel.data.name and jewel.active])
    lab.jewels[10].numberOfActiveOrange = len([jewel for jewel in lab.jewels if "Pyrite" in jewel.data.name and jewel.active])
    lab.jewels[12].numberOfActiveGreen = len([jewel for jewel in lab.jewels if "Emerald" in jewel.data.name and jewel.active])
    lab.jewels[14].numberOfKitchenLevels = sum(kitchen.recipeLevels + kitchen.mealLevels + kitchen.luckLevels for kitchen in cooking.kitchens)

    # Special Bonus handling
    lab.bonuses[0].totalSpecies = sum(breeding.speciesUnlocks)
    lab.bonuses[9].greenMushroomKilled = sum(round(kill_count) for kill_count in (deathnote.mobKillCount.get("mushG") or []))
    if lab.jewels[13].active:
        lab.bonuses[9].jewelBoost = lab.jewels[13].getBonus()

    lab.bonuses[11].greenStacks = len(set(item.internalName for item in storage.chest if item.count >= 1e7))

    if lab.jewels[18].active:
        lab.bonuses[15].jewelBoost = lab.jewels[18].getBonus()

    if lab.jewels[20].active:
        lab.bonuses[17].jewelBoost = lab.jewels[20].getBonus()

    return lab
