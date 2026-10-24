from consts.idleon.consts_idleon import RANDOlist
from consts.idleon.general.dungeons import DungPassiveStats, DungPassiveStats2
from utils.number_formatting import parse_number

dungeon_credit_shop_names = [stat[0].replace('@', ' ') for stat in DungPassiveStats]
dungeon_flurbo_shop_names = [stat[0].replace('@', ' ') for stat in DungPassiveStats2]

# Purchase caps in the Dungeon shop UI in source. Last updated in v2.531.0
max_credit_shop_level = 100
max_flurbo_shop_level = 50

# Rank is the index of the first entry above your lifetime Dungeon Credits
dungeon_rank_credit_requirements = [parse_number(requirement) for requirement in RANDOlist[29]]
