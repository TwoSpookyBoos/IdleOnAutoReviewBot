from utils.number_formatting import parse_number

# InitializeTrophyBonuses in source. Last update in 2.48 Giftmas Event
podium_multi_by_level = [0.3, 1, 1.5, 2, 2.5]

# InitializeNametagBonuses in source. Last update in v2.48 Giftmas event
nametag_multi_by_level = [parse_number(n) for n in "1,1.6,2,2.3,2.5".split(",")]
