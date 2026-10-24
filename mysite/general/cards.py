from collections import defaultdict

from consts.consts_autoreview import break_you_best
from consts.consts_general import star_tiers, max_card_stars
from consts.general.cards import card_champ_bubble_goal
from consts.progression_tiers import true_max_tiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
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
    cards = session_data.account.cards
    five_aces = session_data.account.bribes['Five Aces in the Deck']
    anearful_vial = session_data.account.alchemy_vials['Anearful (Glublin Ear)']
    guild_bonus = session_data.account.guild_bonuses['C2 Card Spotter']
    card_champ_bubble = session_data.account.alchemy_bubbles['Card Champ']

    card_drop_chance_advices = {
        f'Total: {cards.drop_chance}x ({cards.drop_chance_jman}x if Jman)': [
            cards.get_drop_chance_advice()
        ],
        f'Base Chance: +20%': [cards.get_base_drop_chance_advice()],
        f'Multi Group A: {cards.drop_chance_multi_a}x ({cards.drop_chance_multi_a_jman}x if Jman)': [],
        f'Multi Group A - account-wide': [
            five_aces.get_bonus_advice(),
            anearful_vial.get_advice(full_name=False),
            session_data.account.stamps['Card Stamp'].get_advice(),
            card_champ_bubble.get_bonus_advice(goal=card_champ_bubble_goal),
            guild_bonus.get_advice()
        ],
        f'Multi Group A - character-specific': [
            cards.named('Gigafrog').getAdvice(),
            cards.named('Snelbie').getAdvice(),
            cards.named('Sir Stache').getAdvice(),
            cards.named('Egggulyte').getAdvice(),
            cards.get_pokaminni_advice(),
            cards.get_obols_advice(),
            cards.get_keychains_advice(),
        ],
        f'Multi Group A - class-specific': [cards.get_cards_galore_advice()],
        f'Multi Group B: {cards.drop_chance_multi_b}x (character-specific)': [
            cards.get_cardiovascular_advice()
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

def getCardsetAdviceGroups(cards, groups):
    for name, cardset in cards.cardsets.items():
        progress = cards.cardset_progress[name]
        advices = [
            Advice(
                label=f"{card.name}:<br>{card.getFormattedXY()}",
                picture_class=card.css_class,
                progression=f"{card.diff_to_next:,}",
                goal=star_tiers[card.star + 1]
            ) for card in cardset if -1 < card.star < cards.player_max_card_stars
        ]
        group = AdviceGroup(
            tier="",
            pre_string=f"{name}: Collect {len(cardset) - progress.stars_over} more cards for {star_tiers[progress.star]} ({progress.stars_sum}/{progress.next_star_sum})",
            picture_class=name,
            advices=advices,
            informational=True
        )
        groups.append(group)


def getCardsAdviceSection() -> AdviceSection:
    cards = session_data.account.cards
    player_max_card_stars = cards.player_max_card_stars

    groups = list()

    getUnlockableAdviceGroup(cards, groups)
    getCardDropChanceAdviceGroup(groups)
    getCardsetAdviceGroups(cards, groups)

    note = (
        '' if player_max_card_stars == max_card_stars
        else 'Majestic star locked: Only recommending reaching Ruby star' if player_max_card_stars == max_card_stars - 1
        else 'Ruby star locked: Only recommending reaching Platinum star'
    )

    for group in [g for g in groups if g][3:]:
        group.hide = True

    max_tier = len(cards.cardsets) * (player_max_card_stars + 1)
    true_max = true_max_tiers['Cards']
    curr_tier = cards.cardset_rank_total
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
        if not session_data.account.rift['RubyCards'].unlocked:
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
