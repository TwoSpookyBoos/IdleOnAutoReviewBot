"""Companion bonuses the game keeps only in description text.

`CompanionDB` holds one number per tier, so extra bonuses live in the description. Everything a
companion grants beyond that single number lives here, one entry per companion, with the consuming
formula from the game source quoted above it.

`Companions(i)` is the raw field 2 / field 11 number, so a formula's own `1 +` is what turns it into
a multi. Only companions whose formula transforms that number need an entry - where `Value` already
IS the bonus, nothing is listed, because the array is the better source.

Each stat is `(form, base, upgraded)`. A 'multi' reads 1.0 when absent or unowned, a 'value' reads 0.
Base values are what the game computes. The '+' halves follow the description instead, because most
Pet Mart+ variants aren't earnable yet and field 11 is provisional - a comment marks each one that
currently computes something different, to be revisited as they release.

Ordered by companion Id.
"""

companion_bonuses = {
    # a constant per pachinko payout (3/6/12/75/200/500/3000), working out to 25-33%. Advertised +25%
    'Slime': {'Gold Balls': ('multi', 1.25, 1.50)},
    # `1 + 2 * Companions(13)` computes 3.68x, desc says 4x. `25 * Companions(13)` for the opals,
    # which computes 33.5 against a desc of +33
    'Samurai Guardian': {
        'Villager EXP': ('multi', 3.0, 4.0),
        'Opals': ('value', 25.0, 33.0),
    },
    # `min(1.3, 1 + Companions(26))` - the cap currently holds the '+' at 1.30x, desc says 1.50x
    'Mallay': {'Drop Rate': ('multi', 1.30, 1.50)},
    # `FriendBonusXtraMulti`: `1 + 100 * Companions(30) / 100`
    'Mr Pig': {'Friend Bonuses': ('multi', 2.0, 2.5)},
    # `1 + Companions(32)`
    'Whale': {'Class EXP': ('multi', 2.0, 2.5), 'Skill EXP': ('multi', 2.0, 2.5)},
    # `1 + Companions(33)`
    'Chippy': {'Total Damage': ('multi', 2.0, 2.5), 'Class EXP': ('multi', 2.0, 2.5)},
    # `1 + 9 * Companions(37)` computes 14.5x, desc says 15x. `10 * Companions(37)` for the PTS
    'Whallamus': {
        'Class EXP': ('multi', 10.0, 15.0),
        'Legend Talent PTS': ('value', 10.0, 15.0),
    },
    # `CoinDropMulti` and `AllMasterclassDropz`: `1 + Companions(38)`
    'Balloonfish': {'Coins': ('multi', 4.0, 6.0), 'Masterclass Drops': ('multi', 4.0, 6.0)},
    # `min(1.01, 1 + Companions(50) / 2500)` - the cap holds the '+' at 1.01x
    'Santa Snake': {'Class EXP': ('multi', 1.01, 1.01), 'Drop Rate': ('multi', 1.01, 1.01)},
    # `max(.01, 1 - Companions(57) / 100)` on Glimbo_Cost, a divisor. f11 computes 15.02x
    'Dreadnaught Captain': {'Swap Meet Cost': ('multi', 5.0, 15.0)},
    # `1 + 2 * Companions(87)`, and `5 * Companions(87)` for the PTS, which computes 7.5 vs a desc of +7
    'Rift Spooker': {
        'Cooking Mastery EXP': ('multi', 3.0, 4.0),
        'Cooking Mastery PTS': ('value', 5.0, 7.0),
    },
    # `PrismaBonusMult`: `50 * Companions(88)` into a `/100` pool
    'Rift Hivemind': {'Prisma Bubble Bonus': ('multi', 1.50, 1.75)},
    # `1 + (min(.5, Companions(128)) + .25 * CompLV2(128))`
    'Baby Troll': {'Class EXP': ('multi', 1.50, 1.75)},
    # `1 + (min(.5, Companions(132)) + .2 * CompLV2(132))`
    'Mama Troll': {'Drop Rate': ('multi', 1.50, 1.70)},
    # `max(1, Companions(143))` and `max(1, min(2, Companions(143)) + CompLV2(143))`
    'Boomy Mine': {
        'Spelunking POW': ('multi', 20.0, 30.0),
        'Minehead Currency': ('multi', 2.0, 3.0),
    },
    # `ResearchEXPmulti`: `1 + Companions(153) + CompLV2(153)`. The AFK and PTS terms are
    # `20 * Companions(153) + 10 * CompLV2(153)` and `10 * Companions(153) + 5 * CompLV2(153)`
    'Rift Stalker': {
        'Research EXP': ('multi', 2.0, 3.0),
        'Research AFK Gains': ('value', 20.0, 30.0),
        'Research PTS': ('value', 10.0, 15.0),
    },
    # `KillPerKill`: `1 + Companions(154)`. `BoatArtiMulti`: `max(1, min(2, 1 + 2 * C(154)) + CompLV2(154))`
    'Glimbo': {'Kills': ('multi', 1.60, 2.0), 'Artifact Find': ('multi', 2.0, 3.0)},
    # `1 + n * Companions(160)`, but f11 is untuned and equals f2, so the game computes base twice.
    # Using the advertised '+' numbers on the assumption Lava fills field 11 in
    'Glunko The Massive': {
        'Total Damage': ('multi', 3.0, 5.0),
        'Class EXP': ('multi', 5.0, 9.0),
        'Drop Rate': ('multi', 1.50, 2.0),
    },
    # `max(1, 5 * Companions(162))` and `1 + 25 * Companions(162) / 100`
    'Wickerlight Spirit': {'Meal Cost': ('multi', 5.0, 8.0), 'Meal Bonus': ('multi', 1.25, 1.40)},
    # `1 + n * Companions(163)` computes 149.5x / 59.5x, desc says 150x / 60x
    'Smoke Devil': {
        'Jade Gain': ('multi', 100.0, 150.0),
        'Ninja Stealth': ('multi', 40.0, 60.0),
        'Sneaking EXP': ('multi', 2.50, 3.25),
    },
    # `1 + n * Companions(168)`
    'Crystal Glunko': {
        'Total Damage': ('multi', 1.50, 1.75),
        'Class EXP': ('multi', 1.40, 1.60),
        'Drop Rate': ('multi', 1.30, 1.45),
        'Extra Kills': ('multi', 1.20, 1.30),
    },
    # `1 + (SecretSetBonus + 50 * Companions(174)) / 100`, and `1e4 * Companions(174)` for the additive
    'Verminous': {
        'Gold Food': ('multi', 1.50, 2.0),
        'Gold Food Effect': ('value', 10000.0, 20000.0),
    },
}

# Deliberately absent, both checked against the source so nobody re-hunts them:
#   Rift Hivemind (88) the +5/+7 Prisma Bubbles is a one-time grant already saved in the file
#   Bin Goosey (169)   ribbon tiers are a dice roll, no fixed bonus to report

# Extra `_customBlock_CompLV2` term when upgraded, on top of the field 2 -> 11 swap. By id.
complv2_companion_ids = (0, 2, 28, 44, 54, 88, 128, 132, 143, 153, 154, 169)
