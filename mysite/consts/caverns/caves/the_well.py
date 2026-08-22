from consts.idleon.caverns.cavern import HolesInfo

schematics_unlocking_buckets = [
    "2nd Bucket!",
    "3rd Bucket!",
    "4th Bucket!",
    "Five Nights at Bucket",
    "6th Bucket!",
    "7rth Barckot?!",
    "Last Bucket!",
    "9th Bucket!",
    "Bucket Finale!",
]
max_buckets = 1 + len(schematics_unlocking_buckets)

sediment_names = [
    "Gravel",
    "Goldust",
    "Redstone",
    "Mythril",
    "Cobaltine",
    "Brunite",
    "Freezium",
    "Sweetium",
    "Rad Coral",
    "Hyper Coral",
]
sediment_bars = [int(float(v)) for v in HolesInfo[21]]
max_sediments = len(sediment_names)
