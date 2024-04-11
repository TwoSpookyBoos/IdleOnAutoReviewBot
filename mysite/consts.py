from utils.logging import get_logger


logger = get_logger(__name__)

###WORLD 1 PROGRESSION TIERS###
bribes_progressionTiers = [
        #int tier, int w1purchased, int w2purchased, int w3purchased, int w4purchased, int trashIslandpurchased, int w6purchased
        [0, 0, -7, -7, -6, -7, -8],
        [1, 6, -7, -7, -6, -7, -8],
        [2, 6, 7, -7, -6, -7, -8],
        [3, 6, 7, 7, -6, -7, -8],
        [4, 6, 7, 7, 6, -7, -8],
        [5, 6, 7, 7, 6, 7, -8],  #The 8th bribe in w5 cannot be purchased until Jade Emporium
        [6, 6, 7, 7, 6, 7, 7, ]  #The 7th bribe in w6 can't be purchased yet
]
stamps_progressionTiers = [
    # int Tier, int Total Stamp Level, str Required combat stamps, str Required Skill stamps, str Required Misc stamps, dict Specific stamp levels, str Notes
    [0, 0, [], [], [], {}, "Just level up any stamp you can afford!"],
    [1, 50, [], [], [], {}, "Just level up any stamp you can afford!"],
    [2, 100, [], [], [], {}, "Just level up any stamp you can afford!"],
    [3, 150, [2, 3, 4, 5, 11], [5], [10], {}, "W1 town and W1 Tiki shop both sell stamps!"],
    [4, 200, [8, 13, 14], [3, 16, 18], [17], {},
     "Expected progression roughly near the start of World 3. Some of these required stamps are drops from enemies or quest rewards. Use the Wiki to find their sources!"],
    [5, 250, [6, 7, 9], [2, 7], [0], {'Pickaxe Stamp': 25, 'Hatchet Stamp': 25}, ""],
    [6, 300, [17, 18, 20], [25], [5], {}, ""],
    [7, 400, [], [8], [], {'Pickaxe Stamp': 35, 'Hatchet Stamp': 35}, ""],
    [8, 500, [15, 16, 21], [14, 17], [14, 19], {'Drippy Drop Stamp': 30}, ""],
    [9, 600, [27], [10], [1, 2], {'Mason Jar Stamp': 12}, ""],
    [10, 700, [], [4, 6, 9, 11, 12, 15, 22, 24, 26], [], {'Drippy Drop Stamp': 40, 'Matty Bag Stamp': 50}, ""],
    [11, 800, [], [29, 37, 40], [11], {'Pickaxe Stamp': 45, 'Hatchet Stamp': 45, 'Mason Jar Stamp': 24, }, ""],
    [12, 900, [], [13, 20, 30, 46], [8], {'Drippy Drop Stamp': 50}, ""],
    [13, 1000, [10, 12], [19, 21, 36], [13], {'Pickaxe Stamp': 55, 'Hatchet Stamp': 55, 'Card Stamp': 50}, ""],
    [14, 1500, [23, 24], [35, 39], [21], {'Matty Bag Stamp': 100, 'Crystallin': 60}, ""],
    [15, 2000, [28], [41], [6, 20], {'Pickaxe Stamp': 65, 'Hatchet Stamp': 65, 'Card Stamp': 100}, ""],
    [16, 2500, [31], [38, 42], [15], {'Golden Apple Stamp': 28}, ""],
    [17, 3000, [25, 29], [43, 44, 45], [], {'Bugsack Stamp': 80, 'Bag o Heads Stamp': 80}, ""],
    [18, 3500, [33], [], [], {'Pickaxe Stamp': 75, 'Hatchet Stamp': 75, 'Drippy Drop Stamp': 90, 'Crystallin': 100}, ""],
    [19, 4000, [], [], [], {'Matty Bag Stamp': 150}, ""],
    [20, 4500, [39], [47], [18], {'Card Stamp': 150, 'Ladle Stamp': 100, 'Potion Stamp': 20}, ""],
    [21, 5000, [30, 32], [23], [], {'Pickaxe Stamp': 85, 'Hatchet Stamp': 85, 'Mason Jar Stamp': 52, 'Golden Apple Stamp': 40}, ""],
    [22, 5500, [], [], [], {'Bugsack Stamp': 120, 'Bag o Heads Stamp': 120}, ""],
    [23, 6000, [19, 26, 34], [33], [], {'Matty Bag Stamp': 200, 'Crystallin': 150}, ""],
    [24, 6500, [36], [48, 49, 51], [9], {'Drippy Drop Stamp': 100, 'Ladle Stamp': 150, 'Potion Stamp': 40}, ""],
    [25, 7000, [35], [], [], {'Pickaxe Stamp': 95, 'Hatchet Stamp': 95, 'Golden Apple Stamp': 60, 'Multitool Stamp': 100}, ""],
    [26, 7500, [], [], [], {'Ladle Stamp': 180}, ""],
    [27, 8000, [], [], [], {'Matty Bag Stamp': 280, 'Multitool Stamp': 150}, ""],
    [28, 8400, [], [53], [22],
     {'Pickaxe Stamp': 105, 'Hatchet Stamp': 105, 'Mason Jar Stamp': 80, 'Crystallin': 200, 'Bugsack Stamp': 144, 'Bag o Heads Stamp': 144, }, ""],
    [29, 8800, [], [], [], {'Drippy Drop Stamp': 110, 'Potion Stamp': 60}, ""],
    [30, 9200, [], [], [], {'Card Stamp': 200, 'Crystallin': 250}, ""],
    [31, 9600, [], [], [], {'Golden Apple Stamp': 80}, "Guaranteed daily Gilded Stamp at 10k"],
    [32, 10000, [], [], [], {'Mason Jar Stamp': 100}, ""],
    [33, 10500, [], [], [], {'Bugsack Stamp': 168, 'Bag o Heads Stamp': 168}, ""],
    [34, 11000, [], [], [], {'Golden Apple Stamp': 100, 'Multitool Stamp': 210}, ""],
    [35, 11500, [37], [], [], {'Golden Sixes Stamp': 120}, ""],
    [36, 12000, [38], [31], [], {'Maxo Slappo Stamp': 98, 'Sashe Sidestamp': 98, 'Intellectostampo': 98}, ""],
    [37, 12500, [], [], [], {'Ladle Stamp': 270}, ""],
    [38, 13000, [40, 22], [52, 50], [], {'Triad Essence Stamp': 80}, ""],
]
smithing_progressionTiers = [
    # int tier, int Cash Points Purchased, int Monster Points Purchased, int Forge Totals, str Notes
    [0, 0, 0, 0, ""],
    [1, 20, 85, 60, "all W1 enemies"],
    [2, 60, 150, 120, "early W2 enemies through Pincermin"],
    [3, 100, 225, 180, "all W2 enemies"],
    [4, 150, 350, 240, "most W3 enemies, excluding Dedotated Rams"],
    [5, 200, 500, 291, "early W4 enemies through Soda Cans"],
    [6, 600, 700, 291, "all W4 enemies"]
]

###WORLD 2 PROGRESSION TIERS###
bubbles_progressionTiers = [
    # int tier, int TotalBubblesUnlocked,
    # dict {OrangeSampleBubbles},
    # dict {GreenSampleBubbles},
    # dict {PurpleSampleBubbles},
    # dict {UtilityBubbles},
    # str BubbleValuePercentage,
    # str Notes
    [0, 0, {}, {}, {}, {}, "0%", ""],
    [1, 10,
     {'Roid Ragin': 12, 'Warriors Rule': 6, 'Hearty Diggy': 12, 'Wyoming Blood': 6, 'Sploosh Sploosh': 6, 'Stronk Tools': 8},
     {'Swift Steppin': 12, 'Archer or Bust': 6, 'Sanic Tools': 8, 'Bug^2': 6},
     {'Stable Jenius': 12, 'Mage is Best': 6, 'Hocus Choppus': 12, 'Molto Loggo': 6, 'Le Brain Tools': 8},
     {'FMJ': 5, 'Shaquracy': 5, 'Prowesessary': 7, 'Hammer Hammer': 6},
     "10%",
     "MINIMUM recommended Utility bubbles for finishing W2. Prowess hard-caps at 2x."],
    [2, 20,
     {'Roid Ragin': 25, 'Warriors Rule': 13, 'Hearty Diggy': 25, 'Wyoming Blood': 13, 'Sploosh Sploosh': 13, 'Stronk Tools': 18},
     {'Swift Steppin': 25, 'Archer or Bust': 13, 'Sanic Tools': 18, 'Bug^2': 13},
     {'Stable Jenius': 25, 'Mage is Best': 13, 'Hocus Choppus': 25, 'Molto Loggo': 13, 'Le Brain Tools': 18},
     {'FMJ': 10, 'Shaquracy': 10, 'Prowesessary': 15, 'Hammer Hammer': 14, 'All for Kill': 25},
     "20%",
     "MINIMUM recommended Utility bubbles for starting W3. Prowess hard-caps at 2x."],
    [3, 40,
     {'Roid Ragin': 67, 'Warriors Rule': 34, 'Hearty Diggy': 67, 'Wyoming Blood': 20, 'Sploosh Sploosh': 20, 'Stronk Tools': 47},
     {'Swift Steppin': 67, 'Archer or Bust': 34, 'Sanic Tools': 47, 'Bug^2': 20},
     {'Stable Jenius': 67, 'Mage is Best': 34, 'Hocus Choppus': 67, 'Molto Loggo': 20, 'Le Brain Tools': 47},
     {'FMJ': 15, 'Shaquracy': 15, 'Prowesessary': 40, 'Hammer Hammer': 41, 'All for Kill': 67},
     "40%",
     "MINIMUM recommended Utility bubbles for starting W4. Prowess hard-caps at 2x."],
    [4, 60,
     {'Roid Ragin': 100, 'Warriors Rule': 50, 'Hearty Diggy': 100, 'Wyoming Blood': 30, 'Sploosh Sploosh': 30, 'Stronk Tools': 70},
     {'Swift Steppin': 100, 'Archer or Bust': 50, 'Sanic Tools': 70, 'Bug^2': 30},
     {'Stable Jenius': 100, 'Mage is Best': 50, 'Hocus Choppus': 100, 'Molto Loggo': 30, 'Le Brain Tools': 70},
     {'FMJ': 20, 'Shaquracy': 20, 'Prowesessary': 60, 'Hammer Hammer': 65, 'All for Kill': 100},
     "50%",
     "MINIMUM recommended Utility bubbles for starting W5. Prowess hard-caps at 2x, which you should be reaching now!"],
    [5, 80,
     {'Roid Ragin': 150, 'Warriors Rule': 75, 'Hearty Diggy': 150, 'Wyoming Blood': 45, 'Sploosh Sploosh': 45, 'Stronk Tools': 105, 'Multorange': 45},
     {'Swift Steppin': 150, 'Archer or Bust': 75, 'Bug^2': 45, 'Premigreen': 45, },
     {'Stable Jenius': 150, 'Mage is Best': 75, 'Molto Loggo': 45, 'Le Brain Tools': 105, 'Severapurple': 45, },
     {'FMJ': 30, 'Shaquracy': 30, 'Hammer Hammer': 105, 'All for Kill': 150},
     "60%",
     "MINIMUM recommended Utility bubbles for starting W6 push. Keep watch of your No Bubble Left Behind list (from W4 Lab) to keep cheap/easy bubbles off when possible!"],
    [6, 100,
     {'Roid Ragin': 234, 'Warriors Rule': 117, 'Hearty Diggy': 234, 'Wyoming Blood': 70, 'Sploosh Sploosh': 70, 'Stronk Tools': 164, 'Multorange': 70,
      'Dream of Ironfish': 70},
     {'Swift Steppin': 234, 'Archer or Bust': 117, 'Bug^2': 70, 'Premigreen': 70, 'Fly in Mind': 94},
     {'Stable Jenius': 234, 'Mage is Best': 117, 'Molto Loggo': 70, 'Le Brain Tools': 164, 'Severapurple': 70, 'Tree Sleeper': 94},
     {'Cookin Roadkill': 105, 'All for Kill': 167},
     "70%",
     "Cookin Roadkill 105 = 60% bubble strength. All for Kill hard-cap at 167, you're finished!"],
    [7, 100,
     {'Roid Ragin': 400, 'Warriors Rule': 200, 'Hearty Diggy': 400, 'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 280, 'Multorange': 120,
      'Dream of Ironfish': 120},
     {'Swift Steppin': 400, 'Archer or Bust': 200, 'Bug^2': 120, 'Premigreen': 120},
     {'Stable Jenius': 400, 'Mage is Best': 200, 'Hocus Choppus': 400, 'Molto Loggo': 120, 'Le Brain Tools': 280, 'Severapurple': 120, 'Tree Sleeper': 160},
     {'Laaarrrryyyy': 150, 'Hammer Hammer': 150, },
     "80%",
     "Larry at 150 = 72% chance for +2 levels. Somewhere around level 125-150, this bubble should pass 100m Dementia Ore cost and be available to level with Boron upgrades from the W3 Atom Collider in Construction.  It should be, in my opinion, the ONLY Utility Bubble you spend these daily clicks on until it reaches 501. If you cannot afford the Particles needed to level Larry, invest into Sampling Bubbles."],
    [8, 100,
     {'Roid Ragin': 567, 'Warriors Rule': 284, 'Hearty Diggy': 567, 'Stronk Tools': 397, 'Multorange': 170, 'Dream of Ironfish': 170, 'Shimmeron': 227},
     {'Swift Steppin': 567, 'Archer or Bust': 284, 'Premigreen': 170},
     {'Stable Jenius': 567, 'Mage is Best': 284, 'Hocus Choppus': 567, 'Le Brain Tools': 397, 'Severapurple': 170, 'Tree Sleeper': 227},
     {'Hammer Hammer': 180, },
     "85%",
     ""],
    [9, 100,
     {'Roid Ragin': 615, 'Warriors Rule': 308, 'Hearty Diggy': 615, 'Stronk Tools': 430, 'Multorange': 185, 'Dream of Ironfish': 185, 'Shimmeron': 246},
     {'Swift Steppin': 615, 'Archer or Bust': 308, 'Premigreen': 185},
     {'Stable Jenius': 615, 'Mage is Best': 308, 'Hocus Choppus': 615, 'Le Brain Tools': 430, 'Severapurple': 185, 'Tree Sleeper': 246},
     {'Hammer Hammer': 210, },
     "86%",
     ""],
    [10, 100,
     {'Roid Ragin': 670, 'Warriors Rule': 335, 'Hearty Diggy': 670, 'Stronk Tools': 469, 'Multorange': 201, 'Dream of Ironfish': 201, 'Shimmeron': 268},
     {'Swift Steppin': 670, 'Archer or Bust': 335, 'Premigreen': 201},
     {'Stable Jenius': 670, 'Mage is Best': 335, 'Hocus Choppus': 670, 'Le Brain Tools': 469, 'Severapurple': 201, 'Tree Sleeper': 268},
     {'Laaarrrryyyy': 501, },
     "87%",
     ""],
    [11, 100,
     {'Roid Ragin': 700, 'Warriors Rule': 367, 'Hearty Diggy': 734, 'Stronk Tools': 514, 'Multorange': 220, 'Dream of Ironfish': 220, 'Shimmeron': 294},
     {'Swift Steppin': 700, 'Archer or Bust': 367, 'Premigreen': 220},
     {'Stable Jenius': 700, 'Mage is Best': 367, 'Hocus Choppus': 734, 'Le Brain Tools': 514, 'Severapurple': 220, 'Tree Sleeper': 294},
     {'Cookin Roadkill': 630, 'Hammer Hammer': 270, },
     "88%",
     ""],
    [12, 100,
     {'Roid Ragin': 720, 'Warriors Rule': 405, 'Hearty Diggy': 810, 'Stronk Tools': 567, 'Multorange': 243, 'Dream of Ironfish': 243, 'Shimmeron': 324},
     {'Swift Steppin': 720, 'Archer or Bust': 405, 'Premigreen': 243},
     {'Stable Jenius': 720, 'Mage is Best': 405, 'Hocus Choppus': 810, 'Le Brain Tools': 567, 'Severapurple': 243, 'Tree Sleeper': 324},
     {'Startue Exp': 240, 'Hammer Hammer': 300, },
     "89%",
     ""],
    [13, 100,
     {'Roid Ragin': 740, 'Warriors Rule': 450, 'Hearty Diggy': 900, 'Stronk Tools': 630, 'Multorange': 270, 'Dream of Ironfish': 270, 'Shimmeron': 360},
     {'Swift Steppin': 740, 'Archer or Bust': 450, 'Premigreen': 270},
     {'Stable Jenius': 740, 'Mage is Best': 450, 'Hocus Choppus': 900, 'Le Brain Tools': 630, 'Severapurple': 270, 'Tree Sleeper': 360},
     {'Droppin Loads': 280},
     "90%",
     ""],
    [14, 100,
     {'Roid Ragin': 760, 'Warriors Rule': 506, 'Hearty Diggy': 1012, 'Multorange': 304, 'Shimmeron': 405},
     {'Swift Steppin': 760, 'Archer or Bust': 506, 'Premigreen': 304},
     {'Stable Jenius': 760, 'Mage is Best': 506, 'Hocus Choppus': 1012, 'Severapurple': 304},
     {'Call Me Bob': 200},
     "91%",
     ""],
    [15, 100,
     {'Roid Ragin': 780, 'Warriors Rule': 575, 'Hearty Diggy': 1150, 'Multorange': 345, 'Shimmeron': 460},
     {'Swift Steppin': 780, 'Archer or Bust': 575, 'Premigreen': 345},
     {'Stable Jenius': 780, 'Mage is Best': 575, 'Hocus Choppus': 1150, 'Severapurple': 345},
     {'Big P': 140, 'Big Game Hunter': 70, 'Mr Massacre': 117},
     "92%",
     ""],
    [16, 100,
     {'Roid Ragin': 800, 'Warriors Rule': 665, 'Hearty Diggy': 1329, 'Multorange': 399, 'Shimmeron': 532},
     {'Swift Steppin': 800, 'Archer or Bust': 665, 'Premigreen': 399},
     {'Stable Jenius': 800, 'Mage is Best': 665, 'Hocus Choppus': 1329, 'Severapurple': 399},
     {'Big P': 240, 'Big Game Hunter': 120, 'Mr Massacre': 200},
     "93%",
     ""],
    [17, 100,
     {'Roid Ragin': 820, 'Warriors Rule': 784, 'Hearty Diggy': 1567, 'Multorange': 470, 'Shimmeron': 627},
     {'Swift Steppin': 820, 'Archer or Bust': 784, 'Premigreen': 470},
     {'Stable Jenius': 820, 'Mage is Best': 784, 'Hocus Choppus': 1567, 'Severapurple': 470},
     {'Big P': 340, 'Carpenter': 284, 'Big Game Hunter': 170, 'Mr Massacre': 284},
     "94%",
     ""],
    [18, 100,
     {'Roid Ragin': 840, 'Warriors Rule': 950, 'Hearty Diggy': 1900, 'Multorange': 570, 'Shimmeron': 760},
     {'Swift Steppin': 840, 'Archer or Bust': 950, 'Premigreen': 570},
     {'Stable Jenius': 840, 'Mage is Best': 950, 'Hocus Choppus': 1900, 'Severapurple': 570},
     {'Laaarrrryyyy': 900, 'Big P': 540, 'Call Me Bob': 500, 'Carpenter': 450, 'Big Game Hunter': 270, 'Mr Massacre': 450},
     "95%",
     ""],
    [19, 100,
     {'Roid Ragin': 860, 'Warriors Rule': 1200, 'Multorange': 720},
     {'Swift Steppin': 860, 'Archer or Bust': 1200},
     {'Stable Jenius': 860, 'Mage is Best': 1200, 'Severapurple': 720},
     {'Call Me Bob': 700},
     "96%",
     ""],
    [20, 100,
     {'Roid Ragin': 880, 'Warriors Rule': 1617, 'Multorange': 970},
     {'Swift Steppin': 880, 'Archer or Bust': 1617},
     {'Stable Jenius': 880, 'Mage is Best': 1617, 'Severapurple': 970},
     {'Laaarrrryyyy': 1900, 'Big P': 1140, 'Carpenter': 950, 'Big Game Hunter': 570, 'Mr Massacre': 950, 'Diamond Chef': 553},
     "97%",
     ""],
    [21, 120,
     {'Roid Ragin': 900, 'Warriors Rule': 2450, 'Multorange': 1470},
     {'Swift Steppin': 900, 'Archer or Bust': 2450},
     {'Stable Jenius': 900, 'Mage is Best': 2450, 'Severapurple': 1470},
     {'Call Me Bob': 1000, 'Diamond Chef': 890},
     "98%",
     ""],
    [22, 140,
     {'Roid Ragin': 950, 'Warriors Rule': 4950, 'Multorange': 2970},
     {'Swift Steppin': 950, 'Archer or Bust': 4950},
     {'Stable Jenius': 950, 'Mage is Best': 4950, 'Severapurple': 2970},
     {'Diamond Chef': 1226, 'Carpenter': 2331},
     "99%",
     ""],
    [23, 160,
     {'Roid Ragin': 1000, 'Hearty Diggy': 9900, 'Stronk Tools': 6930, 'Dream of Ironfish': 2970, 'Shimmeron': 3960, 'Slabi Orefish': 5940,
      'Slabi Strength': 5940},
     {'Swift Steppin': 1000, 'Sanic Tools': 6930, 'Premigreen': 2970, 'Fly in Mind': 3960, 'Slabo Critterbug': 5940, 'Slabo Agility': 5940},
     {'Stable Jenius': 1000, 'Hocus Choppus': 9900, 'Le Brain Tools': 6930, 'Tree Sleeper': 3960, 'Slabe Logsoul': 5940, 'Slabe Wisdom': 5940},
     {'Diamond Chef': 1897, 'Carpenter': 2450},
     "99% catchup",
     ""],
]
vials_progressionTiers = [
    # int tier, int TotalVialsUnlocked, int TotalVialsMaxed, list ParticularVials, str Notes
    [0, 0, 0, [], ""],
    [1, 7, 0, [], "This is the number of vials requiring an unlock roll of 75 or less. "],
    [2, 14, 0, [], "This is the number of vials requiring an unlock roll of 85 or less. "],
    [3, 19, 0, [], "This is the number of vials requiring an unlock roll of 90 or less. "],
    [4, 27, 0, [], "This is the number of vials requiring an unlock roll of 95 or less. "],
    [5, 33, 0, [], "This is the number of vials requiring an unlock roll of 98 or less. "],
    [6, 38, 0, [], "This is all vials up through W4, excluding the Arcade Pickle. "],
    [7, 51, 0, [], "This is all vials up through W5, excluding the Arcade Pickle. "],
    [8, 63, 0, [], "This is all vials up through W5, excluding the Arcade Pickle. "],
    [9, 67, 0, [], "This is all vials up through W5, excluding the Arcade Pickle. "],
    [10, 70, 0, [], "This is all vials up through W5, excluding the Arcade Pickle. "],
    [11, 70, 4, ['Copper Corona (Copper Ore)', 'Sippy Splinters (Oak Logs)', 'Jungle Juice (Jungle Logs)', 'Tea With Pea (Potty Rolls)'],
     "This is the first half of W6, excluding the Arcade Pickle. "],
    [12, 70, 8, ['Gold Guzzle (Gold Ore)', 'Seawater (Goldfish)', 'Fly In My Drink (Fly)', 'Blue Flav (Platinum Ore)'], ""],
    [13, 72, 12, ['Slug Slurp (Hermit Can)', 'Void Vial (Void Ore)', 'Ew Gross Gross (Mosquisnow)', 'The Spanish Sahara (Tundra Logs)'], ""],
    [14, 72, 16, ['Mushroom Soup (Spore Cap)', 'Maple Syrup (Maple Logs)', 'Marble Mocha (Marble Ore)', 'Skinny 0 Cal (Snake Skin)'], ""],
    [15, 72, 20, ['Long Island Tea (Sand Shark)', 'Anearful (Glublin Ear)', 'Willow Sippy (Willow Logs)', 'Dieter Drink (Bean Slices)'], ""],
    [16, 72, 24, ['Shinyfin Stew (Equinox Fish)', 'Ramificoction (Bullfrog Horn)', 'Tail Time (Rats Tail)', 'Dreamy Drink (Dream Particulate)'], ""],
    [17, 72, 28, ['Mimicraught (Megalodon Tooth)', 'Fur Refresher (Floof Ploof)', 'Etruscan Lager (Mamooth Tusk)', 'Dusted Drink (Dust Mote)'], ""],
    [18, 72, 32, ['Ded Sap (Effervescent Log)', 'Sippy Soul (Forest Soul)', 'Visible Ink (Pen)', 'Snow Slurry (Snow Ball)'], ""],
    [19, 72, 36, ['Sippy Cup (Sippy Straw)', 'Goosey Glug (Honker)', 'Crab Juice (Crabbo)', 'Chonker Chug (Dune Soul)'], ""],
    [20, 72, 40, ['40-40 Purity (Contact Lense)', 'Ladybug Serum (Ladybug)', 'Bubonic Burp (Mousey)', 'Capachino (Purple Mush Cap)'], ""],
    [21, 72, 44, ['Donut Drink (Half Eaten Donut)', 'Krakenade (Kraken)', 'Calcium Carbonate (Tongue Bone)', 'Spool Sprite (Thread)'], ""],
    [22, 72, 48, ['Choco Milkshake (Crumpled Wrapper)', 'Electrolyte (Condensed Zap)', 'Ash Agua (Suggma Ashes)', 'Oj Jooce (Orange Slice)'], ""],
    [23, 72, 52, ['Thumb Pow (Trusty Nails)', 'Slowergy Drink (Frigid Soul)', 'Bunny Brew (Bunny)', 'Flavorgil (Caulifish)'], ""],
    [24, 72, 56, ['Spook Pint (Squishy Soul)', 'Firefly Grog (Firefly)', 'Barium Mixture (Copper Bar)', 'Bloat Draft (Blobfish)'], ""],
    [25, 73, 60, ['Barley Brew (Iron Bar)', 'Oozie Ooblek (Oozie Soul)', 'Ricecakorade (Rice Cake)', 'Greenleaf Tea (Leafy Branch)'], ""],
    [26, 74, 65, ['Venison Malt (Mongo Worm Slices)', 'Gibbed Drink (Eviscerated Horn)', 'Royale Cola (Royal Headpiece)', 'Refreshment (Breezy Soul)',
                  'Turtle Tisane (Tuttle)'], ""],
    # [27, 75, 69, ['Red Malt (Redox Salts)', 'Poison Tincture (Poison Froge)', 'Orange Malt (Explosive Salts)', 'Shaved Ice (Purple Salt)'], "Currently considered impossible"],
    # [28, 75, 73, ['Dreadnog (Dreadlo Bar)', 'Dabar Special (Godshard Bar)', 'Pearl Seltzer (Pearler Shell)', 'Hampter Drippy (Hampter)'], "Currently considered impossible"],
    # [29, 75, 76, ['Pickle Jar (BobJoePickle)', 'Ball Pickle Jar (BallJoePickle)'], "Currently considered impossible"],
]

###WORLD 3 PROGRESSION TIERS###
saltLick_progressionTiers = [
    [0, {}, ""],
    [1, {'Obol Storage': 8}, "Froge"],
    [2, {'Printer Sample Size': 20}, "Redox Salts"],
    [3, {'Refinery Speed': 10}, "Explosive Salts"],
    [4, {'Max Book': 10}, "Spontaneity Salts"],
    [5, {'Movespeed': 1}, "Frigid Soul"],  # This buff only works under 170% move speed, so can become useless quite quickly.
    [6, {'TD Points': 10}, "Dioxide Synthesis"],
    [7, {'Multikill': 10}, "Purple Salt"],
    [8, {'EXP': 100}, "Dune Soul"],
    [9, {'Alchemy Liquids': 100}, "Mousey"],
    [10, {'Damage': 250}, "Pingy"]
]
deathNote_progressionTiers = [
    # 0-4 int tier. int w1LowestSkull, int w2LowestSkull, int w3LowestSkull, int w4LowestSkull,
    # 5-9 int w5LowestSkull, int w6LowestSkull, int w7LowestSkull, int w8LowestSkull, int zowCount, int chowCount,
    # 10-11 int meowCount, str Notes
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ""],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, ""],
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, ""],
    [3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, ""],
    [4, 4, 4, 4, 2, 0, 0, 0, 0, 15, 0, 0,
     "The recommendation for ZOWs is 12hrs or less (8,333+ KPH) per enemy. If you aren't at that mark yet, don't sweat it. Come back later!"],
    [5, 5, 5, 5, 3, 0, 0, 0, 0, 26, 0, 0,
     "The Voidwalker questline requires W1-W3 at all Plat Skulls. Aim to complete this by Mid W5 as Vman's account-wide buffs are insanely strong."],
    [6, 7, 5, 5, 4, 0, 0, 0, 0, 40, 15, 0,
     "The recommendation for CHOWs is 12hrs or less (83,333+ KPH) per enemy. If you aren't at that mark yet, don't sweat it. Come back later!"],
    [7,  10, 7,  5,  5,  1,  0,     0, 0, 40, 26, 0, ""],
    [8,  10, 10, 7,  5,  2,  0,     0, 0, 40, 40, 0, ""],
    [9,  10, 10, 10, 5,  3,  0,     0, 0, 40, 40, 0, ""],
    [10, 10, 10, 10, 7,  4,  0,     0, 0, 53, 53, 0, ""],
    [11, 10, 10, 10, 10, 5,  0,     0, 0, 53, 53, 0, "Complete Lava Skull, then BB Super CHOW, before you start working on Eclipse Skulls. "],
    [12, 10, 10, 10, 10, 7,  0,     0, 0, 66, 66, 0, ""],
    [13, 10, 10, 10, 10, 10, 0,     0, 0, 66, 66, 0, ""],
    [14, 10, 10, 10, 10, 10, 0,     0, 0, 73, 66, 0, ""],
    [15, 10, 10, 10, 10, 10, 0,     0, 0, 73, 73, 0, "The recommendation for Super CHOWs is 24hrs or less (4m+ KPH)"],
    [16, 20, 10, 10, 10, 10, 0,     0, 0, 80, 73, 26, ""],
    [17, 20, 20, 10, 10, 10, 1,     0, 0, 84, 80, 40, ""],
    [18, 20, 20, 20, 10, 10, 2,     0, 0, 85, 80, 53, ""],
    [19, 20, 20, 20, 20, 10, 3,     0, 0, 85, 80, 66, ""],
    [20, 20, 20, 20, 20, 20, 4,     0, 0, 85, 82, 66, ""],
    [21, 20, 20, 20, 20, 20, 5,     0, 0, 85, 83, 66, ""],
    [22, 20, 20, 20, 20, 20, 7,     0, 0, 85, 83, 66, ""],
    [23, 20, 20, 20, 20, 20, 10,    0, 0, 85, 83, 70, ""],
    [24, 20, 20, 20, 20, 20, 10,    0, 0, 85, 83, 80, ""],
    [25, 20, 20, 20, 20, 20, 20,    0, 0, 85, 83, 82, ""],
    [26, 20, 20, 20, 20, 20, 20,    0, 0, 85, 83, 83, ""],
    [27, 20, 20, 20, 20, 20, 20,    0, 0, 85, 85, 84, "As of v2.05, completing a Super CHOW on Boops is impossible."],
    [28, 20, 20, 20, 20, 20, 20,    0, 0, 86, 86, 86, "Info only"]
]
buildingsPostBuffs_progressionTiers = [
    [0, "Unlock", [], "", ""],
    [1, "SS", [0, 5, 7], "", ""],
    [2, "S", [1, 2, 3, 6, 11, 15, 16], "", ""],
    [3, "A", [4, 9, 10, 12, 13, 14, 17, 22, 24, 25], "", ""],
    [4, "B", [18, 19, 20, 21, 23, 26], "", ""],
    [5, "C", [8], "", ""],
    [6, "D", [], "", ""],
    [7, "F", [], "", ""]
]
buildingsPreBuffs_progressionTiers = [
    [0, "Unlock", [], "", ""],
    [1, "SS", [0, 5, 7], "", ""],
    [2, "S", [1, 2, 3, 6, 11, 15, 16], "", ""],
    [3, "A", [4, 13, 14, 22, 24, 25], "", ""],
    [4, "B", [12, 17], "", ""],
    [5, "C", [8, 18, 19, 20, 21], "", ""],
    [6, "D", [9, 10, 23], "", ""],
    [7, "F", [26], "", ""]
]
prayers_progressionTiers = [
    #Tier, PrayerDict, 	Notes
    [0, {}, ""],
    [1, {'The Royal Sampler (Rooted Soul)': 5}, ""],
    [2, {'Skilled Dimwit (Forest Soul)':20}, ""],
    [3, {'Balance of Pain (Squishy Soul)':11}, ""],
    [4, {'Skilled Dimwit (Forest Soul)':35, 'Balance of Pain (Squishy Soul)':20}, ""],
    [5, {'Midas Minded (Dune Soul)':20}, ""],
    [6, {'Skilled Dimwit (Forest Soul)':50, 'Midas Minded (Dune Soul)':50, 'Balance of Pain (Squishy Soul)':30}, ""],
    [7, {'Shiny Snitch (Forest Soul)':50, 'Zerg Rushogen (Forest Soul)':20, 'Jawbreaker (Dune Soul)':50, 'Ruck Sack (Rooted Soul)':50, 'Balance of Proficiency (Squishy Soul)':50}, ""],
    [8, {'Unending Energy (Forest Soul)':50, 'Big Brain Time (Forest Soul)':50, 'Antifun Spirit (Rooted Soul)':10, 'Fibers of Absence (Frigid Soul)':50, 'Beefy For Real (Frigid Soul)':40}, ""],
    [9, {'Tachion of the Titans (Dune Soul)':1, 'Balance of Precision (Dune Soul)':1, 'Circular Criticals (Rooted Soul)':1, 'Vacuous Tissue (Frigid Soul)':1, 'Glitterbug (Squishy Soul)':1}, ""],
]

###WORLD 4 PROGRESSION TIERS###
breeding_progressionTiers = {
        0: {
            "Tier": 0,
            "TerritoriesUnlocked": 0,
            "PetSlots": 2,
            "TerritoryNotes": "",
            "ArenaWaves": 0,
            "ArenaNotes": "",
            "Shinies": {},
            "ShinyNotes": ""
            },
        1: {
            "Tier": 1,
            "TerritoriesUnlocked": 3,
            "PetSlots": 3,
            "TerritoryNotes": "",
            "ArenaWaves": 3,
            "ArenaNotes": "",
            "Shinies": {},
            "ShinyNotes": ""
            },
        2: {
            "Tier": 2,
            "TerritoriesUnlocked": 7,
            "PetSlots": 4,
            "TerritoryNotes": "",
            "ArenaWaves": 15,
            "ArenaNotes": "",
            "Shinies": {},
            "ShinyNotes": ""
            },
        3: {
            "Tier": 3,
            "TerritoriesUnlocked": 10,
            "PetSlots": 4,
            "TerritoryNotes": "",
            "ArenaWaves": 50,
            "ArenaNotes": "",
            "Shinies": {},
            "ShinyNotes": ""
            },
        4: {
            "Tier": 4,
            "TerritoriesUnlocked": 14,
            "PetSlots": 5,
            "TerritoryNotes": "",
            "ArenaWaves": 125,
            "ArenaNotes": "",
            "Shinies": {},
            "ShinyNotes": ""
            },
        5: {
            "Tier": 5,
            "TerritoriesUnlocked": 20,
            "PetSlots": 6,
            "TerritoryNotes": "",
            "ArenaWaves": 200,
            "ArenaNotes": "",
            "Shinies": {},
            "ShinyNotes": ""
            },
        #0-5 are Territory/Arena focused.
        #6 is blended
        #7+ are Shiny focused
        6: {
            "Tier": 6,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Faster Shiny Pet Lv Up Rate": 24,
                "Bonuses from All Meals": 10
            },
            "ShinyNotes": "Start by focusing on pets that increase Shiny Speed rate. This will decrease the amount of time needed to level up pets in the future."
            },
        7: {
            "Tier": 7,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Infinite Star Signs": 25,
                "Base Efficiency for All Skills": 20
                },
            "ShinyNotes": ""
            },
        8: {
            "Tier": 8,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Base Critter Per Trap": 10,
                "Drop Rate": 15
                },
            "ShinyNotes": ""
            },
        9: {
            "Tier": 9,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Faster Refinery Speed": 15,
                "Lower Minimum Travel Time for Sailing": 5
                },
            "ShinyNotes": ""
        },
        10: {
            "Tier": 10,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Multikill Per Tier": 20,
                "Higher Artifact Find Chance": 15
                },
            "ShinyNotes": ""
        },
        11: {
            "Tier": 11,
            "TerritoriesUnlocked": 24,
            "ArenaWaves": 200,
            "Shinies": {
                "Faster Shiny Pet Lv Up Rate": 28,
                "Infinite Star Signs": 36
            },
            "ShinyNotes": ""
        }
    }
rift_progressionTiers = {
    0: [0,  "",             0],
    1: [5,  "3 to 5M",      100],
    2: [10, "30M",          140],
    3: [15, "68M",          160],
    4: [20, "185M",         180],
    5: [25, "1,120M",       180],
    6: [30, "12B",          220],
    7: [35, "125B",         220],
    8: [40, "1,554B",       240],
    9: [45, "20T",          240],
}

###WORLD 5 PROGRESSION TIERS###
divinity_progressionTiers = {
    0: {},
    1: {"GodsUnlocked": 1},
    2: {"GodsUnlocked": 2},
    3: {"GodsUnlocked": 3},
    4: {"GodsUnlocked": 4},
    5: {"GodsUnlocked": 5},
    6: {"GodsUnlocked": 6},
    7: {"GodsUnlocked": 7},
    8: {"GodsUnlocked": 8},
    9: {"GodsUnlocked": 9},
    10: {"GodsUnlocked": 10},
    11: {"MaxDivLevel": 50},
    12: {"MinDivLevel": 40}
}
###WORLD 6 PROGRESSION TIERS###

###GENERAL PROGRESSION TIERS###
combatLevels_progressionTiers = [
    # int tier, int TotalAccountLevel, str TAL reward, int PlayerLevels, str PL reward, str notes
    [0, 0, "", 0, "", ""],
    [1, 8, "Character 2", 25, "Personal - Circle Obol Slot 2", ""],
    [2, 30, "Character 3", 32, "Personal - Square Obol Slot 1", ""],
    [3, 60, "Character 4 and Family - Circle Obol Slot 1", 40, "Personal - Circle Obol Slot 3", ""],
    [4, 80, "Family - Circle Obol Slot 2", 48, "Personal - Circle Obol Slot 4", ""],
    [5, 100, "Family - Circle Obol Slot 3", 60, "Personal - Square Obol Slot 2", ""],
    [6, 130, "Character 5", 70, "Personal - Circle Obol Slot 5", ""],
    [7, 160, "Family - Circle Obol Slot 4", 80, "Personal - Circle Obol Slot 6", ""],
    [8, 200, "Family - Square Obol Slot 1", 90, "Personal - Square Obol Slot 3", ""],
    [9, 225, "Character 6", 98, "Personal - Circle Obol Slot 7", ""],
    [10, 250, "Family - Circle Obol Slot 5", 105, "Personal - Hexagon Obol Slot 1", ""],
    [11, 330, "Character 7", 112, "Personal - Circle Obol Slot 8", ""],
    [12, 350, "Family - Circle Obol Slot 6", 120, "Personal - Square Obol Slot 4", ""],
    [13, 400, "Family - Circle Obol Slot 7 and Family - Hexagon Obol Slot 1", 130, "Personal - Circle Obol Slot 9", ""],
    [14, 470, "Character 8 and Family - Circle Obol Slot 8", 140, "Personal - Square Obol Slot 5", ""],
    [15, 600, "Character 9", 150, "Vman Quest, if class = Mman", ""],
    [16, 650, "Family - Sparkle Obol Slot 1", 152, "Personal - Circle Obol Slot 10", ""],
    [17, 700, "Family - Square Obol Slot 2", 180, "Personal - Hexagon Obol Slot 2", ""],
    [18, 875, "Family - Circle Obol Slot 9", 190, "Personal - Square Obol Slot 6", ""],
    [19, 900, "Character 10 and Family - Hexagon Obol Slot 2", 210, "Personal - Circle Obol Slot 12", ""],
    [20, 1150, "Family - Square Obol Slot 3",   250, "Personal - Sparkle Obol Slot 1 and Credit towards Equinox Dream 11", ""],
    [21, 1200, "Family - Sparkle Obol Slot 2",  425, "Able to equip The Divine Scarf", ""],
    [22, 1250, "Family - Circle Obol Slot 10",  450, "Able to equip One of the Divine Trophy", ""],
    [23, 1500, "Family - Circle Obol Slot 11",  500, "Credit towards Equinox Dream 23", ""],
    [24, 1750, "Family - Hexagon Obol Slot 3",  500, "Credit towards Equinox Dream 23", ""],
    [25, 2000, "Family - Square Obol Slot 4",   500, "Credit towards Equinox Dream 23",  ""],
    [26, 2100, "Family - Circle Obol Slot 12",  500, "Credit towards Equinox Dream 23", ""],
    [27, 2500, "Family - Sparkle Obol Slot 3",  500, "Credit towards Equinox Dream 23", ""],
    [28, 3000, "Family - Hexagon Obol Slot 4",  500, "Credit towards Equinox Dream 23", ""],
    [29, 5000, "Family - Sparkle Obol Slot 4",  500, "Credit towards Equinox Dream 23", ""],
    [30, 5300, "Unlock all Tome challenges",    500, "Credit towards Equinox Dream 23", ""]
]
gemShop_progressionTiers = [
    # int tier, str tierName, dict recommendedPurchases, str notes
    [0, "", {}, ""],
    [1, "SS", {'Infinity Hammer': 1, 'Bleach Liquid Cauldrons': 1, 'Crystal 3d Printer': 1, 'Richelin Kitchen': 1, 'Golden Sprinkler': 1, 'Shroom Familiar': 1},
     "These are the highest priority as 1st purchase per world."],
    [2, "S", {'Extra Card Slot': 4, 'Brimstone Forge Slot': 1}, ""],
    [3, "A", {'Item Backpack Space': 1, 'Storage Chest Space': 4, 'Carry Capacity': 2, 'Weekly Dungeon Boosters': 3, 'Brimstone Forge Slot': 4,
              'Bleach Liquid Cauldrons': 2, 'Zen Cogs': 2, 'Tower Building Slots': 1, 'Royal Egg Cap': 3, 'Richelin Kitchen': 3, 'Souped Up Tube': 1,
              'Chest Sluggo': 3, 'Divinity Sparkie': 2, 'Lava Sprouts': 2, 'Plot of Land': 2}, ""],
    [4, "B", {'Item Backpack Space': 2, 'Storage Chest Space': 8, 'Carry Capacity': 4, 'Food Slot': 1, 'Bleach Liquid Cauldrons': 3, 'More Sample Spaces': 2,
              'Zen Cogs': 4, 'Tower Building Slots': 2, 'Royal Egg Cap': 5, 'Fenceyard Space': 2, 'Chest Sluggo': 6, 'Lava Sprouts': 4, 'Plot of Land': 4,
              'Shroom Familiar': 2, 'Instagrow Generator': 1}, ""],
    [5, "C", {'Item Backpack Space': 3, 'Storage Chest Space': 12, 'Carry Capacity': 6, 'Food Slot': 2, 'Bleach Liquid Cauldrons': 4, 'More Sample Spaces': 4,
              'Burning Bad Books': 2, 'Tower Building Slots': 4, 'Fenceyard Space': 4, 'Chest Sluggo': 9, 'Golden Sprinkler': 2, 'Lava Sprouts': 6,
              'Plot of Land': 6, 'Shroom Familiar': 3, 'Instagrow Generator': 2}, ""],
    [6, "D",
     {'Item Backpack Space': 4, 'Carry Capacity': 8, 'More Storage Space': 5, 'Brimstone Forge Slot': 8, 'Ivory Bubble Cauldrons': 4, 'Obol Storage Space': 3,
      'More Sample Spaces': 6, 'Burning Bad Books': 4, 'Zen Cogs': 8, 'Souped Up Tube': 3, 'Fenceyard Space': 6, 'Chest Sluggo': 12, 'Plot of Land': 8,
      'Instagrow Generator': 4}, ""],
    [7, "Practical Max",
     {'Item Backpack Space': 6, 'Carry Capacity': 10, 'More Storage Space': 10, 'Card Presets': 1, 'Brimstone Forge Slot': 16, 'Sigil Supercharge': 10,
      'Fluorescent Flaggies': 2, 'Golden Sprinkler': 4, 'Plot of Land': 12, 'Instagrow Generator': 8},
     "I wouldn't recommend going any further as of v2.02. This tier is for the dedicated Gem Farmers from Colo and Normal-difficulty World Bosses."],
    [8, "True Max",
     {'Card Presets': 5, 'Daily Teleports': 10, 'Daily Minigame Plays': 4, 'Weekly Dungeon Boosters': 11, 'Obol Storage Space': 12, 'Prayer Slots': 4,
      'Cog Inventory Space': 20, 'Fluorescent Flaggies': 6, 'Richelin Kitchen': 10, 'Souped Up Tube': 5, 'Pet Storage': 12, 'Divinity Sparkie': 6},
     "This final tier is for the truly depraved. Many of these bonuses are very weak or outright useless."]
]
greenstack_progressionTiers = {
        0: {  # The timegated tier
            "Vendor Shops": [
                "CraftMat3",  # W1 Cue Tape
                "FoodHealth4", "Quest19",  # W2 Saucy Weiner and Gold Dubloon
                "FoodHealth9", "FoodHealth11",  #W3
                "FoodHealth12", "FoodHealth13", "FoodPotOr4", "FoodPotGr4", "FoodPotRe4", "FoodPotYe4",  #W4
                "FoodHealth14", "FoodHealth15", "OilBarrel6",  #W5
                "FoodHealth16", "FoodHealth17", "OilBarrel7",  #W6
            ],
            "Misc": [
                "FoodPotGr3",  # Previously Tier10
                "FoodPotRe2"   # Previously Tier11.
            ],
            "Other Skilling Resources": [
                "Refinery1", "Refinery2", "Refinery3", "Refinery4", "Refinery5", "Refinery6"],
        },
        1: {
            "Printable Skilling Resources": [
                "OakTree", "BirchTree", "JungleTree", "ForestTree", "ToiletTree", "PalmTree", "StumpTree", "SaharanFoal",
                "Copper", "Iron", "Gold", "Plat", "Dementia", "Void", "Lustre",
                "Fish1", "Fish2", "Fish3",
                "Bug1", "Bug2"],
            },
        2: {
            "Printable Skilling Resources": [
                "Tree7", "AlienTree", "Tree8", "Tree9", "Tree11",
                "Starfire", "Marble",
                "Fish4", "Fish5", "Fish6", "Fish7",
                "Bug3", "Bug4", "Bug5", "Bug6", "Bug7", "Bug8"],
            "Other Skilling Resources": [
                "CraftMat1",],
            "Vendor Shops": [
                "FoodHealth14", "FoodHealth15",]
            },
        3: {
            "Base Monster Materials": [
                "Grasslands1", "Grasslands2", "Grasslands4", "Grasslands3", "Jungle1", "Jungle2", "Jungle3", "Forest1", "Forest2", "Forest3",],
            "Printable Skilling Resources": [
                "Tree10",
                "Dreadlo",
                "Fish8", "Fish9", "Fish10",
                "Bug9", "Bug11"],
            "Other Skilling Resources": [
                "CraftMat5",],
            "Vendor Shops": [
                "FoodHealth12", "FoodHealth13",],
            },
        4: {
            "Base Monster Materials": [
                "Sewers1", "Sewers2", "TreeInterior1", "TreeInterior2",],
            "Printable Skilling Resources": [
                "Tree12",
                "Godshard",
                "Fish11", "Fish12", "Fish13",
                "Bug12", "Bug13",],
            "Other Skilling Resources": [
                "CraftMat6", "Soul1",],
            "Vendor Shops": [
                "FoodHealth16", "FoodHealth17",
                "FoodPotOr4", "FoodPotGr4", "FoodPotRe4", "FoodPotYe4",]
            },
        5: {
                "Base Monster Materials": [
                    "DesertA1", "DesertA2", "DesertA3", "DesertB1", "DesertB2", "DesertB3", "DesertB4", "DesertC1", "DesertC2", "DesertC3", "DesertC4",
                    "SnowA1", "SnowA2", "SnowA3",],
                "Printable Skilling Resources": [
                    "Tree13",],
                "Other Skilling Resources": [
                    "CraftMat7", "CraftMat9",
                    "Critter1", "Critter2",
                    "Soul2",],
            },
        6: {
            "Base Monster Materials": [
                "SnowB1", "SnowB2", "SnowB5", "SnowB3", "SnowB4", "SnowC1", "SnowC2", "SnowC3", "SnowC4"
                "GalaxyA1", "GalaxyA2", "GalaxyA3", "GalaxyA4", "GalaxyB1", "GalaxyB2", ],
            "Other Skilling Resources": [
                "CraftMat8", "CraftMat10",
                "Critter3", "Critter4",
                "Soul3",]
            },
        7: {
            "Base Monster Materials": [
                "SnowA4", "SnowC5",
                "GalaxyB3", "GalaxyB4", "GalaxyB5", "GalaxyC1", "GalaxyC2", "GalaxyC3",],
            "Crystal Enemy Drops": [
                "FoodPotMana1", "FoodPotMana2", "FoodPotGr1", "FoodPotOr1", "FoodPotOr2", "FoodHealth1", "FoodHealth3", "FoodHealth2", "Leaf1"],
            "Other Skilling Resources": [
                "CraftMat11",
                "Critter5",
                "Soul4",],
            },
        8: {
            "Base Monster Materials": [
                "GalaxyC4",
                "LavaA1", "LavaA2", "LavaA3", "LavaA4", "LavaA5", "LavaB1", "LavaB2", "LavaB3", "LavaB4", "LavaB5",],
            "Crystal Enemy Drops": [
                "FoodHealth6", "FoodHealth7", "FoodPotGr2", "FoodPotRe3", "Leaf2",],
            "Other Skilling Resources": [
                "CraftMat12",
                "Critter6", "Critter7",
                "Soul5",],
            },
        9: {
            "Base Monster Materials": [
                "LavaB6", "LavaC1", "LavaC2",  #Can beat Kruk and move to W6 without fighting these
                "SpiA1", "SpiA2", "SpiA3", "SpiA4", "SpiA5", "SpiB1", "SpiB2", "SpiB3",],
            "Crystal Enemy Drops": [
                "FoodHealth10", "FoodPotOr3", "FoodPotYe2", "Leaf3"],
            "Other Skilling Resources": [
                "CraftMat13", "CraftMat14",
                "Critter8", "Critter9",
                "Soul6",],
            },
        10: {
            "Base Monster Materials": [
                "SpiB4", "SpiC1", "SpiC2", "SpiD1", "SpiD2", "SpiD3",],
            "Crystal Enemy Drops": [
                "FoodPotMana4", "Leaf4",
                "FoodPotYe5", "Leaf5",
                "Leaf6",],
            "Printable Skilling Resources": [],
            "Other Skilling Resources": [
                "Critter10", "Critter11",
                "Soul7",
                "CopperBar", "IronBar",
                "Bullet", "BulletB",],
            "Vendor Shops": [
                "OilBarrel6", "OilBarrel7",],
            },
        11: {
            "Missable Quest Items": [
                "Quest3", "Quest4", "Quest7", "Quest12"
                "Quest14", "Quest22", "Quest23", "Quest24",
                "Quest32",
            ],
            "Other Skilling Resources": [
                "PlatBar",
                "FoodMining1", "FoodFish1", "FoodCatch1",
            ],
            },
        12: {
            "Missable Quest Items": ["GoldricP1", "GoldricP2", "GoldricP3", "Quest21"],
            "Base Monster Materials": ["Sewers3"],
            "Crystal Enemy Drops": [
                "EquipmentStatues7", "EquipmentStatues3", "EquipmentStatues2", "EquipmentStatues4", "EquipmentStatues14",
                "rtt0", "StoneZ1", "StoneT1",],
            "Other Skilling Resources": [
                "GoldBar", "DementiaBar", "VoidBar", "LustreBar",
                "Peanut", "Quest68", "Bullet3",],  #I really hate that the Slush Bucket is listed as Quest68
            },
        13: {
            "Base Monster Materials": [
                "Quest15", "Hgg"],
            "Crystal Enemy Drops": [
                "EquipmentStatues1", "EquipmentStatues5",
                "StoneA1", "StoneW1",
                "StoneZ2", "StoneT2",
                "PureWater",
                "FoodG9",],
            "Other Skilling Resources": [
                "StarfireBar",
                "FoodChoppin1",
                "EquipmentSmithingTabs2",
                "PeanutG",],
            "Misc": [
                "FoodPotMana3", "FoodPotRe1", "ButterBar", "OilBarrel2", "Ghost", "Quest78",],
        },
        14: {
            "Crystal Enemy Drops": [
                "StoneW2",],  #"StoneA2",],
            "Other Skilling Resources": [
                "DreadloBar", "MarbleBar", "GodshardBar",
                "FoodTrapping1", "FoodWorship1",
                "Critter1A", "Critter2A", "Critter3A", "Critter4A", "Critter5A", "Critter6A", "Critter7A", "Critter8A", "Critter9A", "Critter10A", "Critter11A"],
            "Misc": [
                "Key2", "Key3"]
        },
    }

missableGStacksDict = {
    #  ItemName               Codename     Quest Codeame          Quest Name                                          Wiki link to the item                             Recommended Class/Farming notes
    "Dog Bone":              ["Quest12",   "Dog_Bone1",           "Dog Bone: Why he Die???",                          "https://idleon.wiki/wiki/Dog_Bone",              "Active ES or time candy."],
    "Ketchup Bottle":        ["Quest3",    "Picnic_Stowaway2",    "Picnic Stowaway: Beating Up Frogs for some Sauce", "https://idleon.wiki/wiki/Ketchup_Bottle",        "Active ES or time candy."],
    "Mustard Bottle":        ["Quest4",    "Picnic_Stowaway2",    "Picnic Stowaway: Beating Up Frogs for some Sauce", "https://idleon.wiki/wiki/Mustard_Bottle",        "Active ES or time candy."],
    "Strange Rock":          ["Quest7",    "Stiltzcho2",          "Stiltzcho: No Stone Unturned",                     "https://idleon.wiki/wiki/Strange_Rock",          "Active ES or time candy."],
    "Time Thingy":           ["Quest21",   "Funguy3",             "Funguy: Partycrastination",                        "https://idleon.wiki/wiki/Time_Thingy",           "Active ES or time candy."],
    "Employment Statistics": ["Quest14",   "TP_Pete2",            "TP Pete: The Rats are to Blame!",                  "https://idleon.wiki/wiki/Employment_Statistics", "Active ES or time candy."],
    "Corporatube Sub":       ["Quest22",   "Mutton4",             "Mutton: 7 Figure Followers",                       "https://idleon.wiki/wiki/Corporatube_Sub",       "Active ES or time candy."],
    "Instablab Follower":    ["Quest23",   "Mutton4",             "Mutton: 7 Figure Followers",                       "https://idleon.wiki/wiki/Instablab_Follower",    "Active ES or time candy."],
    "Cloudsound Follower":   ["Quest24",   "Mutton4",             "Mutton: 7 Figure Followers",                       "https://idleon.wiki/wiki/Cloudsound_Follower",   "Active ES or time candy."],
    "Casual Confidante":     ["GoldricP1", "Goldric3",            "Goldric: Only Winners have Portraits",             "https://idleon.wiki/wiki/Casual_Confidante",     "Active ES or time candy."],
    "Triumphant Treason":    ["GoldricP2", "Goldric3",            "Goldric: Only Winners have Portraits",             "https://idleon.wiki/wiki/Triumphant_Treason",    "Active ES or time candy."],
    "Claiming Cashe":        ["GoldricP3", "Goldric3",            "Goldric: Only Winners have Portraits",             "https://idleon.wiki/wiki/Claiming_Cashe",        "Active ES or time candy."],
    "Monster Rating":        ["Quest32",   "XxX_Cattleprod_XxX3", "XxX_Cattleprod_XxX: Ok, NOW it's Peak Gaming!",    "https://idleon.wiki/wiki/Monster_Rating",        "Monster Ratings can drop from Crystal enemies, making Divine Knight the better farmer for Monster Ratings."]
}

expectedStackables = {
    "Missable Quest Items": [
        "Quest3", "Quest4", "Quest7", "Quest12", "Quest21", "Quest14", "Quest22", "Quest23", "Quest24", "GoldricP1", "GoldricP2", "GoldricP3",
        "Quest32"
    ],
    "Base Monster Materials": [
        "Grasslands1", "Grasslands2", "Grasslands4", "Grasslands3", "Jungle1", "Jungle2", "Jungle3", "Forest1", "Forest2", "Forest3", "Sewers1",
        "Sewers2", "TreeInterior1", "TreeInterior2",  # W1
        "DesertA1", "DesertA2", "DesertA3", "DesertB1", "DesertB2", "DesertB3", "DesertB4", "DesertC1", "DesertC2", "DesertC3", "DesertC4",  # W2
        "SnowA1", "SnowA2", "SnowA3", "SnowB1", "SnowB2", "SnowB5", "SnowB3", "SnowB4", "SnowC1", "SnowC2", "SnowC3", "SnowC4", "SnowA4", "SnowC5",  # W3
        "GalaxyA1", "GalaxyA2", "GalaxyA3", "GalaxyA4", "GalaxyB1", "GalaxyB2", "GalaxyB3", "GalaxyB4", "GalaxyB5", "GalaxyC1", "GalaxyC2",
        "GalaxyC3", "GalaxyC4",  # W4
        "LavaA1", "LavaA2", "LavaA3", "LavaA4", "LavaA5", "LavaB1", "LavaB2", "LavaB3", "LavaB4", "LavaB5", "LavaB6", "LavaC1", "LavaC2",  # W5
        "SpiA1", "SpiA2", "SpiA3", "SpiA4", "SpiA5", "SpiB1", "SpiB2", "SpiB3", "SpiB4", "SpiC1", "SpiC2", "SpiD1", "SpiD2", "SpiD3",  # W6
        "Sewers3", "Quest15", "Hgg"  # Specialty Monster Materials
    ],
    "Crystal Enemy Drops": [
        "FoodPotMana1", "FoodPotMana2", "FoodPotGr1", "FoodPotOr1", "FoodPotOr2", "FoodHealth1", "FoodHealth3", "FoodHealth2", "Leaf1",  # W1
        "FoodHealth6", "FoodHealth7", "FoodPotGr2", "FoodPotRe3", "Leaf2",  # W2
        "FoodHealth10", "FoodPotOr3", "FoodPotYe2", "Leaf3",  # W3
        "FoodPotMana4", "Leaf4",  # W4
        "FoodPotYe5", "Leaf5",  # W5
        "Leaf6",  # W6
        "EquipmentStatues7", "EquipmentStatues3", "EquipmentStatues2", "EquipmentStatues4", "EquipmentStatues14",  # Standard statues
        "EquipmentStatues1", "EquipmentStatues5",  # Plausible but time consuming
        "rtt0", "StoneZ1", "StoneT1", "StoneW1", "StoneA1",  #W1 Slow drops = Town TP + Stones
        "StoneT2", "StoneZ2",  "StoneW2",  #"StoneA2", # W2 upgrade stones and Mystery2
        "PureWater",  #W3 Slow drops = Distilled Water
        "FoodG9",  #W5 Slow drops = Golden W5 Sammy
    ],
    "Printable Skilling Resources": [
        "OakTree", "BirchTree", "JungleTree", "ForestTree", "ToiletTree", "PalmTree", "StumpTree", "SaharanFoal",  # Logs1
        "Tree7", "AlienTree", "Tree8", "Tree9", "Tree11", "Tree10", "Tree12", "Tree13",  # Logs2

        "Copper", "Iron", "Gold", "Plat", "Dementia", "Void", "Lustre",  # Ores1
        "Starfire", "Marble", "Dreadlo", "Godshard",  # Ores2

        "Fish1", "Fish2", "Fish3", "Fish4", # Small Fish
        "Fish5", "Fish6", "Fish7", "Fish8",  # Medium Fish
        "Fish9", "Fish10", "Fish11", "Fish13", "Fish12",  # Large Fish

        "Bug1", "Bug2", "Bug3", "Bug4",  # W2 Bugs
        "Bug5", "Bug6", "Bug7", "Bug8",  # W3-4 Bugs
        "Bug9", "Bug11", "Bug10", "Bug12", "Bug13",  # W5-6 Bugs
    ],
    "Other Skilling Resources": [
        "CraftMat1", "CraftMat5", "CraftMat6", "CraftMat7", "CraftMat8", "CraftMat9", "CraftMat10", "CraftMat11", "CraftMat12", "CraftMat13",  #Anvil1
        "CraftMat14",
        "Critter1", "Critter2", "Critter3", "Critter4", "Critter5", "Critter6",  #Critter1
        "Critter7", "Critter8", "Critter9", "Critter10", "Critter11",
        "Critter1A", "Critter2A",  "Critter3A", "Critter4A", "Critter5A", "Critter6A", "Critter7A", "Critter8A",  #ShinyCritter1
        "Critter9A", "Critter10A", "Critter11A",  #ShinyCritter2
        "Soul1", "Soul2", "Soul3", "Soul4", "Soul5", "Soul6", "Soul7",  #WorshipSouls
        "CopperBar", "IronBar", "GoldBar", "PlatBar", "DementiaBar", "VoidBar", "LustreBar",  #SmeltedBars1
        "StarfireBar", "DreadloBar", "MarbleBar", "GodshardBar",  #SmeltedBars2
        "Bullet", "BulletB", "FoodMining1", "FoodFish1", "FoodCatch1", "Peanut",  #Crafted1
        "Quest68", "Bullet3", "FoodChoppin1", "EquipmentSmithingTabs2",  #Crafted2
        "PeanutG",  #Gold Peanut Crafted
        "FoodTrapping1", "FoodWorship1",  # Critter Numnums and Soulble Gum Crafted
        "Refinery1", "Refinery2", "Refinery3", "Refinery4", "Refinery5", "Refinery6"
    ],
    "Vendor Shops": [
        "FoodHealth14", "FoodHealth15", "FoodHealth16", "FoodHealth17", "FoodHealth12", "FoodHealth13", "FoodPotOr4", "FoodPotGr4", "FoodPotRe4",
        "FoodPotYe4", "OilBarrel6", "OilBarrel7", "FoodHealth4", "FoodHealth9", "FoodHealth11", "Quest19", "CraftMat3",  # Sorted by daily quantity
        # "FoodHealth4", "Quest19", #W2
        # "FoodHealth11", "FoodHealth9", "FoodPotGr3", #W3
        # "FoodHealth12", "FoodHealth13", "FoodPotOr4", "FoodPotGr4", "FoodPotRe4", "FoodPotYe4", #W4
        # "OilBarrel6", "FoodHealth14", "FoodHealth15", #W5 shop
        # "FoodHealth16", "FoodHealth17", "OilBarrel7", #W6 Shop
    ],
    "Misc": [
        "FoodPotGr3",  #Decent Speed from W3 Shop + Sir Stache
        "FoodPotRe2",  #Average Life Potion from W2 Shop + Gigafrogs

        "FoodPotRe1",  #Small Life Potion from W1 Sewers and Tree mobs, not crystals
        "ButterBar",  #Catching Butterflies
        "FoodPotMana3",  #Decent Mana Potion from Bloques
        "OilBarrel2",  # Slime Barrel, 1 in 3334
        "DesertC2b",  # Ghost, 1 in 2k
        "Quest78",  # Equinox Mirror
        "Key2", "Key3"  # Efaunt and Chizoar keys
    ],
    "Cheater": [
        "SilverPen", "Ladle",
        "Sewers1b", "TreeInterior1b", "BabaYagaETC", "JobApplication",  # W1 Rare Drops
        "DesertA1b", "DesertA3b", "MidnightCookie",  # W2 Rare Drops
        "SnowA2a", "SnowB2a", "SnowC4a",  # W3 Rare Drops
        "GalaxyA2b", "GalaxyC1b",  # W4 Rare Drops
        "LavaA1b", "LavaA5b", "LavaB3b",  # W5 Rare Drops
        "SpiA2b", "SpiB2b",  # W6 Rare Drops
        "EfauntDrop1", "EfauntDrop2", "Chiz0", "Chiz1", "TrollPart", "KrukPart", "KrukPart2",  # World Boss Materials
        "CraftMat2",  # Crimson String
        "OilBarrel1", "OilBarrel3", "OilBarrel4", "OilBarrel5",  # Oil Barrels
        "PureWater2",  # Alchemy Dense water
        "Quest1", "Quest2", "Quest5", "Quest6", "Quest8", "Quest10", "Quest11", "Quest13", "Quest16", "Quest17", "Quest18", "Quest20", "Quest25",
        "Quest26", "Quest27", "Quest28", "Quest29", "Quest30", "Quest31", "Quest33", "Quest34", "Quest36", "Quest37", "Quest38", "Quest39", "Quest40",
        "Quest41", "Quest42", "Quest43", "Quest44", "Quest45", "Quest46", "Quest47", "Quest48", "Quest49", "Quest50", "Quest9",
        "Mayo", "Trash", "Trash2", "Trash3",  # Treasure Hunt rewards
        "Meatloaf", "FoodHealth5",  #Small quantity foods
        "BobJoePickle", "BallJoePickle", "BoneJoePickle",  #Pickles
        "FoodPotYe1", "FoodPotYe3",  # EXP 1 and 3
        "FoodEvent1", "FoodEvent2", "FoodEvent3", "FoodEvent4", "FoodEvent5", "FoodEvent6", "FoodEvent7", "FoodEvent8",  # Event Foods
        "Pearl1", "Pearl2", "Pearl3", "Pearl4", "Pearl5", "Pearl6",  # Skilling Speed Pearls, EXP pearls
        "Line1", "Line2", "Line3", "Line4", "Line5", "Line6", "Line7", "Line8", "Line9", "Line10", "Line11", "Line12", "Line13", "Line14",  # Fishing Lines
        "ExpBalloon1", "ExpBalloon2", "ExpBalloon3",  # Experience Balloons
        "Timecandy1", "Timecandy2", "Timecandy3", "Timecandy4", "Timecandy5", "Timecandy6", "Timecandy7", "Timecandy8", "Timecandy9",  # Time Candies
        "PetEgg", "Whetstone", "Quest72", "Quest73", "Quest76", "Quest77",  # Other Time Skips
        "Quest70", "Quest71", "Quest75", "Gfoodcoupon", "ItemsCoupon1", "ItemsCoupon2",  # Loot Bags
        "FoodHealth8", "Quest69", "Quest74",  # Unobtainables
        "EquipmentStatues6", "EquipmentStatues15",  # Kachow and Bullseye
        "EquipmentStatues8", "EquipmentStatues9", "EquipmentStatues10", "EquipmentStatues11", "EquipmentStatues12", "EquipmentStatues13",  # W2 Statues
        "EquipmentStatues16", "EquipmentStatues17", "EquipmentStatues18", "EquipmentStatues19",  # W3 Statues
        "EquipmentStatues20", "EquipmentStatues21", "EquipmentStatues22", "EquipmentStatues23", "EquipmentStatues24",
        "EquipmentStatues25",  # W4 and W5 Statues
        "FoodG1", "FoodG2", "FoodG3", "FoodG4", "FoodG5", "FoodG6", "FoodG7", "FoodG8", "FoodG10",  # Gold Foods
        "ResetFrag", "ResetCompleted", "ResetCompletedS", "ClassSwap",
        "ClassSwapB", "ResetBox",
    ]
}

card_data = {
    "Blunder Hills": {
        "Crystal0": ["Crystal Carrot", 3],
        "acorn": ["Nutto", 10],
        "beanG": ["Bored Bean", 7],
        "branch": ["Walking Stick", 10],
        "carrotO": ["Carrotman", 10],
        "frogBIG": ["Gigafrog", 10],
        "frogG": ["Frog", 6],
        "goblinG": ["Glublin", 10],
        "mushG": ["Green Mushroom", 5],
        "mushR": ["Red Mushroom", 10],
        "mushW": ["Wood Mushroom", 10],
        "plank": ["Wode Board", 10],
        "poopSmall": ["Poop", 10],
        "ratB": ["Rat", 10],
        "slimeG": ["Slime", 8],
        "snakeG": ["Baby Boa", 9],
    },
    "Yum-Yum Desert": {
        "Bandit_Bob": ["Bandit Bob", 1],
        "Crystal1": ["Crystal Crabal", 3],
        "coconut": ["Mafioso", 10],
        "crabcake": ["Crabcake", 10],
        "jarSand": ["Sandy Pot", 10],
        "mimicA": ["Mimic", 10],
        "moonman": ["Moonmoon", 10],
        "pincermin": ["Pincermin", 10],
        "potato": ["Mashed Potato", 10],
        "sandcastle": ["Sand Castle", 10],
        "sandgiant": ["Sand Giant", 10],
        "shovelR": ["Dig Doug", 10],
        "snailZ": ["Snelbie", 10],
        "steak": ["Tyson", 10],
    },
    "Easy Resources": {
        "BirchTree": ["Bleach Logs", 10],
        "Bug1": ["Fly", 10],
        "Bug2": ["Butterfly", 10],
        "Copper": ["Copper Ore", 10],
        "Fish1": ["Goldfish", 10],
        "Fish2": ["Hermit Can", 10],
        "Fish3": ["Jellyfish", 10],
        "ForestTree": ["Forest Fibres", 10],
        "ForgeA": ["Fire Forge", 10],
        "Gold": ["Gold Ore", 10],
        "Iron": ["Iron Ore", 10],
        "JungleTree": ["Jungle Logs", 10],
        "OakTree": ["Oak Logs", 10],
    },
    "Medium Resources": {
        "Bug3": ["Sentient Cereal", 10],
        "Bug4": ["Fruitfly", 10],
        "CritterCard1": ["Froge", 4],
        "CritterCard2": ["Crabbo", 4],
        "CritterCard3": ["Scorpie", 4],
        "Dementia": ["Dementia Ore", 10],
        "Fish4": ["Bloach", 10],
        "ForgeB": ["Cinder Forge", 10],
        "PalmTree": ["Tropilogs", 10],
        "Plat": ["Platinum Ore", 10],
        "SoulCard1": ["Forest Soul", 3],
        "SoulCard2": ["Dune Soul", 3],
        "StumpTree": ["Veiny Logs", 10],
        "ToiletTree": ["Potty Rolls", 10],
        "Void": ["Void Ore", 10],
    },
    "Frostbite Tundra": {
        "Crystal2": ["Crystal Cattle", 10],
        "bloque": ["Bloque", 14],
        "eye": ["Neyeptune", 17],
        "flake": ["Frost Flake", 12],
        "glass": ["Quenchie", 17],
        "mamoth": ["Mamooth", 15],
        "penguin": ["Penguin", 15],
        "ram": ["Dedotated Ram", 20],
        "sheep": ["Sheepie", 11],
        "skele": ["Xylobone", 15],
        "skele2": ["Bloodbone", 15],
        "snakeB": ["Cryosnake", 17],
        "snowball": ["Snowman", 15],
        "speaker": ["Bop Box", 17],
        "stache": ["Sir Stache", 13],
        "thermostat": ["Thermister", 15],
    },
    "Hard Resources": {
        "AlienTree": ["Alien Hive Chunk", 10],
        "Bug10": ["Dust Mote", 15],
        "Bug12": ["Ladybug", 15],
        "Bug13": ["Firefly", 15],
        "Bug5": ["Mosquisnow", 10],
        "Bug6": ["Flycicle", 10],
        "Bug7": ["Worker Bee", 10],
        "Bug8": ["Fairy", 10],
        "Bug9": ["Scarab", 12],
        "CritterCard10": ["Blobfish", 12],
        "CritterCard4": ["Mousey", 4],
        "CritterCard5": ["Owlio", 4],
        "CritterCard6": ["Pingy", 5],
        "CritterCard7": ["Bunny", 6],
        "CritterCard8": ["Dung Beat", 7],
        "CritterCard9": ["Honker", 9],
        "Dreadlo": ["Dreadlo Ore", 15],
        "Fish10": ["Shellfish", 18],
        "Fish11": ["Jumbo Shrimp", 24],
        "Fish12": ["Caulifish", 30],
        "Fish5": ["Skelefish", 8],
        "Fish6": ["Sand Shark", 10],
        "Fish7": ["Manta Ray", 10],
        "Fish8": ["Kraken", 10],
        "Fish9": ["Icefish", 15],
        "Godshard": ["Godshard Ore", 400],
        "Lustre": ["Lustre Ore", 10],
        "SaharanFoal": ["Tundra Logs", 10],
        "SoulCard3": ["Rooted Soul", 3],
        "SoulCard4": ["Frigid Soul", 4],
        "SoulCard5": ["Squishy Soul", 5],
        "SoulCard6": ["Oozie Soul", 7],
        "SoulCard7": ["Breezy Soul", 7],
        "Starfire": ["Starfire Ore", 12],
        "Tree10": ["Dandielogs", 15],
        "Tree12": ["Bamboo Logs", 15],
        "Tree13": ["Effervescent Logs", 15],
        "Tree7": ["Wispy Lumber", 10],
        "Tree8": ["Cubed Logs", 10],
        "Tree9": ["Maple Logs", 12],
    },
    "Hyperion Nebula": {
        "Crystal3": ["Crystal Custard", 10],
        "demonP": ["Demon Genie", 19],
        "mushP": ["Purp Mushroom", 15],
        "w4a2": ["TV", 17],
        "w4a3": ["Donut", 18],
        "w4b1": ["Flying Worm", 21],
        "w4b2": ["Soda Can", 20],
        "w4b3": ["Gelatinous Cuboid", 22],
        "w4b4": ["Choccie", 23],
        "w4b5": ["Biggole Wurm", 24],
        "w4c1": ["Clammie", 26],
        "w4c2": ["Octodar", 27],
        "w4c3": ["Flombeige", 28],
        "w4c4": ["Stilted Seeker", 30],
    },

    "Smolderin' Plateau": {
        "Crystal4": ["Crystal Capybara", 15],
        "w5a1": ["Suggma", 25],
        "w5a2": ["Maccie", 28],
        "w5a3": ["Mister Brightside", 32],
        "w5a4": ["Cheese Nub", 35],
        "w5a5": ["Stiltmole", 45],
        "w5b1": ["Molti", 48],
        "w5b2": ["Purgatory Stalker", 52],
        "w5b3": ["Citringe", 60],
        "w5b4": ["Lampar", 65],
        "w5b5": ["Fire Spirit", 70],
        "w5b6": ["Biggole Mole", 75],
        "w5c1": ["Crawler", 80],
        "w5c2": ["Tremor Wurm", 100],
    },
    "Spirited Valley": {
        "Crystal5": ["Crystal Candalight", 5000],
        "w6a1": ["Sprout Spirit", 50],
        "w6a2": ["Ricecake", 60],
        "w6a3": ["River Spirit", 75],
        "w6a4": ["Baby Troll", 85],
        "w6a5": ["Woodlin Spirit", 100],
        "w6b1": ["Bamboo Spirit", 150],
        "w6b2": ["Lantern Spirit", 170],
        "w6b3": ["Mama Troll", 200],
        "w6b4": ["Leek Spirit", 250],
        "w6c1": ["Ceramic Spirit", 400],
        "w6c2": ["Skydoggie Spirit", 500],
        "w6d1": ["Royal Egg", 900],
        "w6d2": ["Minichief Spirit", 1300],
        "w6d3": ["Samurai Guardian", 2500],
    },
    "Dungeons": {
        "cactus": ["Cactopunk", 2],
        "frogD": ["Globohopper", 2],
        "frogGG": ["Eldritch Croaker", 5],
        "frogGR": ["Grandfrogger", 1.5],
        "frogGR2": ["Rotting Grandfrogger", 1.5],
        "frogGR3": ["Forlorn Grandfrogger", 1.5],
        "frogGR4": ["Vengeful Grandfrogger", 1],
        "frogP": ["Poisonic Frog", 1.5],
        "frogR": ["Lava Slimer", 2],
        "frogW": ["Chromatium Frog", 3],
        "frogY": ["King Frog", 2],
        "iceBossZ": ["Glaciaxus", 2],
        "iceBossZ2": ["Golden Glaciaxus", 1.5],
        "iceBossZ3": ["Caustic Glaciaxus", 1.5],
        "iceknight": ["Ice Guard", 8],
        "potatoB": ["Crescent Spud", 5],
        "rocky": ["Grumblo", 2],
        "snakeZ": ["Snakenhotep", 1.5],
        "snakeZ2": ["Enraged Snakenhotep", 1.5],
        "snakeZ3": ["Inevitable Snakenhotep", 1.5],
        "steakR": ["Beefie", 2],
        "target": ["Target", 2],
        "totem": ["Lazlo", 2],
    },
    "Bosses n Nightmares": {
        "Boss2A": ["Efaunt", 1.5],
        "Boss2B": ["Chaotic Efaunt", 1.5],
        "Boss2C": ["Gilded Efaunt", 11],
        "Boss3A": ["Chizoar", 1.5],
        "Boss3B": ["Chaotic Chizoar", 1.5],
        "Boss3C": ["Blighted Chizoar", 12],
        "Boss4A": ["Massive Troll", 2],
        "Boss4B": ["Chaotic Troll", 2],
        "Boss4C": ["Blitzkrieg Troll", 4],
        "Boss5A": ["Kattlekruk", 3],
        "Boss5B": ["Chaotic Kattlekruk", 4],
        "Boss5C": ["Sacrilegious Kattlekruk", 5],
        "Boss6A": ["Emperor", 6],
        "Boss6B": ["Chaotic Emperor", 9],
        "Boss6C": ["Sovereign Emperor", 13],
        "babaHour": ["Biggie Hours", 1.5],
        "babaMummy": ["King Doot", 1.5],
        "babayaga": ["Baba Yaga", 1.5],
        "mini3a": ["Dilapidated Slush", 5],
        "mini4a": ["Mutated Mush", 5],
        "poopBig": ["Dr Defecaus", 1.5],
        "poopD": ["Boop", 1],
        "wolfA": ["Amarok", 1.5],
        "wolfB": ["Chaotic Amarok", 1.5],
        "wolfC": ["Radiant Amarok", 10],
    },
    "Events": {
        "EasterEvent1": ["Egggulyte", 1.5],
        "EasterEvent2": ["Egg Capsule", 1.5],
        "SummerEvent1": ["Coastiolyte", 8],
        "SummerEvent2": ["Summer Spirit", 8],
        "crabcakeB": ["Mr Blueberry", 4],
        "fallEvent1": ["Falloween Pumpkin", 3],
        "ghost": ["Ghost (Event)", 2],
        "loveEvent": ["Loveulyte", 1.5],
        "loveEvent2": ["Chocco Box", 1.5],
        "loveEvent3": ["Giant Rose", 1.5],
        "sheepB": ["Floofie", 3],
        "shovelY": ["Plasti Doug", 4],
        "slimeR": ["Valentslime", 2],
        "snakeY": ["Shell Snake", 3],
        "springEvent1": ["Bubbulyte", 1],
        "springEvent2": ["Spring Splendor", 1],
        "xmasEvent": ["Giftmas Blobulyte", 1.5],
        "xmasEvent2": ["Meaning of Giftmas", 1.5],
        "xmasEvent3": ["Golden Giftmas Box", 1],
    },
}

maxTiersPerGroup = 3
numberOfArtifacts = 33  # As of v2.03
numberOfArtifactTiers = 4  # As of v2.03
currentMaxChestsSum = 45  # As of v2.0
maxDreams = 31
maxCookingTables = 10
maxMeals = 67
maxMealLevel = 90
numberOfSecretClasses = 3

humanReadableClasses = {
    1: "Beginner",
    2: "Journeyman",
    3: "Maestro",
    4: "Voidwalker",
    5: "Infinilyte",
    6: "Rage Basics",
    7: "Warrior",
    8: "Barbarian",
    9: "Squire",
    10: "Blood Berserker",
    11: "Death Bringer",
    12: "Divine Knight",
    13: "Royal Guardian",
    18: "Calm Basics",
    19: "Archer",
    20: "Bowman",
    21: "Hunter",
    22: "Siege Breaker",
    23: "Mayheim",
    24: "Wind Walker",
    25: "Beast Master",
    30: "Savvy Basics",
    31: "Mage",
    32: "Wizard",
    33: "Shaman",
    34: "Elemental Sorcerer",
    35: "Spiritual Monk",
    36: "Bubonic Conjuror",
    37: "Arcane Cultist"
}

switches = [
    {
        "label": "Autoloot purchased",
        "name": "autoloot",
        "true": "",
        "false": "",
    },
    {
        "label": "Sheepie pet acquired",
        "name": "sheepie",
        "true": "",
        "false": "",
    },
    {
        "label": "Doot pet acquired",
        "name": "doot",
        "true": "",
        "false": "",
    },
    {
        "label": "Order groups by tier",
        "name": "order_tiers",
        "true": "",
        "false": "",
    },
    {
        "label": "Show progress bars",
        "name": "progress_bars",
        "true": "",
        "false": "",
    },
    {
        "label": "Handedness",
        "name": "handedness",
        "true": "L",
        "false": "R",
    },
    # {"label": "Legacy style", "name": "legacy", "true": "", "false": ""},
]

skillIndexList = ["Combat",
                  "Mining", "Smithing", "Choppin",
                  "Fishing", "Alchemy", "Catching",
                  "Trapping", "Construction", "Worship",
                  "Cooking", "Breeding", "Lab",
                  "Sailing", "Divinity", "Gaming",
                  "Farming", "Sneaking", "Summoning"]
emptySkillList = [0] * 25

expectedInventoryBagValuesDict = {
    0:1,
    1:1,
    2:1,
    3:2,
    4:2,
    5:2,
    6:2,
    7:2,
    20:4,
    21:4,
    22:4,
    23:4,
    24:4,
    25:4,
    100:2,
    101:2,
    102:4,
    103:4,
    104:1,
    105:1,
    106:1,
    107:1,
    108:2,
    109:3,
    110:1,
    111:3,
}
expectedStorageChestValuesDict = {
    0:3,
    1:3,
    2:3,
    3:3,
    4:3,
    5:4,
    6:4,
    7:4,
    8:4,
    9:5,
    10:5,
    11:5,
    12:5,
    13:6,
    14:5,
    15:6,
    16:6,
    17:6,
    18:6,
    19:7,
    20:7,
    21:8,
    22:9,
    23:9,
    24:9,
    25:9,
    26:9,
    27:10,
    30:9,
    31:9,
    32:9,
    33:9,
    34:9,
    35:9,
    36:9,
    37:9,
    38:9,
    39:9,
    40:9,
    41:9,
    100:3,
    101:3,
    102:4,
    103:4,
    104:3,
}

jade_emporium = [
  {
    "name": "Quick Ref Access",
    "bonus": "Adds the Sneaking skill to your QuickRef menu! Manage your Ninja Twins from anywhere!"
  },
  {
    "name": "Gold Food Beanstalk",
    "bonus": "Grows a giant beanstalk behind the ninja castle! Drop a stack of 10,000 Gold Food to add it with the beanstalk and permanently gain its bonus!"
  },
  {
    "name": "Supersized Gold Beanstacking",
    "bonus": "You can now drop a stack of 100,000 Gold Food to supersize it! This will obviously give a bigger bonus, and will even enlargen the food on the stalk!"
  },
  {
    "name": "Charmed, I'm Sure",
    "bonus": "All your Ninja Twins can now equip two of the same charm at once!"
  },
  {
    "name": "Mob Cosplay Craze",
    "bonus": "Certain monsters in World 6 will now have a rare chance to drop Ninja Hats, but only the ones you've found already from the Ninja Castle!"
  },
  {
    "name": "Level Exemption",
    "bonus": "Completely and utterly removes the UNDER-LEVELED bonus reduction of all stamps in your collection, now and forever. Amen."
  },
  {
    "name": "Gaming to the MAX",
    "bonus": "All plant types in Gaming have +1 Max Evolution, but this one is 50,000x rarer than normal and will make you wonder if evolution is even real (it is)"
  },
  {
    "name": "Revenge of the Pickle",
    "bonus": "Adds a new boss page to the left of World 1 in Deathnote. Each BoneJoePickle in your inventory counts as +1 Boss Deathnote Kill!"
  },
  {
    "name": "The Artifact Matrix",
    "bonus": "Extends the Laboratory Event Horizon, adding another bonus to connect to! In particular, a boost to Artifact Find Chance!"
  },
  {
    "name": "The Slab Matrix",
    "bonus": "Further extends the Laboratory Event Horizon, adding another bonus to connect to! In particular, a boost to all bonuses from the Slab!"
  },
  {
    "name": "The Spirit Matrix",
    "bonus": "Even further extends the Laboratory Event Horizon, adding another bonus to connect to! In particular, a boost to W6 Skill exp gain!"
  },
  {
    "name": "The Crop Matrix",
    "bonus": "Yet again even further extends the Laboratory Event Horizon, adding another bonus to connect to! In particular, a boost to Crop Depot!"
  },
  {
    "name": "MSA Expander I",
    "bonus": "Adds a new bonus type to the Miniature Soul Apparatus in World 3, specifically Farming EXP!"
  },
  {
    "name": "MSA Expander II",
    "bonus": "Adds a new bonus type to the Miniature Soul Apparatus in World 3, specifically Jade Coin Gain!"
  },
  {
    "name": "MSA Expander III",
    "bonus": "Adds a new bonus type to the Miniature Soul Apparatus in World 3, specifically All Essence Gain!"
  },
  {
    "name": "Deal Sweetening",
    "bonus": "Earn +25% more Magic Beans from the mysterious Legumulyte bean merchant found in the Troll Broodnest map."
  },
  {
    "name": "No Meal Left Behind",
    "bonus": "Every 24 hours, your lowest level Meal gets +1 Lv. This only works on Meals Lv 5 or higher, and doesn't trigger on days you don't play."
  },
  {
    "name": "Jade Coin Magnetism",
    "bonus": "Adds a new bonus of +5% Jade Coin Gain per 10 items found after 1000 items, as shown at The Slab in World 5."
  },
  {
    "name": "Essence Confetti",
    "bonus": "Adds a new bonus of +3% All Essence Gain per 10 items found after 1000 items, as shown at The Slab in World 5."
  },
  {
    "name": "Shrine Collective Bargaining Agreement",
    "bonus": "Shrines no longer lose EXP when moved around, so you can finally bring those baddies out of retirement!"
  },
  {
    "name": "Papa Blob's Quality Guarantee",
    "bonus": "Increases the Max Level of all cooking meals by +10. Better meals, better levels, Papa Blob's."
  },
  {
    "name": "Chef Geustloaf's Cutting Edge Philosophy",
    "bonus": "Increases the Max Level of all cooking meals by +10 again! But oh hoho, you sir are no Chef Geustloaf! Good luck cooking to these LVs!"
  },
  {
    "name": "Crop Depot Scientist",
    "bonus": "Employs a friendly scientist blobulyte to keep a Data Sheet of all the crops you've ever found!"
  },
  {
    "name": "Science Environmentally Sourced Pencil",
    "bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '+15% Cash from Mobs' per crop found!"
  },
  {
    "name": "Science Pen",
    "bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '1.02x Plant Evolution Chance in Gaming (multiplicative)' per Crop!"
  },
  {
    "name": "Science Marker",
    "bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '+8% Jade Coin Gain' per Crop!"
  },
  {
    "name": "Science Featherpen",
    "bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '1.10x Cooking Speed (multiplicative)' per Crop!"
  },
  {
    "name": "Reinforced Science Pencil",
    "bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '+20% Total Damage' per Crop!"
  },
  {
    "name": "Science Crayon",
    "bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '+7% Shiny Pet Lv Up Rate and Pet Breeding Rate' per Crop!"
  },
  {
    "name": "Science Paintbrush",
    "bonus": "Adds a new bonus type to your crop scientist's Data Sheet! Specifically '+0.1 Base Critter caught in Trapping' per Crop!"
  },
  {
    "name": "New Critter",
    "bonus": "Unlocks a new critter type to capture! These have their own very special vial in Alchemy."
  },
  {
    "name": "Ionized Sigils",
    "bonus": "Sigils can now be upgraded a 3rd time. Push past lame ol' yellow, and further increasing those sigil boosts!"
  },
  {
    "name": "The Endercaptain",
    "bonus": "Adds the Endercaptain to Recruitment pool. They're very rare, and have a hidden account-wide +25% Loot Multi and Artifact Find."
  },
  {
    "name": "True Godly Blessings",
    "bonus": "All Divinity Gods give 1.05x higher Blessing bonus per God Rank. Whats a Blessing bonus? Select a god, it's the one on the bottom, go look."
  },
  {
    "name": "Brighter Lighthouse Bulb",
    "bonus": "You can now find 3 additional Artifacts from The Edge island."
  },
  {
    "name": "Sovereign Artifacts",
    "bonus": "You can now find Sovereign Artifacts from sailing, but only if you've found the Eldritch form first."
  },
  {
    "name": "New Bribes",
    "bonus": "Mr. Pigibank is up to no good once again, and he's looking to get some funding from his favorite patron... you. Well, your wallet specifically."
  },
  {
    "name": "Laboratory Bling",
    "bonus": "Adds 3 new Jewels to unlock at the Jewel Spinner in W4 Town. Or, get one for free every 700 total Lab LV as shown in Rift Skill Mastery."
  }
]
