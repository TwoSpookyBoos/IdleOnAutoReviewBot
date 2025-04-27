from collections import defaultdict
from flask import g as session_data
from consts import break_you_best
from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger

logger = get_logger(__name__)

star_tiers = ["Unlock", "Bronze", "Silver", "Gold", "Platinum", "Ruby"]


def getCardsAdviceSection() -> AdviceSection:
    cards = session_data.account.cards
    unlockable = [card for card in cards if card.star == -1]

    groups = list()

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

    cardsets = defaultdict(list)
    for card in cards:
        cardsets[card.cardset].append(card)

    cardsets = {
        name: sorted(cards, key=lambda card: card.diff_to_next)
        for name, cards in cardsets.items()
    }

    max_card_stars = 5 if session_data.account.rift['RubyCards'] else 4
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

    note = (
        ""
        if session_data.account.rift['RubyCards']
        else (
            "Once you reach Rift 46 your max card tier will be bumped to Ruby. Until then, I will only recommend reaching Platinum rank"
        )
    )

    for group in [g for g in groups if g][3:]:
        group.hide = True

    max_tier = len(cardsets) * (max_card_stars + 1)
    true_max = max_tier
    curr_tier = cardset_rank_total
    tier = f"{curr_tier}/{max_tier}"
    section = AdviceSection(
        name="Cards",
        tier=tier,
        picture="cards/Cards.png",
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"You have reached {tier} cardset tiers. Keep going!",
        groups=groups,
        note=note,
        unrated=True
    )

    if not section:
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
