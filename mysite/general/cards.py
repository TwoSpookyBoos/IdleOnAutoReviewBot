from collections import defaultdict

from flask import g as session_data

from models.models import AdviceSection, AdviceGroup, Advice

star_tiers = ["Unlock", "Bronze", "Silver", "Gold", "Platinum", "Ruby"]


def getCardSetReview():
    cards = session_data.account.cards
    unlockable = [card for card in cards if card.star == -1]

    groups = list()

    if unlockable:
        advices = defaultdict(list)
        for card in unlockable:
            advices[card.cardset].append(
                Advice(label=card.name, picture_class=card.css_class)
            )
        group_unlockable = AdviceGroup(
            tier="", pre_string="Discover new cards", advices=advices, picture_class='locked-card',
        )
        groups.append(group_unlockable)

    cardsets = defaultdict(list)
    for card in cards:
        cardsets[card.cardset].append(card)

    cardsets = {
        name: sorted(cards, key=lambda card: card.diff_to_next)
        for name, cards in cardsets.items()
    }

    max_card_rank = 5 if session_data.account.ruby_cards_unlocked else 4
    cardset_rank_total = 0

    for name, cardset in cardsets.items():
        cardset_stars_sum = sum(min(card.star, max_card_rank) + 1 for card in cardset)
        cardset_star, cardset_diff = divmod(cardset_stars_sum, len(cardset))
        cardset_star = min(cardset_star, max_card_rank)
        cardset_star_next = (cardset_star + 1) * len(cardset)

        cardset_rank_total += cardset_star

        advices = [
            Advice(label=card.name, picture_class=card.css_class, progression=f"{card.diff_to_next:,}", goal=star_tiers[card.star + 1])
            for card in cardset
            if -1 < card.star < max_card_rank
        ]
        group = AdviceGroup(
            tier="",
            pre_string=f"{name}: Collect {len(cardset) - cardset_diff} more cards for {star_tiers[cardset_star]} ({cardset_stars_sum}/{cardset_star_next})",
            picture_class=name,
            advices=advices,
        )
        groups.append(group)

    note = (
        ""
        if session_data.account.ruby_cards_unlocked
        else (
            "Once you reach Rift 46 your max card tier will be bumped to Ruby. Until then, I will only recommend reaching Platinum rank"
        )
    )

    for group in [g for g in groups if g][3:]:
        group.hide = True

    max_tier = len(cardsets) * (max_card_rank + 1)
    curr_tier = cardset_rank_total
    tier = f"{curr_tier}/{max_tier}"
    section = AdviceSection(
        name="Cards",
        tier=tier,
        picture="cards/Cards.png",
        header=f"You have reached {tier} cardset tiers. Keep going!",
        groups=groups,
        note=note,
    )

    if not section:
        if not session_data.account.ruby_cards_unlocked:
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
            )

    return section
