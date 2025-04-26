from models.models import Advice, AdviceGroup, AdviceSection
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data

from utils.text_formatting import notateNumber

logger = get_logger(__name__)

def getCardSetProgress():
    return

def getDropRateAccountAdviceGroup() -> AdviceGroup:
    cards = session_data.account.cards
    bnn_cardset = []
    events_cardset = []
    for card in cards:
        if card.cardset == "Bosses n Nightmares":
            bnn_cardset.append(card)
        if card.cardset == "Events":
            events_cardset.append(card)

    max_card_stars = 5

    cards = "Cards"
    misc = "Miscellaneous"
    dropRate_Advice = {
        cards: [],
        misc: [],
    }
    # Account Wide
    dropRate_Advice[cards].append(Advice(
        label=f"Emperor card: +{12 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Emperor'))}"
              f"/72% Total Drop Rate",
        picture_class="emperor-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Emperor'),
        goal=6
    ))
    dropRate_Advice[cards].append(Advice(
        label=f"W6 Minichief Spirit card: +{8 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Minichief Spirit'))}"
              f"/48% Total Drop Rate",
        picture_class="minichief-spirit-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Minichief Spirit'),
        goal=6
    ))
    dropRate_Advice[cards].append(Advice(
        label=f"King Doot card: +{6 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'King Doot'))}"
              f"/36% Total Drop Rate",
        picture_class="king-doot-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == 'King Doot'),
        goal=6
    ))
    dropRate_Advice[cards].append(Advice(
        label=f"W5 Mister Brightside card: +{6 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Mister Brightside'))}"
              f"/36% Total Drop Rate",
        picture_class="mister-brightside-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Mister Brightside'),
        goal=6
    ))
    dropRate_Advice[cards].append(Advice(
        label=f"W1 Crystal Carrot card: +{5 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Crystal Carrot'))}"
              f"/30% Total Drop Rate",
        picture_class="crystal-carrot-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Crystal Carrot'),
        goal=6
    ))
    dropRate_Advice[cards].append(Advice(
        label=f"W3 Bop Box card: +{3.5 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Bop Box')):g}"
              f"/21% Total Drop Rate",
        picture_class="minichief-spirit-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Bop Box'),
        goal=6
    ))
    dropRate_Advice[cards].append(Advice(
        label=f"Events Mr Blueberry card: +{3 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Mr Blueberry'))}"
              f"/18% Total Drop Rate",
        picture_class="mr-blueberry-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Mr Blueberry'),
        goal=6
    ))
    dropRate_Advice[cards].append(Advice(
        label=f"Events Giftmas Blobulyte card: +{3 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Giftmas Blobulyte'))}"
              f"/18% Total Drop Rate",
        picture_class="giftmas-blobulyte-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Giftmas Blobulyte'),
        goal=6
    ))
    dropRate_Advice[cards].append(Advice(
        label=f"W2 Mimic card: +{3 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Mimic'))}"
              f"/12% Total Drop Rate",
        picture_class="mimic-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Mimic'),
        goal=6
    ))
    dropRate_Advice[cards].append(Advice(
        label=f"Domeo Magmus card: +{1.5 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Domeo Magmus')):g}"
              f"/9% PASSIVE Total Drop Rate",
        picture_class="domeo-magmus-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Domeo Magmus'),
        goal=6
    ))
    
    bnn_stars_sum = sum(min(card.star, max_card_stars) + 1 for card in bnn_cardset)
    bnn_star, _ = divmod(bnn_stars_sum, len(bnn_cardset))
    bnn_star = min(bnn_star, max_card_stars)
    bnn_star_next = (bnn_star + 1) * len(bnn_cardset)
    dropRate_Advice[cards].append(Advice(
        label=f"Bosses n Nightmares card set: +{6 * bnn_star}"
              f"/36% Drop Rate | Cards until next set level {bnn_stars_sum}/{bnn_star_next}",
        picture_class="bosses-n-nightmares",
        progression=bnn_star,
        goal=6
    ))

    events_stars_sum = sum(min(card.star, max_card_stars) + 1 for card in events_cardset)
    events_star, _ = divmod(events_stars_sum, len(events_cardset))
    events_star = min(events_star, max_card_stars)
    events_star_next = (events_star + 1) * len(events_cardset)
    dropRate_Advice[cards].append(Advice(
        label=f"Events card set: +{7 * events_star}"
              f"/42% Drop Rate | Cards until next set level {events_stars_sum}/{events_star_next}",
        picture_class="events",
        progression=events_star,
        goal=6
    ))

    # Misc
    dropRate_Advice[misc].append(Advice(
        label=f"W6 Big Big Hampter achievement +4% Drop Rate",
        picture_class="big-big-hampter",
        progression=1 if session_data.account.achievements["Big Big Hampter"]['Complete'] else 0,
        goal=1
    ))
    dropRate_Advice[misc].append(Advice(
        label=f"W6 Summoning GM achievement +6% Drop Rate",
        picture_class="summoning-gm",
        progression=int(session_data.account.achievements["Summoning GM"]['Complete']),
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

    dropRate_Advice[misc].append(Advice(
        label=f"Alchemy Bubble Droppin Loads +38% Drop Rate",
        picture_class='droppin-loads',
        progression=session_data.account.alchemy_bubbles['Droppin Loads']['Level'],
        goal=1330
    ))

    # TODO: Account wide Drop Rate buffs
    # Caverns: Gloomie Lootie
    # Crop Depot: Science Highlighter
    # Companion: Crystal Custard
    # Equinox: Faux Jewels
    # Beanstalk: Golden Cakes

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
        picture='Auto.png',
        groups=droprate_AdviceGroupDict.values(),
        unrated=True,
    )
    return droprate_AdviceSection
