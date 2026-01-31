from collections import defaultdict

from consts.consts_autoreview import break_you_best, ValueToMulti
from consts.consts_general import star_tiers, max_card_stars
from consts.idleon.lava_func import lava_func
from consts.consts_w2 import max_vial_level, obols_max_bonuses_dict
from consts.consts_w3 import approx_max_talent_level_star_talents
from consts.progression_tiers import true_max_tiers
from models.general.session_data import session_data

from models.general.cards import Card
from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.advice.generators.general import get_guild_bonus_advice
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger

logger = get_logger(__name__)


def getUnlockableAdviceGroup(cards, groups):
    unlockable = [card for card in cards if card.star == -1]
    if unlockable:
        advices = defaultdict(list)
        for card in unlockable:
            advices[card.cardset].append(Advice(
                label=f"{card.name}:<br>{card.getFormattedXY()}",
                picture_class=card.css_class,
                completed=False
            ))
        group_unlockable = AdviceGroup(
            tier="",
            pre_string="Discover new cards",
            advices=advices,
            picture_class='locked-card',
            informational=True
        )
        groups.append(group_unlockable)

def getCardDropChanceAdviceGroup(groups):
    # Multi Group B: Cardiovascular

    cardiovascular_id = next(index for index, talent in all_talentsDict.items() if talent['name'] == 'Cardiovascular!')
    cardiovascular_max_level = 100

    cardiovascular_dict_entry = all_talentsDict[cardiovascular_id]
    cardiovascular_bonus = ValueToMulti(lava_func(cardiovascular_dict_entry['funcX'], cardiovascular_max_level, cardiovascular_dict_entry['x1'], cardiovascular_dict_entry['x2']))
    cardiovascular_bonus = round(cardiovascular_bonus, 2)

    multi_group_b = cardiovascular_bonus
    multi_group_b = round(multi_group_b, 2)

    # Multi Group A: all other bonuses
    bribe_bonus = session_data.account.bribes['W2']['Five Aces in the Deck'] * 20

    pokaminni = session_data.account.star_signs['Pokaminni']

    gigafrog: Card = next(card for card in session_data.account.cards if card.name == "Gigafrog")
    snelbie: Card = next(card for card in session_data.account.cards if card.name == "Snelbie")
    sir_stache: Card = next(card for card in session_data.account.cards if card.name == "Sir Stache")
    egggulyte: Card = next(card for card in session_data.account.cards if card.name == "Egggulyte")

    gigafrog_bonus = 5 * gigafrog.level
    snelbie_bonus = 8 * snelbie.level
    sir_stache_bonus = 9 * sir_stache.level
    egggulyte_bonus = 1 * egggulyte.level

    anearful_vial = session_data.account.alchemy_vials['Anearful (Glublin Ear)']
    anearful_vial_bonus = anearful_vial['Value']

    card_stamp = session_data.account.stamps['Card Stamp']
    card_stamp_bonus = card_stamp.total_value

    # JMAN ONLY
    cards_galore_talent = all_talentsDict[28]
    cards_galore_talent_bonus = lava_func(cards_galore_talent['funcX'], approx_max_talent_level_star_talents, cards_galore_talent['x1'], cards_galore_talent['x2'])

    guild_bonus = session_data.account.guild_bonuses['C2 Card Spotter']
    guild_bonus_bonus = guild_bonus['Value']

    max_obol_card_drop_chance = obols_max_bonuses_dict["PlayerCardDropChanceTrue"] + obols_max_bonuses_dict["FamilyCardDropChanceTrue"]
    max_8ball_keychain_card_drop_chance = 2 * 10
    max_equipment_card_drop_chance_bonus = max_obol_card_drop_chance + max_8ball_keychain_card_drop_chance

    card_champ_bubble = session_data.account.alchemy_bubbles['Card Champ']
    card_champ_bubble_bonus = card_champ_bubble['BaseValue']

    multi_group_a = (
            bribe_bonus +
            int(pokaminni['Unlocked']) * 15 +
            gigafrog_bonus + snelbie_bonus + sir_stache_bonus + egggulyte_bonus +
            anearful_vial_bonus +
            card_stamp_bonus +
            guild_bonus_bonus +
            max_equipment_card_drop_chance_bonus +
            card_champ_bubble_bonus
    ) / 100

    multi_group_a_jman = (
            bribe_bonus +
            int(pokaminni['Unlocked']) * 15 +
            gigafrog_bonus + snelbie_bonus + sir_stache_bonus + egggulyte_bonus +
            anearful_vial_bonus +
            card_stamp_bonus +
            cards_galore_talent_bonus +
            guild_bonus_bonus +
            max_equipment_card_drop_chance_bonus +
            card_champ_bubble_bonus
    ) / 100

    multi_group_a = round(multi_group_a, 2)
    multi_group_a_jman = round(multi_group_a_jman, 2)

    # Total

    multi_total = round(0.2 + multi_group_a * multi_group_b, 2)
    multi_total_jman = round(0.2 + multi_group_a_jman * multi_group_b, 2)

    card_drop_chance_advices = {
        f'Total: {multi_total}x ({multi_total_jman}x if Jman)': [
            Advice(
                label=f'Total Card Drop Chance bonus: {multi_total}x ({multi_total_jman}x if Jman)',
                picture_class='dementia-obol-of-cards',
            )
        ],
        f'Base Chance: +20%': [
            Advice(
                label="Passive +20% bonus. Not multiplied by other Multi Groups",
                picture_class=""
            )
        ],
        f'Multi Group A: {multi_group_a}x ({multi_group_a_jman}x if Jman)': [],
        f'Multi Group A - account-wide': [
            Advice(
                label=f"{{{{ Bribe|#bribes }}}}: Five Aces in the Deck: "
                      f"+{bribe_bonus}/20%",
                picture_class='bottomless-bags',
                progression=1 if session_data.account.bribes['W4']['Bottomless Bags'] >= 1 else 0,
                goal=1
            ),
            Advice(
                label=f"{{{{ Vial|#vials }}}}: Anearful: +{anearful_vial['Value']:.2f}%",
                picture_class='glublin-ear',
                progression=anearful_vial['Level'],
                goal=max_vial_level
            ),
            session_data.account.stamps['Card Stamp'].get_advice(),
            Advice(
                label=f"{{{{ Alchemy Bubbles|#bubbles }}}} - Card Champ: +{card_champ_bubble['BaseValue']:.2f}/100%",
                picture_class='card-champ',
                resource=card_champ_bubble['Material'],
                progression=card_champ_bubble['Level'],
                goal=3960
            ),
            get_guild_bonus_advice('C2 Card Spotter')
        ],
        f'Multi Group A - character-specific': [
            gigafrog.getAdvice(),
            snelbie.getAdvice(),
            sir_stache.getAdvice(),
            egggulyte.getAdvice(),
            Advice(
                label=f"{{{{ Star Signs|#star-signs }}}} - Pokaminni: {'+15% if equipped' if pokaminni['Unlocked'] else 'Locked.'}",
                picture_class='pokaminni',
                progression=int(pokaminni['Unlocked']),
                goal=1
            ),
            Advice(
                label=f'Full Card Drop Chance Obols: +{max_obol_card_drop_chance}%'
                      f'<br>Both personal and family, all rerolled for +1% Card Drop Chance',
                picture_class="dementia-obol-of-cards"
            ),
            Advice(
                label=f'2x 8 Ball Keychains: 2x +10%',
                picture_class="x8-ball-chain"
            )
        ],
        f'Multi Group A - class-specific': [
            Advice(
                label=f"Cards Galore Talent: +{cards_galore_talent_bonus:.2f}% if maxed (Jman only)",
                picture_class="cards-galore",
            )
        ],
        f'Multi Group B: {multi_group_b}x (character-specific)': [
            Advice(
                label=f'Star Talent "Cardiovascular!": {cardiovascular_bonus}x if maxed',
                picture_class="cardiovascular",
            )
        ],
    }

    for subgroup in card_drop_chance_advices:
        for advice in card_drop_chance_advices[subgroup]:
            advice.mark_advice_completed()

    groups.append(AdviceGroup(
        tier="",
        pre_string="Sources of Card Drop Chance",
        advices=card_drop_chance_advices,
        picture_class="dementia-obol-of-cards",
        informational=True
    ))

def getCardsetAdviceGroups(cardsets, max_card_stars, groups):
    cardset_rank_total = 0
    for name, cardset in cardsets.items():
        cardset_stars_sum = sum(min(card.star, max_card_stars) + 1 for card in cardset)
        cardset_star, cardset_diff = divmod(cardset_stars_sum, len(cardset))
        cardset_star = min(cardset_star, max_card_stars)
        cardset_star_next = (cardset_star + 1) * len(cardset)
        cardset_maxed = cardset_stars_sum == cardset_star_next  #96/96 Blunder Hills, for instance

        cardset_rank_total += cardset_star + cardset_maxed
        #logger.debug(f"{name} at {cardset_stars_sum}/{cardset_star_next} toward {star_tiers[cardset_star]} is worth {cardset_star + cardset_maxed} total cardset tiers")

        advices = [
            Advice(
                label=f"{card.name}:<br>{card.getFormattedXY()}",
                picture_class=card.css_class,
                progression=f"{card.diff_to_next:,}",
                goal=star_tiers[card.star + 1]
            ) for card in cardset if -1 < card.star < max_card_stars
        ]
        group = AdviceGroup(
            tier="",
            pre_string=f"{name}: Collect {len(cardset) - cardset_diff} more cards for {star_tiers[cardset_star]} ({cardset_stars_sum}/{cardset_star_next})",
            picture_class=name,
            advices=advices,
            informational=True
        )
        groups.append(group)
    return cardset_rank_total


def getCardsAdviceSection() -> AdviceSection:
    cards = session_data.account.cards
    cardsets = defaultdict(list)
    for card in cards:
        cardsets[card.cardset].append(card)

    cardsets = {
        name: sorted(cards, key=lambda card: card.diff_to_next)
        for name, cards in cardsets.items()
    }

    player_max_card_stars = (
        4
        + (1 * session_data.account.rift['RubyCards'])
        + (1 * session_data.account.spelunk.cave["Rustbelt 03"].bonus_obtained)
    )

    groups = list()

    getUnlockableAdviceGroup(cards, groups)
    getCardDropChanceAdviceGroup(groups)
    cardset_rank_total = getCardsetAdviceGroups(cardsets, player_max_card_stars, groups)

    note = (
        '' if player_max_card_stars == max_card_stars
        else 'Majestic star locked: Only recommending reaching Ruby star' if player_max_card_stars == max_card_stars - 1
        else 'Ruby star locked: Only recommending reaching Platinum star'
    )

    for group in [g for g in groups if g][3:]:
        group.hide = True

    max_tier = len(cardsets) * (player_max_card_stars + 1)
    true_max = true_max_tiers['Cards']
    curr_tier = cardset_rank_total
    overall_SectionTier = 0
    tier = f"{curr_tier}/{max_tier}"
    section = AdviceSection(
        name='Cards',
        tier=tier,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f'You have reached {tier} cardset tiers. Keep going!',
        picture='cards/Cards.png',
        groups=groups,
        note=note,
        unrated=True
    )

    if not section:  #If there are no AdviceGroups
        if not session_data.account.rift['RubyCards']:
            section.tier = f"{max_tier}/{max_tier}"
            section.header = (
                f"You have completed all {section.tier} cardset tiers. But... "
                f"I'll see your Diamonds and raise you Rubies! Come back once you reach Rift 46."
            )
        else:
            section.tier = f"{max_tier}/{max_tier}"
            section.header = (
                f"You have completed all {section.tier} cardset tiers. Too rich "
                f"for my blood, I fold. Your sleight of hand is admirable. ♥️♠️♦️♣️"
                f"{break_you_best}"
            )

    return section
