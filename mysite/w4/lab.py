from models.models import AdviceSection, AdviceGroup, Advice, Character, Account
from utils.logging import get_logger
from flask import g as session_data
import math
from consts import (break_you_best, labJewelsDict, labBonusesDict)

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
    # TODO it's only a debug call :
    update_lab(session_data.account)

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


def get_character_linewidth(account: Account, character: Character, px_meal_bonus, line_pct_meal_bonus, passive_card_bonus, pet_arena_bonus, in_gem_tube, bubo_boost,
                            shiny_bonus) -> float:
    base_width = 50 + (2 * character.lab_level)

    if account.labJewels["Sapphire Rhombol"]["Enabled"]:
        if get_distance(*labJewelsDict[5]['Coordinates'], *character.lab_position) < 150:
            base_width *= 1.25

    # 12% per Conductive Motherboard chip equipped
    player_chip_bonus = sum(12 for chip in character.equipped_lab_chips if chip == "Conductive Motherboard")

    bonus_width = 30 if in_gem_tube else 0
    return math.floor(
        (base_width + (px_meal_bonus + min(passive_card_bonus, 50))) *
        (1 + ((bubo_boost + line_pct_meal_bonus + player_chip_bonus + (20 * pet_arena_bonus) + bonus_width + shiny_bonus) / 100))
    )


def calculate_players_line_width(account: Account):
    if account.characters_in_lab:
        px_meal_bonus = account.meals["Pancakes"]["Value"] + account.meals["Wild Boar"]["Value"]
        line_pct_meal_bonus = account.meals["Eel"]["Value"]
        passive_card_bonus = 2 + 2 * next(card.getStars() for card in account.cards if card.name == "Crystal Custard")
        pet_arena_bonus = 1 if account.breeding['ArenaMaxWave'] > 65 else 0
        shiny_bonus = account.breeding["Grouped Bonus"]["Line Width in Lab"][0][1]  # Mallay bonus : +1% per level
        gem_tubes = account.gemshop["Souped Up Tube"] * 2

        for index, character in enumerate(account.characters_in_lab):
            best_bubo: Character = max(
                (bubo for bubo in account.bubos if any(idx == '535' and bubo.current_preset_talents[idx] > 0 for idx in bubo.current_preset_talents)),
                key=lambda bubo: bubo.character_index, default=None)
            # TODO : It's only the skill level for now
            bubo_px_boost = next((best_bubo.current_preset_talents[talentIdx] for talentIdx in best_bubo.current_preset_talents if talentIdx == '535'), 0) if best_bubo else 0
            right_of_bubo = best_bubo and character.lab_position[0] >= best_bubo.lab_position[0]

            character.lab_line_width = get_character_linewidth(
                account, character, px_meal_bonus, line_pct_meal_bonus, passive_card_bonus,
                pet_arena_bonus, index < gem_tubes, bubo_px_boost if right_of_bubo else 0, shiny_bonus
            )


def find_prism_source(account: Account) -> Character | None:
    for character in account.characters_in_lab:
        if get_distance(43, 229, character.lab_position[0], character.lab_position[1]) < character.lab_line_width:
            return character
    return None


def update_lab(account: Account):
    lab = {}
    cooking = {}
    breeding = {}
    deathnote = {}
    storage = {}

    # Append chip info to players
    # for player_index, chips in lab.player_chips.items():
    #     index = int(player_index)
    #     for chip_index, chip in enumerate(chips):
    #         player_data[index].lab_info.chips[chip_index].chip = chip
    #
    #     # Update card boosts
    #     if any(chip.data.name == "Omega Nanochip" for chip in chips) and player_data[index].card_info:
    #         player_data[index].card_info.equipped_cards[0].chip_boost = 2
    #     if any(chip.data.name == "Omega Motherboard" for chip in chips) and player_data[index].card_info:
    #         player_data[index].card_info.equipped_cards[7].chip_boost = 2
    #
    #     # Handle starsign doubler
    #     if any(chip.data.name == "Silkrode Nanochip" for chip in chips):
    #         for sign in player_data[index].star_signs:
    #             if sign.aligned:
    #                 sign.has_chip = True


    extra_px_from_bonuses = account.merits[3][4]["Level"] # W4 Merit extra connection range
    extra_px_from_bonuses += account.equinox_bonuses['Laboratory Fuse']['CurrentLevel'] or 0
    extra_px_from_bonuses += 0  # TODO : Account for the summoning win bonuses ##next((bonus.getBonus() for bonus in summoning.summonBonuses if bonus.index == 4), 0)


    # Loop until no more updates
    connected_players = []
    loop_again = True
    while loop_again:
        loop_again = False
        # Calculate player line widths
        calculate_players_line_width(account)

        if account.characters_in_lab and not connected_players:
            prism_player = find_prism_source(account)
            if prism_player:
                connected_players.append(prism_player)

        # Calculate player impact
        for chain_index in range(len(account.characters_in_lab)):
            if len(connected_players) > chain_index:
                loop_again = calculate_player_impact(account, connected_players, chain_index, lab, extra_px_from_bonuses)

    if account.labJewels['Black Diamond Rhinestone']['Owned']:
        # Temporarily activate jewel 16, meal bonuses
        account.labJewels['Black Diamond Rhinestone']['Enabled'] = True
        calculate_players_line_width(account)
        account.labJewels['Black Diamond Rhinestone']['Enabled'] = False

        if account.characters_in_lab and not connected_players:
            prism_player = find_prism_source(account)
            if prism_player:
                connected_players.append(prism_player)

        for chain_index in range(len(account.characters_in_lab)):
            if len(connected_players) > chain_index:
                loop_again = calculate_player_impact(account, connected_players, chain_index, lab, extra_px_from_bonuses)

        calculate_players_line_width(account)

    # Pure Opal Navette effect on the spelunker. The calculus seems odd, between bonus and value
    account.labBonuses["Spelunker Obol"]["Value"] = account.labJewels["Pure Opal Navette"]["Value"] / 100
    jewel_multiplier =  account.labBonuses["Spelunker Obol"]["Value"]

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


def calculate_player_impact(account : Account, connected_characters: list[Character], chain_index: int, lab, extra_px_from_bonuses: float):
    jewel_multiplier = account.labBonuses["Spelunker Obol"]["Value"]
    jewel_connection_range_bonus = account.labJewels["Pyrite Rhombol"]["Value"] if account.labJewels['Pyrite Rhombol']['Enabled'] else 0
    bonus_connection_range_bonus = account.labBonuses["Viral Connection"]['Value']
    connection_range_bonus = jewel_connection_range_bonus + bonus_connection_range_bonus

    character = connected_characters[chain_index]
    has_impact = False

    # Check players in tubes
    char_pos = character.lab_position
    for tube_character in account.characters_in_lab:
        tube_char_pos = tube_character.lab_position
        in_range = get_distance(char_pos[0], char_pos[1], tube_char_pos[0], tube_char_pos[1]) < tube_character.lab_line_width
        if tube_character not in connected_characters and in_range:
            connected_characters.append(tube_character)
            has_impact = True

    # Activate inactive bonuses in range
    for name, bonus in filter(lambda b: not b[1]["Enabled"], account.labBonuses.items()):
        bonus_pos = labBonusesDict[name]["Coordinates"]
        in_range = get_distance(char_pos[0], char_pos[1], bonus_pos[0], bonus_pos[1]) < _compute_bonus_connection_range(bonus, connection_range_bonus, extra_px_from_bonuses)
        if in_range and bonus["Owned"]:
            bonus["Enabled"] = True
            has_impact = True

    # Activate available but inactive jewels in range
    for name, jewel in filter(lambda j: j[1]["Owned"] and not j[1]["Enabled"], account.labJewels.items()):
        jewel_pos = next(filter(lambda item: item[1]['Name'] == name, labJewelsDict.items()))[1]['Coordinates']
        in_range = get_distance(char_pos[0], char_pos[1], jewel_pos[0], jewel_pos[1]) < _compute_jewel_connection_range(jewel, connection_range_bonus, extra_px_from_bonuses)
        if in_range:
            jewel["Enabled"] = True
            has_impact = True

    return has_impact

def _compute_bonus_connection_range(bonus : str, connection_range_bonus : float, extra_px_from_bonuses : float) -> float:
    if bonus == "Viral Connection" or bonus == "Spelunker Obol":
        return 80
    return math.floor((80 * (1 + connection_range_bonus / 100)) + extra_px_from_bonuses)

def _compute_jewel_connection_range(jewel : str, connection_range_bonus : float, extra_px_from_bonuses : float) -> float:
    if jewel == "Pyrite Rhombol" or jewel == "Pure Opal Navette":
        return 80
    return math.floor((80 * (1 + connection_range_bonus / 100)) + extra_px_from_bonuses)
