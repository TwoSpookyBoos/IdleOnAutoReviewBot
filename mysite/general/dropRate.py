from models.models import Advice, AdviceGroup, AdviceSection
from consts import max_card_stars, maxFarmingCrops, maxLandRankLevel, max_IndexOfSigils
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data

from utils.text_formatting import notateNumber

logger = get_logger(__name__)

def getCardSetProgress():
    return

def getDropRateAccountAdviceGroup() -> AdviceGroup:
    dropRate_shiny_base = 1
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
    dropRate_Advice = {
        cards: [],
        misc: [],
        multi: []
    }

    dropRate_cards = [
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
    for card in dropRate_cards:
        dropRate_Advice[cards].append(Advice(
            label=f"{card['Name']}'card: +{card['Base'] * card['Stars']:g}/{card['Base'] * (1 + max_card_stars):g} {card['Bonus']}",
            picture_class=card['Picture'],
            progression=card['Stars'],
            goal=(1 + max_card_stars)
        ))

    bnn_stars_sum = sum(min(card.star, max_card_stars) + 1 for card in bnn_cardset)
    bnn_star, _ = divmod(bnn_stars_sum, len(bnn_cardset))
    bnn_star = min(bnn_star, max_card_stars)
    bnn_star_next = (bnn_star + 1) * len(bnn_cardset)
    dropRate_Advice[cards].append(Advice(
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
    dropRate_Advice[cards].append(Advice(
        label=f"Events card set: +{7 * events_star}"
              f"/{7 * (1 + max_card_stars)} Drop Rate | Cards until next set level {events_stars_sum}/{events_star_next}",
        picture_class='events',
        progression=events_star,
        goal=6
    ))

    # Misc
    #########################################
    dropRate_Advice[misc].append(Advice(
        label='W6 Big Big Hampter achievement +4% Drop Rate',
        picture_class='big-big-hampter',
        progression=1 if session_data.account.achievements['Big Big Hampter']['Complete'] else 0,
        goal=1
    ))
    dropRate_Advice[misc].append(Advice(
        label='W6 Summoning GM achievement +6% Drop Rate',
        picture_class='summoning-gm',
        progression=int(session_data.account.achievements['Summoning GM']['Complete']),
        goal=1
    ))

    dropRate_arcadebonus_id = 27
    _, dropRate_arcade  = list(session_data.account.arcade.items())[dropRate_arcadebonus_id]
    dropRate_Advice[misc].append(Advice(
        label=f"Arcade Bonus {dropRate_arcadebonus_id}: {dropRate_arcade['Display']}",
        picture_class=dropRate_arcade['Image'],
        progression=dropRate_arcade['Level'],
        resource=dropRate_arcade['Material'],
        goal=101
    ))

    # Maybe up the goal to 6930 for +39.6% at 99% or 2730 for a nice round +39%?
    dropinLoads_bubble = session_data.account.alchemy_bubbles['Droppin Loads']
    dropRate_Advice[misc].append(Advice(
        label=f"Alchemy Bubble Droppin Loads +{round(dropinLoads_bubble['BaseValue'], 2):g}% Drop Rate",
        picture_class='droppin-loads',
        progression=dropinLoads_bubble['Level'],
        goal=1330
    ))

    grotto_cavern = session_data.account.caverns['Caverns']['Grotto']
    gloomieLootie_schematic = session_data.account.caverns['Schematics']['Gloomie Lootie']
    dropRate_Advice[misc].append(Advice(
        label=f"Engineer Schematic Gloomie Lootie +{5 * grotto_cavern['OpalsFound']}% Drop Rate",
        picture_class=gloomieLootie_schematic['Image'],
        progression=grotto_cavern['OpalsFound'] if gloomieLootie_schematic['Purchased'] else 0,
        goal='∞'
    ))

    cropsUnlocked = session_data.account.farming['CropsUnlocked']
    dropRate_Advice[misc].append(Advice(
        label=f"Crop Depot Highlighter +{(cropsUnlocked - 100) if (cropsUnlocked > 100) else 0}/{maxFarmingCrops-100}%"
              f" Drop Rate {' (value only increases after 100 crops found)' if (cropsUnlocked <= 100) else ''}",
        picture_class='depot-highlighter',
        progression=cropsUnlocked,
        goal=maxFarmingCrops
    ))

    # Companions - Crystal Custard
    hasCrystalCustard= session_data.account.companions['Crystal Custard']
    dropRate_Advice[misc].append(Advice(
        label=f"Crystal Custard companion +{100 if hasCrystalCustard else 0}/100% Drop Rate",
        picture_class='crystal-custard',
        progression=int(hasCrystalCustard),
        goal=1
    ))

    # Equinox - Faux Jewels
    # Will show additional info if player is maxed out for their currently available levels
    fauxJewels_bonus = session_data.account.equinox_bonuses['Faux Jewels']
    fauxJewels_level = fauxJewels_bonus['CurrentLevel']
    dropRate_Advice[misc].append(Advice(
        label=f"Equinox Faux Jewels +{5 * fauxJewels_level}% Drop Rate"
              f"{' (increase Faux Jewels max with Endless Summoning)' if fauxJewels_level == fauxJewels_bonus['PlayerMaxLevel'] else ''}",
        picture_class='faux-jewels',
        progression=fauxJewels_level,
        goal='∞' # This is technically Endless, since Endless Summoning increases the max level
    ))

    # Beanstalk - Golden Cake
    cake_beanstalkName ='FoodG13'
    cake_beanstalk = session_data.account.sneaking['Beanstalk'][cake_beanstalkName]
    cake_beanstalkLevel = int(cake_beanstalk['Beanstacked']) + int(cake_beanstalk['SuperBeanstacked'])
    if cake_beanstalkLevel == 2:
        cake_beanstalkBonus = '+6.67'
    elif cake_beanstalkLevel == 1:
        cake_beanstalkBonus = '+4.59'
    else:
        cake_beanstalkBonus = '0%'
    dropRate_Advice[misc].append(Advice(
        label=f"Beanstalk Golden Cake {cake_beanstalkBonus}/6.67% Drop Rate (further increased by Golden Food multi)",
        picture_class='golden-cake',
        progression=cake_beanstalkLevel,
        goal=2
    ))

    # Guild Bonus - Gold Charm
    goldCharm_bonus = session_data.account.guildBonuses['Gold Charm']
    dropRate_Advice[misc].append(Advice(
        label=f"Guild Bonus Gold Charm +{goldCharm_bonus['Value']:g}"
              f"/{goldCharm_bonus['MaxValue']:g}% Drop Rate",
        picture_class=goldCharm_bonus['Picture'],
        progression=goldCharm_bonus['Level'],
        goal=goldCharm_bonus['MaxLevel']
    ))

    # TODO: Add temporary line for + Land Rank Level
    # Land Rank - Seed of Loot
    # Will show additional info if the player does not have the current max number of available land rank levels
    seedOfLoot_landRank = session_data.account.farming['LandRankDatabase']['Seed of Loot']
    dropRate_Advice[misc].append(Advice(
        label=f"Land Rank Seed of Loot +{seedOfLoot_landRank['BaseValue'] * seedOfLoot_landRank['Level']}"
              f"/{seedOfLoot_landRank['BaseValue'] * maxLandRankLevel}% Drop Rate"
              f"{' (increase Land Rank max with Grimoire)' if seedOfLoot_landRank['Level'] < maxLandRankLevel else ''}",
        picture_class='seed-of-loot',
        progression=seedOfLoot_landRank['Level'],
        goal=maxLandRankLevel
    ))

    # Rift - Sneak Mastery 1
    sneakMastery_level = session_data.account.sneaking['MaxMastery']
    dropRate_Advice[misc].append(Advice(
        label=f"Rift Sneaking Mastery +{30 if (sneakMastery_level > 0) else 0}/30% Drop Rate",
        picture_class='sneaking-mastery',
        progression=sneakMastery_level,
        goal=1
    ))

    # Owl Bonuses
    dropRate_owlBonus = session_data.account.owlBonuses['Drop Rate']
    dropRate_Advice[misc].append(Advice(
        label=f"Bonuses of Orion +{dropRate_owlBonus['Value']}% Drop Rate",
        picture_class='drop-rate',
        progression=dropRate_owlBonus['NumUnlocked'],
        goal='∞'
    ))

    # Gem Shop - DB Pack
    dropRate_Advice[misc].append(Advice(
        label="Gemshop Deathbringer Pack +200% Drop Rate (can't tell if you have this)",
        picture_class='gem',
        progression='IDK',
        goal='IDK'
    ))

    # Breeding - Shiny Pets
    dropRate_shinyLevel = 0
    dropRate_shinyValue = 0
    for name, shiny in session_data.account.breeding['Species'][1].items():
        if shiny['ShinyBonus'] == 'Drop Rate':
            dropRate_shinyLevel += shiny['ShinyLevel']
            dropRate_shinyValue += dropRate_shiny_base * shiny['ShinyLevel']
    dropRate_Advice[misc].append(Advice(
        label=f"Total Shiny Critter +{dropRate_shinyValue}% Drop Rate",
        picture_class='breeding',
        progression=dropRate_shinyLevel,
        goal='∞'
    ))

    # Shrine - Clover Shrine
    dropRate_Advice[misc].append(Advice(
        label=f"Shrine +{session_data.account.shrines['Clover Shrine']['Value']:g}% Drop Rate",
        picture_class='clover-shrine',
        progression=session_data.account.shrines['Clover Shrine']['Level'],
        goal='∞'
    ))

    # Sigil
    troveSigil_level = session_data.account.alchemy_p2w['Sigils']['Trove']['Level']
    dropRate_Advice[misc].append(Advice(
        label=f"Clover Sigil +{sigils_trove_base * troveSigil_level}"
              f"/{sigils_trove_base * max_IndexOfSigils}% Drop Rate",
        picture_class='trove',
        progression=troveSigil_level,
        goal=max_IndexOfSigils
    ))

    # Stamps - Golden Sixes + Pristine Charm - Liqorice Rolle (only show if missing charm)
    if session_data.account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained']:
        dropRate_Advice[misc].append(Advice(
            label=f"Liqorice Rolle pristine charm (buffs the stamp below)",
            picture_class='liqorice-rolle',
            progression=0, # we're only showing if it's missing, so just assume 0
            goal=1
        ))
    goldenSixes_stamp = session_data.account.stamps['Golden Sixes Stamp']
    dropRate_Advice[misc].append(Advice(
        label=f"Golden Sixes stamp +{round(goldenSixes_stamp['Value'], 2)}/72.78% (can be increased by Liqorice Rolle Pristine Charm and Exalted Stamps)",
        picture_class='golden-sixes-stamp',
        progression=goldenSixes_stamp['Level'],
        goal=210
    ))

    # Summoning 
    dropRate_Advice[multi].append(Advice(
        label=f"Cotton Candy pristine charm {'1.15x' if cottonCandy_obtained else '0%'} Drop Rate MULTI",
        picture_class='cotton-candy-charm',
        progression=int(session_data.account.sneaking['PristineCharms']['Cotton Candy']['Obtained']),
        goal=1
    ))

    # Sneaking Pristine Charm - Cotton Candy
    cottonCandy_obtained = session_data.account.sneaking['PristineCharms']['Cotton Candy']['Obtained']
    dropRate_Advice[multi].append(Advice(
        label=f"Cotton Candy pristine charm {'1.15x' if cottonCandy_obtained else '0%'} Drop Rate MULTI",
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

    for subgroup in dropRate_Advice:
        for advice in dropRate_Advice[subgroup]:
            mark_advice_completed(advice)

    droprate_AG = AdviceGroup(
        tier="",
        pre_string="Info- Account wide sources of Drop Rate",
        advices=dropRate_Advice,
        informational=True,
    )
    return droprate_AG

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

def getDropRateAdviceSection() -> AdviceSection:
    # Generate AdviceGroups
    droprate_AdviceGroupDict = {}
    droprate_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    droprate_AdviceGroupDict['Account'] = getDropRateAccountAdviceGroup()

    # Generate AdviceSection

    tier_section = f"{overall_SectionTier}/{max_tier}"
    droprate_AdviceSection = AdviceSection(
        name="Drop Rate",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Drop Rate Information",
        picture='wiki/Orion_DR.png',
        groups=droprate_AdviceGroupDict.values(),
        unrated=True,
    )
    return droprate_AdviceSection
