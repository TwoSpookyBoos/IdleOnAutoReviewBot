from models.models import Advice, AdviceGroup, AdviceSection, EnemyWorld, EnemyMap
from consts import lavaFunc, stamp_maxes, pearlable_skillsList, max_VialLevel, currentWorld, dnSkullValueList, cookingCloseEnough, dnBasicMapsCount
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data

from utils.text_formatting import notateNumber

logger = get_logger(__name__)

def getCrystalSpawnChanceAdviceGroup() -> AdviceGroup:
    aw = "Account Wide"
    cs = "Character Specific"
    total = "Total"
    crystal_Advice = {
        aw: [],
        cs: [],
        total: [],
    }
    # Account Wide
    crystal_Advice[aw].append(Advice(
        label="Chocco Chip for more Crystal Mobs",
        picture_class="chocolatey-chip",
        progression=session_data.account.labChips.get('Chocolatey Chip', 0),
        goal=1
    ))
    crystal_Advice[aw].append(Advice(
        label=f"W4 Demon Genie card: +{15 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Demon Genie'))}"
              f"/90% Crystal Mob Spawn Chance",
        picture_class="demon-genie-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == "Demon Genie"),
        goal=6
    ))
    crystal_Advice[aw].append(Advice(
        label=f"W1 Poop card: +{10 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Poop'))}"
              f"/60% Crystal Mob Spawn Chance",
        picture_class="poop-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == "Poop"),
        goal=6
    ))
    crystal_Advice[aw].append(Advice(
        label="Omega Nanochip: Top Left card doubler",
        picture_class="omega-nanochip",
        progression=session_data.account.labChips.get('Omega Nanochip', 0),
        goal=1
    ))
    crystal_Advice[aw].append(Advice(
        label="Omega Motherboard: Bottom Right card doubler",
        picture_class="omega-motherboard",
        progression=session_data.account.labChips.get('Omega Motherboard', 0),
        goal=1
    ))
    crystal_Advice[aw].append(Advice(
        label=f"Level {session_data.account.stamps['Crystallin']['Level']}/{stamp_maxes['Crystallin']} Crystallin Stamp: {1 + session_data.account.stamps['Crystallin']['Value'] / 100:.3f}x",
        picture_class="crystallin",
        progression=session_data.account.stamps['Crystallin']['Level'],
        goal=stamp_maxes['Crystallin']
    ))
    crystal_Advice[aw].append(session_data.account.shrine_advices['Crescent Shrine'])
    crystal_Advice[aw].append(session_data.account.shrine_advices['Chaotic Chizoar Card'])
    crystal_Advice[aw].append(Advice(
        label=f"{{{{ Sailing|#sailing }}}}: Moai Head artifact to apply Shrines everywhere",
        picture_class="moai-head",
        progression=session_data.account.sailing['Artifacts']['Moai Head']['Level'],
        goal=1
    ))

    # Character Specific
    bestCrystalBook = 0
    for jman in session_data.account.jmans:
        bestCrystalBook = max(bestCrystalBook, jman.max_talents.get("26", 0))
    crystal_Advice[cs].append(Advice(
        label=f"Level {bestCrystalBook}/{session_data.account.library['MaxBookLevel']} booked Cmon Out Crystals talent (Jman only)",
        picture_class="cmon-out-crystals",
        progression=bestCrystalBook,
        goal=session_data.account.library['MaxBookLevel']
    ))
    crystals_4_dayys_multi = 1 + lavaFunc('decay', 100, 174, 50) / 100
    crystal_Advice[cs].append(Advice(
        label=f"Crystals 4 Dayys star talent: {crystals_4_dayys_multi}x at level 100",
        picture_class="crystals-4-dayys",
    ))
    box_value = lavaFunc('decay', 300, 65, 200)
    crystal_Advice[cs].append(Advice(
        label=f"Non Predatory Loot Box: +{box_value:.0f}% at 400 crates",
        picture_class="non-predatory-loot-box",
    ))

    # Totals
    crystal_Advice[total].append(Advice(
        label=f"Note: Crescent Shrine and PO Box are additive: {1 + ((session_data.account.shrines['Crescent Shrine']['Value'] + box_value) / 100):.3f}x"
              f"<br>The cards also add together. Everything else is a unique multiplier.",
        picture_class="shrine-box2"
    ))

    crystal_Advice[total].append(Advice(
        label=f"Best Crystal Spawn Chance on Non-Jman:"
              f" {session_data.account.highest_crystal_spawn_chance * 100:.4f}%"
              f" (1 in {100 / (session_data.account.highest_crystal_spawn_chance * 100):.2f})",
        picture_class="crystal-carrot",
    ))
    crystal_Advice[total].append(Advice(
        label=f"Best Crystal Spawn Chance on Jman:"
              f" {session_data.account.highest_jman_crystal_spawn_chance * 100:.4f}%"
              f" (1 in {100 / (session_data.account.highest_jman_crystal_spawn_chance * 100):.2f})",
        picture_class="crystal-crabal",
    ))

    for subgroup in crystal_Advice:
        for advice in crystal_Advice[subgroup]:
            mark_advice_completed(advice)

    crystal_AG = AdviceGroup(
        tier="",
        pre_string="Info- Sources of Crystal Spawn Chance",
        advices=crystal_Advice,
        informational=True,
    )
    return crystal_AG

def getShortTermAdviceList() -> list[Advice]:
    shortterm = []
    obols = []
    #Div jail if Goat not unlocked
    quick_divinity_goals = [2, 5]
    for divinity in quick_divinity_goals:
        if max(session_data.account.all_skills.get("Divinity", [0])) > 0 and not session_data.account.divinity['Divinities'][divinity]['Unlocked']:
            shortterm.append(Advice(
                label=f"Divinity jail until you unlock {session_data.account.divinity['Divinities'][divinity]['Name']} 🙁",
                picture_class=session_data.account.divinity['Divinities'][divinity]['Name'],
                progression=session_data.account.divinity['GodsUnlocked'],
                goal=divinity
            ))
            break
    if not session_data.account.labBonuses['No Bubble Left Behind']['Enabled']:
        shortterm.append(Advice(
            label=f"Lab jail until you unlock No Bubble Left Behind 🙁",
            picture_class='no-bubble-left-behind',
        ))

    #OBOLS
    if 10 > session_data.account.obols['Drop Rate']['Square']['Total']:
        obols.append(Advice(
            label=f"Farm Dice Obols for Square slots with DK at Sandy Pots"
                  f"<br>Note: Hyper Six Obols are included in your progress",
            picture_class='golden-obol-of-triple-sixes',
            resource='crystal-crabal',
            progression=session_data.account.obols['Drop Rate']['Square']['Total'],
            goal=10  # 4 family, 6 personal
        ))
    if 6 > session_data.account.obols['Drop Rate']['Hexagon']['Total']:
        obols.append(Advice(
            label=f"Farm Dice Obols for Hexagon slots with DK at Sandy Pots"
                  f"<br>Note: W5 Miniboss Obols are included in your progress",
            picture_class='platinum-obol-of-yahtzee-sixes',
            resource='crystal-crabal',
            progression=session_data.account.obols['Drop Rate']['Hexagon']['Total'],
            goal=6  # 4 family, 2 personal
        ))
    if 5 > session_data.account.obols['Drop Rate']['Sparkle']['Total']:
        obols.append(Advice(
            label=f"Farm Dice Obols for Sparkle slots with DK at Sandy Pots",
            picture_class='dementia-obol-of-infinisixes',
            resource='crystal-crabal',
            progression=session_data.account.obols['Drop Rate']['Sparkle']['Total'],
            goal=5  # 4 family, 1 personal
        ))
    if 24 > session_data.account.obols['Drop Rate']['Circle']['Total']:
        # If Chocco Chip is owned, POPs last, otherwise POPs first
        obols.insert(0 if session_data.account.labChips['Chocolatey Chip'] > 0 else len(obols), Advice(
            label=f"Farm POP Obols for Circle slots with ES at Gigafrogs"
                  f"<br>Note: Hyper Six Obols are included in your progress",
            picture_class='silver-obol-of-pop-pop',
            resource='gigafrog',
            progression=session_data.account.obols['Drop Rate']['Circle']['Total'],
            goal=24  #12 family, 12 personal
        ))
    shortterm += obols

    for char in session_data.account.all_characters:
        if 'Journeyman' not in char.all_classes:
            for mapNumber, details in {
                1: [1, 'weekly-boss-action-t'],  # Green Mushrooms
                53: [2, 'weekly-boss-action-r'],  # Crabcakes
                116: [3, 'weekly-boss-action-u'],  # Dedotated Rams
                158: [4, 'weekly-boss-action-y'],  # Choccies
                205: [5, 'weekly-boss-action-v'],  # Stiltmoles
            }.items():
                enemy_map = session_data.account.enemy_worlds[details[0]].maps_dict[mapNumber]
                goal = 1000000
                try:
                    char_kills = enemy_map.portal_requirement - char.kill_dict.get(mapNumber, [0])[0]
                    if char_kills < goal:
                        #logger.debug(f"{char} {enemy_map.monster_name} KLA: {char.kill_dict.get(mapNumber, [0])[0]} means total kills of {char_kills}")
                        shortterm.append(Advice(
                            label=f"{char}- Kill 1M {enemy_map.monster_name}s for W2 Weekly Boss",
                            picture_class=char.class_name_icon,
                            progression=notateNumber('Match', char_kills, 2, 'K'),
                            goal=notateNumber('Match', goal, 0, 'K'),
                            resource=details[1]
                        ))
                except Exception as reason:
                    logger.debug(f"W{details[0]}M{mapNumber} '{char}': {reason}")
                    continue

    return shortterm

def getCardsAdviceList() -> list[Advice]:
    cards = []
    card_level_goal = 6 if session_data.account.rift['RubyCards'] else 5
    all_cards = {
        "Card Drop Chance": ["Sir Stache", "Snelbie", "Gigafrog"],
        "Shrine Value": ["Chaotic Chizoar"],
        "Crystal Spawn Chance": ["Demon Genie", "Poop"],
        "Drop Chance": ["Emperor", "Minichief Spirit", "King Doot", "Mister Brightside", "Crystal Carrot", "Bop Box"],
        "Skilling Goodness": ["Chaotic Troll", "Amarok", "Mama Troll", "Bunny"],
        "Combat Gains": ["Chaotic Amarok", "Boop", "Woodlin Spirit", "Suggma", "Clammie", "Demented Spiritlord", "Moonmoon", "Fly"],
        "Solid Passives": ["Godshard Ore", "Crystal Candalight", "Crystal Capybara", "Samurai Guardian", "Royal Egg", "Domeo Magmus"],
        "Stat% Filler": ["River Spirit", "Blighted Chizoar", "Tremor Wurm", "Stilted Seeker"],
    }
    card_advice_limit = 10

    for reason, cardnameList in all_cards.items():
        for card in cardnameList:
            #logger.debug(f"Looking up card: {card}")
            if (1 + next(c.getStars() for c in session_data.account.cards if c.name == card)) < card_level_goal and len(cards) < card_advice_limit:
                cards.append(Advice(
                    label=f"Farm {card} cards for {reason}",
                    picture_class=f"{card}-card",
                    progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == card),
                    goal=card_level_goal
                ))

    return cards

def getLongTermAdviceList() -> list[Advice]:
    longterm = []
    # 2100 lab for jewels
    if sum(session_data.account.all_skills.get("Lab", [0])) < 2100:
        longterm.append(Advice(
            label=f"Lab jail until 2100 total Lab levels for W6 jewels 🙁"
                  f"<br>Note: You probably want to link to Goat and level Divinity at the same time"
                  f"{'<br>Also: Buy Laboratory Bling from Jade Emporium' if not session_data.account.sneaking['JadeEmporium']['Laboratory Bling']['Obtained'] else ''}",
            picture_class='Laboratory Bling',
            resource='laboratory',
            progression=sum(session_data.account.all_skills.get("Lab", [0])),
            goal=2100
        ))
    # Gmush Farming
    for killTarget in [1e6, 500e6, 1e9, 100e9, 500e9, 1e12]:
        if killTarget > session_data.account.enemy_worlds[1].maps_dict[1].kill_count:
            goalString = notateNumber('Basic', killTarget, 0)
            longterm.append(Advice(
                label=f"Kill more Gmush for Money multi"
                      f"<br>AFK or Candy kills with highest KPH character",
                picture_class='fungi-finger-pocketer',
                progression=notateNumber("Match", session_data.account.enemy_worlds[1].maps_dict[1].kill_count, 2, '', goalString),
                goal=notateNumber("Match", killTarget, 0, '', goalString),
                resource=session_data.account.enemy_worlds[1].maps_dict[1].monster_image
            ))
            break  # Only show the next closest target

    # SB Plunder Kills
    for killTarget in [1e3, 10e3, 32e3, 100e3, 320e3, 1e6]:
        if killTarget > session_data.account.sb_plunder_kills:
            goalString = notateNumber("Basic", killTarget, 1)
            longterm.append(Advice(
                label=f"Farm more Plunder Kills with Siege Breaker for Drop Rate"
                      f"<br>Crystal Setup at W5 Citringes for ~20k per day",
                picture_class='archlord-of-the-pirates',
                progression=notateNumber("Match", session_data.account.sb_plunder_kills, 2, '', goalString),
                goal=goalString,
                resource='pirate-flag'
            ))
            break  # Only show the next closest target

    # DK Orb Kills
    for killTarget in [1e3, 10e3, 32e3, 100e3, 320e3, 1e6]:
        if killTarget > session_data.account.dk_orb_kills:
            goalString = notateNumber("Basic", killTarget, 1)
            longterm.append(Advice(
                label=f"Farm more Orb stacks with Divine Knight for Printer Output"
                      f"<br>Crystal Setup at any world you need Crystal loot from",
                picture_class='king-of-the-remembered',
                progression=notateNumber("Match", session_data.account.dk_orb_kills, 2, '', goalString),
                goal=goalString,
                resource='orb-of-remembrance'
            ))
            break  # Only show the next closest target

    # ES Wormhole Kills
    for killTarget in [1e3, 10e3, 32e3, 100e3, 320e3, 1e6]:
        if killTarget > session_data.account.es_wormhole_kills:
            goalString = notateNumber("Basic", killTarget, 1)
            longterm.append(Advice(
                label=f"Farm more Wormhole kills with Elemental Sorcerer for Damage"
                      f"<br>Generally alongside farming Rare Drops, such as Dark Lanterns",
                picture_class='wormhole-emperor',
                progression=notateNumber("Match", session_data.account.es_wormhole_kills, 2, '', goalString),
                goal=goalString,
                resource='dimensional-wormhole'
            ))
            break  # Only show the next closest target

    # Bubo Liquid Decants
    if session_data.account.equinox_bonuses['Liquidvestment']['CurrentLevel'] < session_data.account.equinox_bonuses['Liquidvestment']['FinalMaxLevel']:
        equinox_note = f"<br>Whoa, get maxed Liquidvestment from {{{{ Equinox|#equinox }}}} first!"
    else:
        equinox_note = ''
    for levelTarget in [100, 200, 400, 600, 800, 1000]:
        if levelTarget > session_data.account.alchemy_cauldrons["WaterDroplets"][1]:
            longterm.append(Advice(
                label=f"Increase Water Droplet Rate via Active Bubo"
                      f"<br>W5 Wurms or W6 Minichiefs recommended"
                      f"{equinox_note}",
                picture_class='cranium-cooking',
                progression=session_data.account.alchemy_cauldrons["WaterDroplets"][1],
                goal=levelTarget,
                resource='Water Droplets'
            ))
            break  # Only show the next closest target
    return longterm

def getDailyAdviceList() -> list[Advice]:
    daily = []

    if session_data.account.daily_particle_clicks_remaining > 0:
        daily.append(Advice(
            label=f"Spend Alternative Particle Clicks for {{{{ Bubbles|#bubbles }}}}",
            picture_class='boron',
            progression=session_data.account.daily_particle_clicks_remaining
        ))

    if session_data.account.minigame_plays_remaining > 0:
        daily.append(Advice(
            label=f"Spend remaining daily Minigame plays",
            picture_class='daily-minigame-plays',
            progression=session_data.account.minigame_plays_remaining
        ))
    if session_data.account.daily_world_boss_kills < 300:
        daily.append(Advice(
            label=f"Daily World Boss retries for Gems",
            picture_class='gem',
            progression=session_data.account.daily_world_boss_kills,
            goal=300,
            resource='kruks-volcano-key'
        ))
    return daily

def getWeeklyAdviceList() -> list[Advice]:
    weekly = []

    return weekly

def getConsumablesAdviceList() -> list[Advice]:
    consumables = []

    #If 30+ Colo tickets owned
    total_colo_tickets = session_data.account.stored_assets.get('TixCol').amount + session_data.account.raw_data.get("CYColosseumTickets", 0)
    if total_colo_tickets > 300 and session_data.account.highestWorldReached >= 6:
        consumables.append(Advice(
            label=f"{total_colo_tickets} Colo Tickets available",
            picture_class='colosseum-ticket',
        ))

    if (
            session_data.account.stored_assets.get('Quest35').amount
            + session_data.account.stored_assets.get('Quest36').amount
            + session_data.account.stored_assets.get('Quest37').amount
    ) > 300:
        biggies = f"<br>{session_data.account.stored_assets.get('Quest35').amount} Biggie Hours available" if session_data.account.stored_assets.get(
            'Quest35').amount > 0 else ''
        doot_total = session_data.account.stored_assets.get('Quest36').amount + session_data.account.stored_assets.get('Quest37').amount
        doots = f"<br>{doot_total} King Doots available" if doot_total > 0 else ''

        consumables.append(Advice(
            label=f"Spend W2 Miniboss Summon Items for more consumables lol:"
                  f"{biggies}"
                  f"{doots}",
            picture_class='googley-eyes',
            resource='dootjat-eye'
        ))

    #Pearls and Balloons
    if session_data.account.highestWorldReached >= 4:
        # Black Pearls
        if session_data.account.stored_assets.get('Pearl4').amount > 0:
            black_pearlable_skills = [skillName for skillName in pearlable_skillsList if min(session_data.account.all_skills.get(skillName, [0])) < 30]
            if black_pearlable_skills:
                consumables.append(Advice(
                    label=f"Spend Black Pearls on Skills under level 30:"
                          f"<br>{', '.join(skillName for skillName in black_pearlable_skills)}",
                    picture_class='black-pearl' if len(black_pearlable_skills) > 1 else black_pearlable_skills[0],
                    resource='black-pearl'
                ))
        # Red Pearls
        if session_data.account.stored_assets.get('Pearl6').amount > 0:
            red_pearlable_skills = [skillName for skillName in pearlable_skillsList if min(session_data.account.all_skills.get(skillName, [0])) < 50]
            if red_pearlable_skills:
                consumables.append(Advice(
                    label=f"Spend Divinity Pearls on Skills under level 50:"
                          f"<br>{', '.join(skillName for skillName in red_pearlable_skills)}",
                    picture_class='divinity-pearl' if len(red_pearlable_skills) > 1 else red_pearlable_skills[0],
                    resource='divinity-pearl'
                ))
        # Balloons
        if (
                session_data.account.stored_assets.get('ExpBalloon1').amount
                + session_data.account.stored_assets.get('ExpBalloon2').amount
                + session_data.account.stored_assets.get('ExpBalloon3').amount
        ) > 0:
            balloonable_skills = [skillName for skillName in pearlable_skillsList if sum(session_data.account.all_skills.get(skillName, [0])) < 750]
            if balloonable_skills:
                consumables.append(Advice(
                    label=f"Spend Experience Balloons on Skills under 750 Skill Mastery for Printer Output:"
                          f"<br>{', '.join(skillName for skillName in balloonable_skills)}",
                    picture_class='small-experience-balloon' if len(balloonable_skills) > 1 else balloonable_skills[0],
                    resource='small-experience-balloon'
                ))

    # Candy options
    if session_data.account.highestWorldReached >= 2:
        if not session_data.account.maestros and session_data.account.jmans:
            consumables.append(Advice(
                label=f"Level any remaining skills for {{{{ Maestro|#secret-class-path }}}} quest."
                      f"<br>Pearls, Balloons, and Candies are all valid here!",
                picture_class='maestro-icon',
                resource='time-candy-1-hr'
            ))
    if session_data.account.highestWorldReached >= 4:
        for character in session_data.account.all_characters:
            try:
                if (
                    character.elite_class == "None"
                    and 'Journeyman' not in character.all_classes
                    and float(character.kill_dict.get(153, [0])[0]) > 0  #Killcount on Donut map would be 0 or negative if portal to Demon Genies is open
                ):

                    consumables.append(Advice(
                        label=f"Candy {character.character_name} through W4 maps to obtain their Elite Class",
                        picture_class=character.class_name_icon,
                        resource='time-candy-4-hr'
                    ))
            except:
                continue
        if not session_data.account.vmans:
            consumables.append(Advice(
                label=f"Candy any remaining kills for {{{{ Voidwalker|#secret-class-path }}}} quest",
                picture_class='voidwalker-icon',
                resource='time-candy-1-hr'
            ))
    if session_data.account.highestWorldReached >= 6:
        for worldIndex in range(1, currentWorld):
            if session_data.account.enemy_worlds[worldIndex].lowest_skull_value < dnSkullValueList[-1]:
                consumables.append(Advice(
                    label=f"Candy World {worldIndex} kills for {{{{ Death Note|#death-note }}}}",
                    picture_class='death-note',
                    resource='time-candy-24-hr'
                ))
        if session_data.account.cooking['MaxRemainingMeals'] > cookingCloseEnough and session_data.account.apocalypse_character_Index is not None:
            if session_data.account.all_characters[session_data.account.apocalypse_character_Index].apoc_dict['MEOW']['Total'] < dnBasicMapsCount:
                consumables.append(Advice(
                    label=f"Candy Super CHOW stacks with {session_data.account.all_characters[session_data.account.apocalypse_character_Index].character_name}",
                    picture_class='death-note',
                    resource='time-candy-24-hr'
                ))

        total_gold_cakes = session_data.account.all_assets.get('FoodG13').amount

        if (
            session_data.account.sneaking['JadeEmporium']["Gold Food Beanstalk"]['Obtained']
            and not session_data.account.sneaking['Beanstalk']['FoodG13']['Beanstacked']
        ):
            consumables.append(Advice(
                label=f"Candy materials to Beanstack Golden Cakes in {{{{ The Beanstalk|#beanstalk }}}}",
                picture_class='golden-cake',
                resource='time-candy-24-hr',
                progression=notateNumber("Match", total_gold_cakes, 2, "K"),
                goal="10K"
            ))
        elif (
            session_data.account.sneaking['JadeEmporium']["Supersized Gold Beanstacking"]['Obtained']
            and not session_data.account.sneaking['Beanstalk']['FoodG13']['SuperBeanstacked']
        ):
            consumables.append(Advice(
                label=f"Candy materials to Super Beanstack Golden Cakes in {{{{ The Beanstalk|#beanstalk }}}}",
                picture_class='golden-cake',
                resource='time-candy-24-hr',
                progression=notateNumber("Match", total_gold_cakes, 2, "K"),
                goal="100K"
            ))

        elif total_gold_cakes < 100e3:
            consumables.append(Advice(
                label=f"Get another 100k Golden Cakes to wear while farming",
                picture_class='golden-cake',
                resource='time-candy-24-hr',
                progression=notateNumber("Match", total_gold_cakes, 2, "K"),
                goal="100K"
            ))
    if session_data.account.stamps['Mason Jar Stamp']['Level'] < stamp_maxes['Mason Jar Stamp']:
        consumables.append(Advice(
            label=f"Candy Glass Shards for Mason Jar Stamp",
            picture_class='mason-jar-stamp',
            progression=session_data.account.stamps['Mason Jar Stamp']['Level'],
            goal=stamp_maxes['Mason Jar Stamp'],
            resource='time-candy-1-hr'
        ))
    if 0 < session_data.account.alchemy_vials['Dabar Special (Godshard Bar)']['Level'] < max_VialLevel:
        consumables.append(Advice(
            label=f"2 minute Archer AFK claims (or candy) to smelt Metal bars"
                  f"<br>{{{{ Smithing|#smithing }}}} has Forge Ore Capacity sources"
                  f"<br>Ideally, you want 150k+ capacity before going too hard",
            picture_class='smeltin-erryday',
            resource='time-candy-1-hr'
        ))

    return consumables

def getActiveGoalsAdviceGroup() -> AdviceGroup:
    ag = AdviceGroup(
        tier="",
        pre_string="Active Farming goals, not 100% ordered yet. Pick which sounds interesting ¯\\_(ツ)_/¯",
        advices={
            "Short Term": getShortTermAdviceList(), "Cards": getCardsAdviceList(), "Long Term": getLongTermAdviceList(),
            "Daily": getDailyAdviceList(), "Weekly": getWeeklyAdviceList(), "Spend Consumables": getConsumablesAdviceList()
        },
        informational=True  #TODO One day, these should probably be real requirements
    )
    ag.remove_empty_subgroups()

    return ag

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    template_AdviceDict = {
        'Tiers': {},
    }
    info_tiers = 0
    max_tier = 0 - info_tiers
    tier_Active = 0

    #Assess Tiers

    tiers_ag = AdviceGroup(
        tier=tier_Active,
        pre_string="Progression Tiers",
        advices=template_AdviceDict['Tiers']
    )
    overall_SectionTier = min(max_tier + info_tiers, tier_Active)
    return tiers_ag, overall_SectionTier, max_tier, max_tier + info_tiers

def getActiveAdviceSection() -> AdviceSection:
    if session_data.account.highestWorldReached < 4:
        active_AdviceSection = AdviceSection(
            name="Active",
            tier="Not Yet Evaluated",
            header="Come back after reaching W4 town!",
            picture='Auto.png',
            unrated=True,
            unreached=True
        )
        return active_AdviceSection

    # Generate AdviceGroups
    active_AdviceGroupDict = {}
    active_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    active_AdviceGroupDict['Crystals'] = getCrystalSpawnChanceAdviceGroup()
    active_AdviceGroupDict['ActiveFarming'] = getActiveGoalsAdviceGroup()

    # Generate AdviceSection

    tier_section = f"{overall_SectionTier}/{max_tier}"
    active_AdviceSection = AdviceSection(
        name="Active",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Active Farming Information",
        picture='Auto.png',
        groups=active_AdviceGroupDict.values(),
        unrated=True,
    )
    return active_AdviceSection
