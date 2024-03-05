import json
from collections import defaultdict

from flask import g as session_data

from models import AdviceSection, AdviceGroup, Advice


card_tiers = ["Unlock", "Bronze", "Silver", "Gold", "Platinum", "Ruby"]


def getCardSetReview():
    cards = session_data.data.cards
    unlockable = [card for card in cards if card.star == -1]

    groups = list()

    if unlockable:
        advices = defaultdict(list)
        for card in unlockable:
            advices[card.cardset].append(
                Advice(
                    label=card.name,
                    item_name=card.css_class,
                )
            )
        group_unlockable = AdviceGroup(
            tier="0", pre_string="Unlock cards", advices=advices
        )
        groups.append(group_unlockable)

    cardsets = defaultdict(list)
    for card in cards:
        cardsets[card.cardset].append(card)

    cardsets = {
        name: sorted(cards, key=lambda card: card.diff_to_next)
        for name, cards in cardsets.items()
    }

    for name, cardset in cardsets.items():
        cardset_stars_sum = sum(card.star + 1 for card in cardset)
        cardset_star, cardset_diff = divmod(cardset_stars_sum, len(cardset))
        cardset_star_next = (cardset_star + 1) * len(cardset)

        advices = [
            Advice(
                label=card.name,
                item_name=card.css_class,
                progression=card.diff_to_next,
                goal=card_tiers[card.star + 1]
            )
            for card in cardset if -1 < card.star < 5
        ]
        group = AdviceGroup(
            tier="",
            pre_string=f"{name}: Collect {len(cardset) - cardset_diff} more cards for {card_tiers[cardset_star]} ({cardset_stars_sum}/{cardset_star_next})",
            advices=advices
        )
        groups.append(group)

    section = AdviceSection(
        name="Cards",
        tier="",
        header="Get more cards",
        groups=groups
    )

    return section
