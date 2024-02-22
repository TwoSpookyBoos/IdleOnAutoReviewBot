def setDefaultTiers():
    defaultTiers = {}
    defaultTiers['Bribes'] = [
        #int tier, int w1purchased, int w2purchased, int w3purchased, int w4purchased, int trashIslandpurchased, str notes
        [0, 0, -7, -7, -6, -8, ""],
        [1, 6, -7, -7, -6, -8, "by end of W1."],
        [2, 6, 7, -7, -6, -8, "by end of W2."],
        [3, 6, 7, 7, -6, -8, "by end of W3."],
        [4, 6, 7, 7, 6, -8, "by end of W4."],
        [5, 6, 7, 7, 6, 7, "by end of W5, after unlocking the Bribe from Trash Island."], #The 8th bribe in w5 can't be purchased yet
        ]
    defaultTiers['Stamps'] = [
        #int Tier, int Total Stamp Level, str Required combat stamps, str Required Skill stamps, str Required Misc stamps, dict Specific stamp levels, str Notes
        [0, 0, "", "", "", {}, "Just level up any stamp you can afford!"],
        [1, 50, "", "", "", {}, "Just level up any stamp you can afford!"],
        [2, 100, "", "", "", {}, "Just level up any stamp you can afford!"],
        [3, 150, "2,3,4,5,11", "5", "", {}, "W1 town and W1 Tiki shop both sell stamps!"],
        [4, 200, "8,13,14", "3,16,18", "17", {}, "Expected progression roughly near the start of World 3. Some of these required stamps are drops from enemies or quest rewards. Use the Wiki to find their sources!"],
        [5, 250, "6,7,9", "2,7", "0", {'Pickaxe Stamp':25, 'Hatchet Stamp':25}, ""],
        [6, 300, "17,18,20", "25", "5", {}, ""],
        [7, 400, "", "8", "", {'Pickaxe Stamp':35, 'Hatchet Stamp':35}, ""],
        [8, 500, "15,16,21", "14,17", "14,19", {'Drippy Drop Stamp':30}, ""],
        [9, 600, "27", "10", "1,2", {'Mason Jar Stamp':12}, ""],
        [10, 700, "", "4,6,9,11,12,15,22,24,26", "", {'Drippy Drop Stamp':40, 'Matty Bag Stamp':50}, ""],
        [11, 800, "10,12", "29,37,40", "", {'Pickaxe Stamp':45, 'Hatchet Stamp':45, 'Mason Jar Stamp':24,}, ""],
        [12, 900, "23,24", "13,20,30,46", "8", {'Drippy Drop Stamp':50}, ""],
        [13, 1000, "28", "19,21,36", "13", {'Pickaxe Stamp':55, 'Hatchet Stamp':55, 'Card Stamp':50}, ""],
        [14, 1500, "31", "35,39", "21", {'Matty Bag Stamp':100, 'Crystallin':60}, ""],
        [15, 2000, "25,29", "41", "6,20", {'Pickaxe Stamp':65, 'Hatchet Stamp':65, 'Card Stamp':100}, ""],
        [16, 2500, "33", "38,42", "15", {'Golden Apple Stamp':28}, ""],
        [17, 3000, "36", "43,44,45", "", {'Bugsack Stamp':80, 'Bag o Heads Stamp':80},  ""],
        [18, 3500, "", "", "", {'Pickaxe Stamp':75, 'Hatchet Stamp':75, 'Drippy Drop Stamp':90, 'Crystallin':100}, ""],
        [19, 4000, "", "", "", {'Matty Bag Stamp':150}, ""],
        [20, 4500, "", "", "18", {'Card Stamp':150, 'Ladle Stamp':100}, ""],
        [21, 5000, "30,32", "23", "", {'Pickaxe Stamp':85, 'Hatchet Stamp':85, 'Mason Jar Stamp':52, 'Golden Apple Stamp':40}, ""],
        [22, 5500, "", "", "", {'Bugsack Stamp':120, 'Bag o Heads Stamp':120}, ""],
        [23, 6000, "19,26,34", "33", "", {'Matty Bag Stamp':200, 'Crystallin':150}, ""],
        [24, 6500, "36", "", "", {'Drippy Drop Stamp':100, 'Ladle Stamp':150}, ""],
        [25, 7000, "35", "", "", {'Pickaxe Stamp':95, 'Hatchet Stamp':95, 'Golden Apple Stamp':60, 'Multitool Stamp':100}, ""],
        [26, 7500, "", "", "", {'Ladle Stamp':180}, ""],
        [27, 8000, "", "", "", {'Matty Bag Stamp':280, 'Multitool Stamp':150}, ""],
        [28, 8400, "", "", "", {'Pickaxe Stamp':105, 'Hatchet Stamp':105, 'Mason Jar Stamp':92, 'Crystallin':200, 'Bugsack Stamp':152, 'Bag o Heads Stamp':152,}, ""],
        [29, 8600, "", "", "", {'Drippy Drop Stamp':110, 'Matty Bag Stamp':310}, ""],
        [30, 8800, "", "", "", {'Card Stamp':200, 'Crystallin':250}, ""],
        [31, 9000, "", "", "", {'Golden Apple Stamp':80}, "Guaranteed daily Gilded Stamp at 10k"],
        [32, 9200, "", "", "", {'Mason Jar Stamp':124}, ""],
        [33, 9400, "", "", "", {'Bugsack Stamp':184, 'Bag o Heads Stamp':184}, ""],
        [34, 9600, "", "", "", {'Golden Apple Stamp':100, 'Multitool Stamp':210}, ""],
        [35, 9800, "37", "", "", {'Golden Sixes Stamp':150}, ""],
        [36, 10000, "38, 22", "31", "", {'Golden Sixes Stamp':190}, ""],
        [37, 11000, "", "", "", {'Maxo Slappo Stamp':98, 'Sashe Sidestamp':98, 'Intellectostampo':98}, ""]
        ]
    defaultTiers['Smithing'] = [
        #int tier, int Cash Points Purchased, int Monster Points Purchased, int Forge Totals, str Notes
        [0, 0,   0,   0,   ""],
        [1, 20,  85,  60,  "all W1 enemies"],
        [2, 60,  150, 120, "early W2 enemies through Pincermin"],
        [3, 100, 225, 180, "all W2 enemies"],
        [4, 150, 350, 240, "most W3 enemies, excluding Dedotated Rams"],
        [5, 200, 500, 291, "early W4 enemies through Soda Cans"],
        [6, 600, 700, 291, "all W4 enemies"]
        ]
    defaultTiers['Alchemy Bubbles'] = [
        #int tier, int TotalBubblesUnlocked, dict {OrangeSampleBubbles}, dict {GreenSampleBubbles}, dict {PurpleSampleBubbles}, dict {UtilityBubbles}, str BubbleValuePercentage, str Notes
        [0,  0, {}, {}, {}, {}, "0%", ""],
        [1,  10,  {'Roid Ragin': 12,   'Warriors Rule': 6,    'Hearty Diggy': 12,   'Wyoming Blood': 6,   'Sploosh Sploosh': 6,   'Stronk Tools': 8},                                                   {'Swift Steppin': 12,  'Archer or Bust': 6,   'Sanic Tools': 8,  'Bug^2': 6},                                                           {'Stable Jenius': 12,  'Mage is Best': 6,    'Hocus Choppus': 12,   'Molto Loggo': 6,   'Le Brain Tools': 8},                                               {'FMJ':5, 'Shaquracy':5, 'Prowesessary':7, 'Hammer Hammer':6}, "10%", "These are MINIMUM recommended Utility bubbles for closing out W2. The goal for Prowesessary is an eventual 2x (or 200%) for all sources combined."],
        [2,  20,  {'Roid Ragin': 25,   'Warriors Rule': 13,   'Hearty Diggy': 25,   'Wyoming Blood': 13,  'Sploosh Sploosh': 13,  'Stronk Tools': 18},                                                  {'Swift Steppin': 25,  'Archer or Bust': 13,  'Sanic Tools': 18, 'Bug^2': 13},                                                          {'Stable Jenius': 25,  'Mage is Best': 13,   'Hocus Choppus': 25,   'Molto Loggo': 13,  'Le Brain Tools': 18},                                              {'FMJ':10, 'Shaquracy':10, 'Prowesessary':15, 'Hammer Hammer':14}, "20%", "These are MINIMUM recommended Utility bubbles for starting the W3 push. The goal for Prowesessary is an eventual 2x (or 200%) for all sources combined."],
        [3,  40,  {'Roid Ragin': 67,   'Warriors Rule': 34,   'Hearty Diggy': 67,   'Wyoming Blood': 20,  'Sploosh Sploosh': 20,  'Stronk Tools': 47},                                                  {'Swift Steppin': 67,  'Archer or Bust': 34,  'Sanic Tools': 47, 'Bug^2': 20},                                                          {'Stable Jenius': 67,  'Mage is Best': 34,   'Hocus Choppus': 67,   'Molto Loggo': 20,  'Le Brain Tools': 47},                                              {'FMJ':15, 'Shaquracy':15, 'Prowesessary':40, 'Hammer Hammer':41}, "40%", "These are MINIMUM recommended Utility bubbles for starting the W4 push. The goal for Prowesessary is an eventual 2x (or 200%) for all sources combined."],
        [4,  60,  {'Roid Ragin': 100,  'Warriors Rule': 50,   'Hearty Diggy': 100,  'Wyoming Blood': 30,  'Sploosh Sploosh': 30,  'Stronk Tools': 70},                                                  {'Swift Steppin': 100, 'Archer or Bust': 50,  'Sanic Tools': 70, 'Bug^2': 30},                                                          {'Stable Jenius': 100, 'Mage is Best': 50,   'Hocus Choppus': 100,  'Molto Loggo': 30,  'Le Brain Tools': 70},                                              {'FMJ':20, 'Shaquracy':20, 'Prowesessary':60, 'Hammer Hammer':65}, "50%", "These are MINIMUM recommended Utility bubbles for starting the W5 push. The goal for Prowesessary is an eventual 2x (or 200%) for all sources combined, and you should be hitting it right about now!"],
        [5,  80,  {'Roid Ragin': 150,  'Warriors Rule': 75,   'Hearty Diggy': 150,  'Wyoming Blood': 45,  'Sploosh Sploosh': 45,  'Stronk Tools': 105, 'Multorange': 45,   'Dream of Ironfish': 45},    {'Swift Steppin': 150, 'Archer or Bust': 75,  'Sanic Tools': 70, 'Bug^2': 45, 'Premigreen': 45, 'Fly in Mind': 60},                     {'Stable Jenius': 150, 'Mage is Best': 75,   'Hocus Choppus': 150,  'Molto Loggo': 45,  'Le Brain Tools': 105,  'Severapurple': 45,   'Tree Sleeper': 60},  {'FMJ':30, 'Shaquracy':30, 'Hammer Hammer':105}, "60%", "These are MINIMUM recommended Utility bubbles for starting the W6 push. Keep watch of your No Bubble Left Behind list (from W4 Lab) to keep cheap/easy bubbles off when possible!"],
        [6,  100, {'Roid Ragin': 234,  'Warriors Rule': 117,  'Hearty Diggy': 234,  'Wyoming Blood': 70,  'Sploosh Sploosh': 70,  'Stronk Tools': 164, 'Multorange': 70,   'Dream of Ironfish': 70},    {'Swift Steppin': 234, 'Archer or Bust': 117, 'Sanic Tools': 70, 'Bug^2': 70, 'Premigreen': 70},                                        {'Stable Jenius': 234, 'Mage is Best': 117,  'Hocus Choppus': 234,  'Molto Loggo': 70,  'Le Brain Tools': 164,  'Severapurple': 70,   'Tree Sleeper': 94},  {'Cookin Roadkill': 105}, "70%", "Cookin Roadkill 105 = 60% bubble strength. You likely can't use Cranium Cooking very often yet, but this is a prerequisite for doing so."],
        [7,  100, {'Roid Ragin': 400,  'Warriors Rule': 200,  'Hearty Diggy': 400,  'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 280, 'Multorange': 120,  'Dream of Ironfish': 120},   {'Swift Steppin': 400, 'Archer or Bust': 200, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 120},                                       {'Stable Jenius': 400, 'Mage is Best': 200,  'Hocus Choppus': 400,  'Molto Loggo': 120, 'Le Brain Tools': 280,  'Severapurple': 120,  'Tree Sleeper': 160}, {'Laaarrrryyyy': 150}, "80%", "Larry at 150 = 72% chance for +2 levels. Somewhere around level 125-150, this bubble should pass 100m Dementia Ore cost and be available to level with Boron upgrades from the W3 Atom Collider in Construction.  It should be, in my opinion, the ONLY Utility Bubble you spend these daily clicks on until it reaches 501. If you cannot afford the Particles needed to level Larry, invest into Sampling Bubbles."],
        [8,  100, {'Roid Ragin': 567,  'Warriors Rule': 284,  'Hearty Diggy': 567,  'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 397, 'Multorange': 170,  'Dream of Ironfish': 170},   {'Swift Steppin': 567, 'Archer or Bust': 284, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 170},                                       {'Stable Jenius': 567, 'Mage is Best': 284,  'Hocus Choppus': 567,  'Molto Loggo': 120, 'Le Brain Tools': 397,  'Severapurple': 170,  'Tree Sleeper': 227}, {'Laaarrrryyyy': 501}, "85%", "Larry at 501 = 100% chance for +2 levels. This can be leveled with a combination of prints as well as daily Boron upgrades from the Atom Collider."],
        [9,  100, {'Roid Ragin': 615,  'Warriors Rule': 308,  'Hearty Diggy': 615,  'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 430, 'Multorange': 185,  'Dream of Ironfish': 185},   {'Swift Steppin': 615, 'Archer or Bust': 308, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 185},                                       {'Stable Jenius': 615, 'Mage is Best': 308,  'Hocus Choppus': 615,  'Molto Loggo': 120, 'Le Brain Tools': 430,  'Severapurple': 185,  'Tree Sleeper': 246}, {'Cookin Roadkill': 630}, "86%", "Cooking Roadkill 630 = 90% bubble strength. Try to tackle the cheap levels with prints, and add Atom Clicks as needed. This will help your Bubo's Cranium Cooking really pick up in value."],
        [10, 100, {'Roid Ragin': 670,  'Warriors Rule': 335,  'Hearty Diggy': 670,  'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 469, 'Multorange': 201,  'Dream of Ironfish': 201},   {'Swift Steppin': 670, 'Archer or Bust': 335, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 201},                                       {'Stable Jenius': 670, 'Mage is Best': 335,  'Hocus Choppus': 670,  'Molto Loggo': 120, 'Le Brain Tools': 469,  'Severapurple': 201,  'Tree Sleeper': 268}, {'Startue Exp': 240}, "87%", "Startue Exp 240 = 80% bubble strength. This can be leveled with Vman prints. You'll also likely get quite a lot of Pocket Sand while farming for Glass Shards for your Mason Jar stamp. Try to at least get this 80% threshold by the time you're farming Onyx Statues."],
        [11, 100, {'Roid Ragin': 700,  'Warriors Rule': 367,  'Hearty Diggy': 734,  'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 514, 'Multorange': 220,  'Dream of Ironfish': 220},   {'Swift Steppin': 700, 'Archer or Bust': 367, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 220},                                       {'Stable Jenius': 700, 'Mage is Best': 367,  'Hocus Choppus': 734,  'Molto Loggo': 120, 'Le Brain Tools': 514,  'Severapurple': 220,  'Tree Sleeper': 294}, {'Droppin Loads': 280}, "88%", "Droppin Loads 280 = 80% bubble strength. Ideally, this should be leveled with prints but Fishing prints tend to struggle in the beginning. A few Boron upgrades won't hurt."],
        [12, 100, {'Roid Ragin': 720,  'Warriors Rule': 405,  'Hearty Diggy': 810,  'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 567, 'Multorange': 243,  'Dream of Ironfish': 243},   {'Swift Steppin': 720, 'Archer or Bust': 405, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 243},                                       {'Stable Jenius': 720, 'Mage is Best': 405,  'Hocus Choppus': 810,  'Molto Loggo': 120, 'Le Brain Tools': 567,  'Severapurple': 243,  'Tree Sleeper': 324}, {'Call Me Bob': 200}, "89%", "Call Me Bob is a linear Construction EXP bubble, so the early levels are the most impactful to your account. Vman prints can help get this into Atom range. Afterwards, it is a very valid Atom Click target"],
        [13, 100, {'Roid Ragin': 740,  'Warriors Rule': 450,  'Hearty Diggy': 900,  'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 630, 'Multorange': 270,  'Dream of Ironfish': 270},   {'Swift Steppin': 740, 'Archer or Bust': 450, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 270},                                       {'Stable Jenius': 740, 'Mage is Best': 450,  'Hocus Choppus': 900,  'Molto Loggo': 120, 'Le Brain Tools': 630,  'Severapurple': 270,  'Tree Sleeper': 360}, {'Diamond Chef': 31, 'Big P': 140, 'Big Game Hunter': 70, 'Mr Massacre': 117}, "90%", "70% broad on Utility bubbles. Many of these may not be within range to use Atom Clicks on yet. To help them level faster, try to level other cheap bubbles which will ensure No Bubble Left Behind targets these expensive bubbles instead."],
        [14, 100, {'Roid Ragin': 760,  'Warriors Rule': 506,  'Hearty Diggy': 1012, 'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 630, 'Multorange': 304,  'Dream of Ironfish': 270},   {'Swift Steppin': 760, 'Archer or Bust': 506, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 304},                                       {'Stable Jenius': 760, 'Mage is Best': 506,  'Hocus Choppus': 1012, 'Molto Loggo': 120, 'Le Brain Tools': 630,  'Severapurple': 304,  'Tree Sleeper': 360}, {'Diamond Chef': 52, 'Big P': 240, 'Big Game Hunter': 120, 'Mr Massacre': 200}, "91%", "80% broad on Utility bubbles. Some of these may not be within range to use Atom Clicks on yet. To help them level faster, try to level other cheap bubbles which will ensure No Bubble Left Behind targets these expensive bubbles instead."],
        [15, 100, {'Roid Ragin': 780,  'Warriors Rule': 575,  'Hearty Diggy': 1150, 'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 630, 'Multorange': 345,  'Dream of Ironfish': 270},   {'Swift Steppin': 780, 'Archer or Bust': 575, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 345},                                       {'Stable Jenius': 780, 'Mage is Best': 575,  'Hocus Choppus': 1150, 'Molto Loggo': 120, 'Le Brain Tools': 630,  'Severapurple': 345,  'Tree Sleeper': 360}, {'Diamond Chef': 74, 'Big P': 340, 'Carpenter': 284, 'Big Game Hunter': 170, 'Mr Massacre': 284}, "92%", "85% broad on Utility bubbles. A few of these may not be within range to use Atom Clicks on yet. To help them level faster, try to level other cheap bubbles which will ensure No Bubble Left Behind targets these expensive bubbles instead."],
        [16, 100, {'Roid Ragin': 800,  'Warriors Rule': 665,  'Hearty Diggy': 1329, 'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 630, 'Multorange': 399,  'Dream of Ironfish': 270},   {'Swift Steppin': 800, 'Archer or Bust': 665, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 399},                                       {'Stable Jenius': 800, 'Mage is Best': 665,  'Hocus Choppus': 1329, 'Molto Loggo': 120, 'Le Brain Tools': 630,  'Severapurple': 399,  'Tree Sleeper': 360}, {'Laaarrrryyyy': 900, 'Diamond Chef': 117, 'Big P': 540, 'Carpenter': 450, 'Big Game Hunter': 270, 'Mr Massacre': 450}, "93%", "90% broad on Utility bubbles. These should all be within Atom Range now. Try not to go too crazy on these until your Sampling Bubbles are all 90% first."],
        [17, 100, {'Roid Ragin': 820,  'Warriors Rule': 784,  'Hearty Diggy': 1567, 'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 630, 'Multorange': 470,  'Dream of Ironfish': 270},   {'Swift Steppin': 820, 'Archer or Bust': 784, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 470},                                       {'Stable Jenius': 820, 'Mage is Best': 784,  'Hocus Choppus': 1567, 'Molto Loggo': 120, 'Le Brain Tools': 630,  'Severapurple': 470,  'Tree Sleeper': 360}, {}, "94%", ""],
        [18, 100, {'Roid Ragin': 840,  'Warriors Rule': 950,  'Hearty Diggy': 1900, 'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 630, 'Multorange': 570,  'Dream of Ironfish': 270},   {'Swift Steppin': 840, 'Archer or Bust': 950, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 570},                                       {'Stable Jenius': 840, 'Mage is Best': 950,  'Hocus Choppus': 1900, 'Molto Loggo': 120, 'Le Brain Tools': 630,  'Severapurple': 570,  'Tree Sleeper': 360}, {}, "95%", ""],
        [19, 100, {'Roid Ragin': 860,  'Warriors Rule': 1200, 'Hearty Diggy': 2400, 'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 630, 'Multorange': 720,  'Dream of Ironfish': 270},   {'Swift Steppin': 860, 'Archer or Bust': 1200, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 570},                                      {'Stable Jenius': 860, 'Mage is Best': 1200, 'Hocus Choppus': 1900, 'Molto Loggo': 120, 'Le Brain Tools': 630,  'Severapurple': 720,  'Tree Sleeper': 360}, {}, "96%", ""],
        [20, 100, {'Roid Ragin': 880,  'Warriors Rule': 1617, 'Hearty Diggy': 3234, 'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 630, 'Multorange': 970,  'Dream of Ironfish': 270},   {'Swift Steppin': 880, 'Archer or Bust': 1617, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 570},                                      {'Stable Jenius': 880, 'Mage is Best': 1617, 'Hocus Choppus': 1900, 'Molto Loggo': 120, 'Le Brain Tools': 630,  'Severapurple': 970,  'Tree Sleeper': 360}, {}, "97%", ""],
        [21, 120, {'Roid Ragin': 900,  'Warriors Rule': 2450, 'Hearty Diggy': 4900, 'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 630, 'Multorange': 1470, 'Dream of Ironfish': 270},   {'Swift Steppin': 900, 'Archer or Bust': 2450, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 570},                                      {'Stable Jenius': 900, 'Mage is Best': 2450, 'Hocus Choppus': 1900, 'Molto Loggo': 120, 'Le Brain Tools': 630,  'Severapurple': 1470, 'Tree Sleeper': 360}, {}, "98%", ""],
        [22, 140, {'Roid Ragin': 950,  'Warriors Rule': 4950, 'Hearty Diggy': 9900, 'Wyoming Blood': 120, 'Sploosh Sploosh': 120, 'Stronk Tools': 630, 'Multorange': 2970, 'Dream of Ironfish': 270},   {'Swift Steppin': 950, 'Archer or Bust': 4950, 'Sanic Tools': 70, 'Bug^2': 120,'Premigreen': 570},                                      {'Stable Jenius': 950, 'Mage is Best': 4950, 'Hocus Choppus': 1900, 'Molto Loggo': 120, 'Le Brain Tools': 630,  'Severapurple': 2970, 'Tree Sleeper': 360}, {}, "99%", "* You've tackled the big important Utility bubbles, way to go! All previously mentioned bubbles are still great targets to level higher: Larry, Cookin Roadkill, Diamond Chef, Carpenter, Call Me Bob, Big P, Mr Massacre, Big Game Hunter, FMJ, Hammer Hammer, and more!"],
        [23, 160, {'Roid Ragin': 1000, 'Stronk Tools': 6930,  'Dream of Ironfish': 2970, 'Slabi Orefish':5940, 'Slabi Strength':5940},                                                                  {'Swift Steppin': 1000, 'Sanic Tools': 6930, 'Premigreen': 2970, 'Fly in Mind': 3960, 'Slabo Critterbug':5940, 'Slabo Agility':5940},   {'Stable Jenius': 1000, 'Hocus Choppus': 9900, 'Le Brain Tools': 6930, 'Tree Sleeper': 3960, 'Slabe Logsoul':5940, 'Slabe Wisdom':5940}, {}, "99% catchup", "You've tackled the big important Utility bubbles, way to go! All previously mentioned bubbles are still great targets to level higher: Larry, Cookin Roadkill, Diamond Chef, Carpenter, Call Me Bob, Big P, Mr Massacre, Big Game Hunter, FMJ, Hammer Hammer, and more!"],
        ]
    defaultTiers['Alchemy Vials'] = [
        #int tier, int TotalVialsUnlocked, int TotalVialsMaxed, list ParticularVials, str Notes
        [0, 10, 0, [], ""],
        [1, 14, 0, [], ". This is the number of vials requiring an unlock roll of 75 or less. "],
        [2, 19, 0, [], ". This is the number of vials requiring an unlock roll of 85 or less. "],
        [3, 27, 0, [], ". This is the number of vials requiring an unlock roll of 90 or less. "],
        [4, 33, 0, [], ". This is the number of vials requiring an unlock roll of 95 or less. "],
        [5, 38, 0, [], ". This is the number of vials requiring an unlock roll of 98 or less. "],
        [6, 51, 0, [], ". This is all vials up through W4, excluding the Arcade Pickle. "],
        [7, 63, 4, ['Copper Corona (Copper Ore)', 'Sippy Splinters (Oak Logs)', 'Jungle Juice (Jungle Logs)', 'Tea With Pea (Potty Rolls)'], ". This is all vials up through W5, excluding the Arcade Pickle. "],
        [8, 63, 8, ['Gold Guzzle (Gold Ore)', 'Seawater (Goldfish)', 'Fly In My Drink (Fly)', 'Blue Flav (Platinum Ore)'], ""],
        [9, 63, 12, ['Slug Slurp (Hermit Can)', 'Void Vial (Void Ore)', 'Ew Gross Gross (Mosquisnow)', 'The Spanish Sahara (Tundra Logs)'], ""],
        [10, 63, 16, ['Mushroom Soup (Spore Cap)', 'Maple Syrup (Maple Logs)', 'Marble Mocha (Marble Ore)', 'Skinny 0 Cal (Snake Skin)'], ""],
        [11, 63, 20, ['Long Island Tea (Sand Shark)', 'Anearful (Glublin Ear)', 'Willow Sippy (Willow Logs)', 'Dieter Drink (Bean Slices)'], ""],
        [12, 63, 24, ['Shinyfin Stew (Equinox Fish)', 'Ramificoction (Bullfrog Horn)', 'Tail Time (Rats Tail)', 'Dreamy Drink (Dream Particulate)'], ""],
        [13, 63, 28, ['Mimicraught (Megalodon Tooth)', 'Fur Refresher (Floof Ploof)', 'Etruscan Lager (Mamooth Tusk)', 'Dusted Drink (Dust Mote)'], ""],
        [14, 63, 32, ['Sippy Soul (Forest Soul)', 'Visible Ink (Pen)', 'Snow Slurry (Snow Ball)', 'Sippy Cup (Sippy Straw)'], ""],
        [15, 63, 36, ['Goosey Glug (Honker)', 'Crab Juice (Crabbo)', 'Chonker Chug (Dune Soul)', '40-40 Purity (Contact Lense)'], ""],
        [16, 63, 40, ['Bubonic Burp (Mousey)', 'Capachino (Purple Mush Cap)', 'Donut Drink (Half Eaten Donut)', 'Krakenade (Kraken)'], ""],
        [17, 63, 44, ['Calcium Carbonate (Tongue Bone)', 'Spool Sprite (Thread)', 'Choco Milkshake (Crumpled Wrapper)', 'Electrolyte (Condensed Zap)'], ""],
        [18, 63, 48, ['Ash Agua (Suggma Ashes)', 'Venison Malt (Mongo Worm Slices)', 'Thumb Pow (Trusty Nails)', 'Slowergy Drink (Frigid Soul)'], ""],
        [19, 63, 52, ['Bunny Brew (Bunny)', 'Oj Jooce (Orange Slice)', 'Spook Pint (Squishy Soul)', 'Barium Mixture (Copper Bar)'], ""],
        [20, 63, 55, ['Bloat Draft (Blobfish)', 'Barley Brew (Iron Bar)', 'Oozie Ooblek (Oozie Soul)'], " This is the last tier possible as of v1.91"],
        [21, 63, 60, ['Poison Tincture (Poison Froge)', 'Red Malt (Redox Salts)', 'Orange Malt (Explosive Salts)', 'Shaved Ice (Purple Salt)', 'Dreadnog (Dreadlo Bar)'], " This tier is impossible as of v1.91"],
        [22, 63, 64, ['Pickle Jar (BobJoePickle)', 'Ball Pickle Jar (BallJoePickle)', 'Pearl Seltzer (Pearler Shell)', 'Hampter Drippy (Hampter)'], " This tier is super impossible as of v1.91"]
        ]
    defaultTiers['Obols'] = [
        [0,""]
        ]
    defaultTiers['Construction Printer'] = []
    defaultTiers['Construction Refinery'] = [
        # int tier, dict All-tab AutoRefine, int W3Merits purchased, str Notes
        [0, {}, 0, ""],
        [1, {'Red AutoRefine': 0, 'Green AutoRefine': 0}, 1, ""],
        [2, {'Red AutoRefine': 0, 'Green AutoRefine': 0}, 2, ""],
        [3, {'Red AutoRefine': 0, 'Green AutoRefine': 0}, 3, ""],
        [4, {'Red AutoRefine': 0, 'Green AutoRefine': 0}, 4, ""],
        [5, {'Red AutoRefine': 0, 'Green AutoRefine': 0}, 5, ""]
    ]
    defaultTiers['Construction Salt Lick'] = [
        [0, {}, ""],
        [1, {'Obol Storage':8}, "Froge"],
        [2, {'Printer Sample Size':20}, "Redox Salts"],
        [3, {'Refinery Speed':10}, "Explosive Salts"],
        [4, {'Max Book':10}, "Spontaneity Salts"],
        [5, {'Movespeed':1}, "Frigid Soul"],  #This buff only works under 170% move speed, so can become useless quite quickly.
        [6, {'TD Points':10}, "Dioxide Synthesis"],
        [7, {'Multikill':10}, "Purple Salt"],
        [8, {'EXP':100}, "Dune Soul"],
        [9, {'Alchemy Liquids':100}, "Mousey"],
        [10, {'Damage':250}, "Pingy"]
        ]
    defaultTiers['Construction Death Note'] = [
        #0-4 int tier. int w1LowestSkull, int w2LowestSkull, int w3LowestSkull, int w4LowestSkull,
        #5-9 int w5LowestSkull, int w6LowestSkull, int w7LowestSkull, int w8LowestSkull, int zowCount, int chowCount,
        #10-11 int meowCount, str Notes
        [0, 0,  0,  0,   0,   0,   0,0,0,   0,0,0,      ""],
        [1, 1,  1,  1,   0,   0,   0,0,0,   0,0,0,      ""],
        [2, 2,  2,  2,   0,   0,   0,0,0,   0,0,0,      ""],
        [3, 3,  3,  3,   1,   0,   0,0,0,   0,0,0,      ""],
        [4, 4,  4,  4,   2,   0,   0,0,0,   15,0,0,     "The recommendation for ZOWs is 12hrs or less (8,333+ KPH) per enemy. If you aren't at that mark yet, don't sweat it. Come back later!"],
        [5, 5,  5,  5,   3,   0,   0,0,0,   26,0,0,     "The Voidwalker questline requires W1-W3 at all Plat Skulls. Aim to complete this by Mid W5 as Vman's account-wide buffs are insanely strong."],
        [6, 7,  5,  5,   4,   0,   0,0,0,   40,15,0,    "The recommendation for CHOWs is 12hrs or less (83,333+ KPH) per enemy. If you aren't at that mark yet, don't sweat it. Come back later!"],
        [7, 10, 7,  5,   5,   1,   0,0,0,   40,26,0,    ""],
        [8, 10, 10, 7,   5,   2,   0,0,0,   40,40,0,    ""],
        [9, 10, 10, 10,  5,   3,   0,0,0,   40,40,0,    ""],
        [10,10, 10, 10,  7,   4,   0,0,0,   53,53,0,    ""],
        [11,10, 10, 10,  10,  5,   0,0,0,   53,53,0,    "Complete Lava Skull, then BB Super CHOW, before you start working on Eclipse Skulls. "],
        [12,20, 10, 10,  10,  7,   0,0,0,   66,66,15,   "The recommendation for Super CHOWs is 24hrs or less (4m+ KPH)"],
        [13,20, 20, 10,  10,  10,  0,0,0,   66,66,26,   ""],
        [14,20, 20, 20,  10,  10,  0,0,0,   66,66,40,   ""],
        [15,20, 20, 20,  20,  10,  0,0,0,   66,66,53,   ""],
        [16,20, 20, 20,  20,  20,  0,0,0,   66,66,66,   ""],
        [17,20, 20, 20,  20,  20,  0,0,0,   70,66,66,   ""],
        [18,20, 20, 20,  20,  20,  0,0,0,   70,68,66,   ""],
        [19,20, 20, 20,  20,  20,  0,0,0,   70,68,67,   ""],
        [20,20, 20, 20,  20,  20,  0,0,0,   71,68,67,   ""],
        [21,20, 20, 20,  20,  20,  0,0,0,   71,70,67,   ""],
        [22,20, 20, 20,  20,  20,  0,0,0,   72,70,69,   ""],
        [23,20, 20, 20,  20,  20,  0,0,0,   72,72,71,   "As of v1.91, completing a Super CHOW on Boops is impossible."],
        ]
    defaultTiers['Construction Buildings Post-Buffs'] = [
        [0, "Default", [], "", ""],
        [1, "SS", [0, 5, 7], "", ""],
        [2, "S", [1, 2, 3, 6, 11, 15, 16], "", ""],
        [3, "A", [4, 9, 10, 12, 13, 14, 17, 22, 24, 25], "", ""],
        [4, "B", [18, 19, 20, 21, 23, 26], "", ""],
        [5, "C", [8], "", ""],
        [6, "D", [], "", ""],
        [7, "F", [], "", ""]
        ]
    defaultTiers['Construction Buildings Pre-Buffs'] = [
        [0, "Default", [], "", ""],
        [1, "SS", [0, 5, 7], "", ""],
        [2, "S", [1, 2, 3, 6, 11, 15, 16], "", ""],
        [3, "A", [4, 13, 14, 22, 24, 25], "", ""],
        [4, "B", [12, 17], "", ""],
        [5, "C", [8, 18, 19, 20, 21], "", ""],
        [6, "D", [9, 10, 23], "", ""],
        [7, "F", [26], "", ""]
        ]
    defaultTiers['Construction Atom Collider'] = []
    defaultTiers['Combat Levels'] = [
        #int tier, int TotalAccountLevel, str TAL reward, int PlayerLevels, str PL reward, str notes
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
        [20, 1150, "Family - Square Obol Slot 3", 250, "Personal - Sparkle Obol Slot 1 and Credit towards Equinox Dream 11", ""],
        [21, 1200, "Family - Sparkle Obol Slot 2", 425, "Able to equip The Divine Scarf", ""],
        [22, 1250, "Family - Circle Obol Slot 10", 450, "Able to equip One of the Divine Trophy", ""],
        [23, 1500, "Family - Circle Obol Slot 11", 500, "Credit towards Equinox Dream 23", "As of v1.91 Equinox Valley, there are no additional rewards after Player Level 500. However, Family/Account Levels go up to 5k, so it can still be worthwhile to level easier classes over 500."],
        [24, 1750, "Family - Hexagon Obol Slot 3", 500, "Credit towards Equinox Dream 23", "As of v1.91 Equinox Valley, there are no additional rewards after Player Level 500. However, Family/Account Levels go up to 5k, so it can still be worthwhile to level easier classes over 500.", ""],
        [25, 2000, "Family - Square Obol Slot 4", 500, "Credit towards Equinox Dream 23", "As of v1.91 Equinox Valley, there are no additional rewards after Player Level 500. However, Family/Account Levels go up to 5k, so it can still be worthwhile to level easier classes over 500.", ""],
        [26, 2100, "Family - Circle Obol Slot 12", 500, "Credit towards Equinox Dream 23", "As of v1.91 Equinox Valley, there are no additional rewards after Player Level 500. However, Family/Account Levels go up to 5k, so it can still be worthwhile to level easier classes over 500.", ""],
        [27, 2500, "Family - Sparkle Obol Slot 3", 500, "Credit towards Equinox Dream 23", "As of v1.91 Equinox Valley, there are no additional rewards after Player Level 500. However, Family/Account Levels go up to 5k, so it can still be worthwhile to level easier classes over 500.", ""],
        [28, 3000, "Family - Hexagon Obol Slot 4", 500, "Credit towards Equinox Dream 23", "As of v1.91 Equinox Valley, there are no additional rewards after Player Level 500. However, Family/Account Levels go up to 5k, so it can still be worthwhile to level easier classes over 500.", ""],
        [29, 5000, "Family - Sparkle Obol Slot 4", 500, "Credit towards Equinox Dream 23", "As of v1.91 Equinox Valley, there are no additional rewards after Player Level 500. However, Family/Account Levels go up to 5k, so it can still be worthwhile to level easier classes over 500.", ""]
        ]
    defaultTiers['Gem Shop'] = [
        #int tier, str tierName, dict recommendedPurchases, str notes
        [0, "", {}, ""],
        [1, "SS", {'Infinity Hammer':1, 'Bleach Liquid Cauldrons':1, 'Crystal 3d Printer':1, 'Richelin Kitchen':1, 'Golden Sprinkler':1}, ". These are the highest priority as 1st purchase per world."],
        [2, "S", {'Extra Card Slot':4, 'Brimstone Forge Slot':1}, ""],
        [3, "A", {'Item Backpack Space':1, 'Storage Chest Space':4, 'Carry Capacity':2, 'Weekly Dungeon Boosters':3, 'Brimstone Forge Slot':4, 'Bleach Liquid Cauldrons':2, 'Zen Cogs':2, 'Tower Building Slots':1, 'Royal Egg Cap':3, 'Richelin Kitchen':3, 'Souped Up Tube':1, 'Chest Sluggo':3, 'Divinity Sparkie':2, 'Lava Sprouts':2}, ""],
        [4, "B", {'Item Backpack Space':2, 'Storage Chest Space':8, 'Carry Capacity':4, 'Food Slot':1, 'Bleach Liquid Cauldrons':3, 'More Sample Spaces':2, 'Zen Cogs':4, 'Tower Building Slots':2, 'Royal Egg Cap':5, 'Fenceyard Space':2, 'Chest Sluggo':6, 'Lava Sprouts':4, 'Plot of Land': 1, 'Shroom Familiar': 1, 'Instagrow Generator': 1}, ""],
        [5, "C", {'Item Backpack Space':3, 'Storage Chest Space':12, 'Carry Capacity':6, 'Food Slot':2, 'More Sample Spaces':4, 'Burning Bad Books':2, 'Tower Building Slots':4, 'Fenceyard Space':4, 'Chest Sluggo':9, 'Golden Sprinkler':2, 'Lava Sprouts':6}, ""],
        [6, "D", {'Item Backpack Space':4, 'Carry Capacity':8, 'More Storage Space':5, 'Brimstone Forge Slot':8, 'Ivory Bubble Cauldrons':4, 'Obol Storage Space':3, 'More Sample Spaces':6, 'Burning Bad Books':4, 'Zen Cogs':8, 'Souped Up Tube':3, 'Fenceyard Space':6, 'Chest Sluggo':12}, ""],
        [7, "Practical Max", {'Item Backpack Space':6, 'Carry Capacity':10, 'More Storage Space':10, 'Card Presets':1, 'Brimstone Forge Slot':16, 'Sigil Supercharge':10, 'Fluorescent Flaggies':2, 'Golden Sprinkler':4}, ". I wouldn't recommend going any further as of v1.91. This tier is for the dedicated Gem Farmers from Colo and Normal-difficulty World Bosses."],
        [8, "True Max", {'Card Presets':5, 'Daily Teleports':10, 'Daily Minigame Plays':4, 'Weekly Dungeon Boosters':11, 'Obol Storage Space':12, 'Prayer Slots':4, 'Cog Inventory Space':20, 'Fluorescent Flaggies':6, 'Richelin Kitchen':10, 'Souped Up Tube':5, 'Pet Storage':12, 'Divinity Sparkie':6}, ". This final tier is for the truly depraved. Many of these bonuses are very weak or outright useless."]
        ]
    defaultTiers['Worship Prayers'] = [
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
    defaultTiers['Breeding'] = {
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
        #6+ are Shiny focused
        6: {
            "Tier": 6,
            "TerritoriesUnlocked": 20,
            "ArenaWaves": 200,
            "Shinies": { "Faster Shiny Pet Lv Up Rate": 24 },
            "ShinyNotes": "Start by focusing on pets that increase Shiny Speed rate. This will decrease the amount of time needed to level up pets in the future."
            },
        7: {
            "Tier": 7,
            "TerritoriesUnlocked": 20,
            "ArenaWaves": 200,
            "Shinies": {
                "Bonuses from All Meals": 10,
                "Infinite Star Signs": 25,
                "Base Efficiency for All Skills": 20,
                "Base Critter Per Trap": 10 },
            "ShinyNotes": ""
            },
        8: {
            "Tier": 8,
            "TerritoriesUnlocked": 20,
            "ArenaWaves": 200,
            "Shinies": {
                "Drop Rate": 15,
                "Faster Refinery Speed": 15,
                "Higher Artifact Find Chance": 15
                },
            "ShinyNotes": ""
            },
        9: {
            "Tier": 9,
            "TerritoriesUnlocked": 20,
            "ArenaWaves": 200,
            "Shinies": {
                "Multikill Per Tier": 20,
                "Total Damage": 25,
                "World 6...?": 35
                },
            "ShinyNotes": ""
            },
        10: {
            "Tier": 10,
            "TerritoriesUnlocked": 20,
            "ArenaWaves": 200,
            "Shinies": {
                "Faster Shiny Pet Lv Up Rate": 28,
                "Infinite Star Signs": 26,
                "Base WIS": 15,
                "Base STR": 15,
                "Base AGI": 15,
                },
            "ShinyNotes": ""
            }
        }
    defaultTiers['Greenstacks'] = {
        0: {  # The timegated tier
            "Vendor Shops": [
                "FoodHealth14", "FoodHealth15",  # Previously Tier2
                "FoodHealth12", "FoodHealth13",  # Previously Tier2
                "FoodPotOr4", "FoodPotGr4", "FoodPotRe4", "FoodPotYe4",  # Previously Tier3
                "OilBarrel6",  # Previously Tier5
                "FoodHealth9",  # Previously Tier10
                "FoodHealth4", "FoodHealth11",  # Previously Tier11
                "Quest19"  # Previously Tier12
            ],
            "Misc": [
                "FoodPotGr3",  # Previously Tier10
                "FoodPotRe2"   # Previously Tier11
            ],
            "Other Skilling Resources": [
                "Refinery1",  # Previously Tier11
                "Refinery2", "Refinery3", "Refinery4"  # Previously Tier12
            ]
        },
        1: {
            "Base Monster Materials": [
                "Grasslands1", "Grasslands2"],
            "Printable Skilling Resources": [
                "OakTree", "BirchTree", "JungleTree", "ForestTree", "ToiletTree", "PalmTree", "StumpTree", "SaharanFoal", "Tree7",
                "Copper", "Iron", "Gold", "Plat", "Dementia", "Void", "Lustre",
                "Fish1", "Fish2", "Fish3",
                "Bug1", "Bug2"],
            "Other Skilling Resources": [
                "CraftMat1", "CraftMat5"]
            },
        2: {
            "Base Monster Materials": [
                "Grasslands4", "Grasslands3", "Jungle1", "Jungle2", "Jungle3", "Forest1", "Forest2", "Forest3", "Sewers1", "Sewers2", "TreeInterior1", "TreeInterior2",
                "DesertA1", "DesertA2", "DesertA3", "DesertB1", "DesertB2", "DesertB3", "DesertB4", "DesertC1", "DesertC2", "DesertC3", "DesertC4",
                "SnowA1", "SnowA2", "SnowA3", "SnowB1", "SnowB2", "SnowB5", "SnowB3", "SnowB4", "SnowC1", "SnowC2", "SnowC3", "SnowC4"],
            "Printable Skilling Resources": [
                "AlienTree", "Tree8", "Tree9", "Tree11", "Tree10",
                "Starfire", "Marble", "Dreadlo",
                "Fish4", "Fish5", "Fish6", "Fish7", "Fish8",
                "Bug3", "Bug4", "Bug5", "Bug6", "Bug7", "Bug8"],
            "Other Skilling Resources": ["CraftMat6", "CraftMat7", "CraftMat9"]
            #"Vendor Shops": ["FoodHealth14", "FoodHealth15", "FoodHealth12", "FoodHealth13"]
            },
        3: {
            "Base Monster Materials": [
                "SnowA4", "SnowC5",
                "GalaxyA1", "GalaxyA2", "GalaxyA3", "GalaxyA4", "GalaxyB1",  "GalaxyB2", "GalaxyB3", "GalaxyB4", "GalaxyB5", "GalaxyC1", "GalaxyC2", "GalaxyC3", "GalaxyC4"],
            "Printable Skilling Resources": [
                "Fish9", "Fish10", "Fish11", "Fish13",
                "Bug9", "Bug11", "Bug10"],
            "Other Skilling Resources": [
                "CraftMat8", "CraftMat10", "CraftMat11",
                "Critter1", "Critter2", "Critter3",
                "Soul1",
                "CopperBar"]
            #"Vendor Shops": ["FoodPotOr4", "FoodPotGr4", "FoodPotRe4", "FoodPotYe4"]
            },
        4: {
            "Base Monster Materials": ["LavaA1", "LavaA2", "LavaA3", "LavaA4", "LavaA5", "LavaB1", "LavaB2", "LavaB3", "LavaB4", "LavaB5", "LavaB6",  "LavaC1", "LavaC2"],
            "Crystal Enemy Drops": ["FoodPotMana1", "FoodPotMana2", "FoodPotGr1", "FoodPotOr1", "FoodPotOr2", "FoodHealth1", "FoodHealth3", "FoodHealth2", "Leaf1"],
            "Printable Skilling Resources": ["Fish12"],
            "Other Skilling Resources": [
                "CraftMat12", "CraftMat13",
                "Critter4", "Critter5", "Critter6",
                "Soul2",
                "IronBar"],
            "Missable Quest Items": ["Quest3", "Quest4", "Quest7", "Quest12"]
            },
        5: {
            "Crystal Enemy Drops": ["FoodHealth6", "FoodHealth7", "FoodPotGr2", "FoodPotRe3", "Leaf2"],
            "Other Skilling Resources": [
                "CraftMat14",
                "Critter7", "Critter8",
                "Soul3",
                "GoldBar"],
            #"Vendor Shops": ["OilBarrel6"],
            },
        6: {
            "Crystal Enemy Drops": ["FoodHealth10", "FoodPotOr3", "FoodPotYe2", "Leaf3"],
            "Other Skilling Resources": [
                "Critter9", "Critter10",
                "Soul4",
                "PlatBar",
                "Bullet", "BulletB", "FoodMining1", "FoodFish1", "FoodCatch1"]
            },
        7: {
            "Crystal Enemy Drops": ["FoodPotMana4", "Leaf4"],
            "Other Skilling Resources": [
                "Soul5",
                "DementiaBar",
                "Peanut"],
            "Missable Quest Items": ["Quest14", "Quest22", "Quest23", "Quest24", "GoldricP1", "GoldricP2"]
            },
        8: {
            "Crystal Enemy Drops": ["FoodPotYe5", "Leaf5"],
            "Other Skilling Resources": [
                "Soul6",
                "VoidBar"],
            "Missable Quest Items": ["GoldricP3"]
            },
        9: {
            "Other Skilling Resources": [
                "LustreBar",
                "Quest68"], #I really hate that the Slush Bucket is listed as Quest68
            "Missable Quest Items": ["Quest32"],
            },
        10: {
            "Base Monster Materials": ["Sewers3"],
            "Missable Quest Items": ["Quest21"],
            "Other Skilling Resources": [
                "StarfireBar",
                "Bullet3", "FoodChoppin1"],
            "Crystal Enemy Drops": ["EquipmentStatues7", "EquipmentStatues3", "EquipmentStatues2", "EquipmentStatues4", "EquipmentStatues14"],
            "Misc": [],
            #"Vendor Shops": ["FoodHealth9"]
            },
        11: {
            "Base Monster Materials": ["Quest15", "Hgg"],
            "Crystal Enemy Drops": [
                "EquipmentStatues1", "EquipmentStatues5",
                "rtt0", "StoneZ1", "StoneT1", "StoneW1", "StoneA1"],
            "Other Skilling Resources": [
                "DreadloBar",
                "EquipmentSmithingTabs2"
                #"Refinery1"
            ],
            #"Vendor Shops": ["FoodHealth4", "FoodHealth11"],
            "Misc": [
                #"FoodPotGr3",  # Sold in shops as well as dropped from Sir Stache
                "FoodPotRe1",  # Technically sold in W1 shop, but so few that it barely matters
                "FoodPotRe2",
                "FoodPotMana3",
                "ButterBar"]
            },
        12: {
            "Other Skilling Resources": [
                #"Refinery2", "Refinery3", "Refinery4",
                "Critter1A", "Critter2A","Critter3A", "Critter4A", "Critter5A", "Critter6A", "Critter7A", "Critter8A", "Critter9A", "Critter10A"],
            #"Vendor Shops": ["Quest19"]
            }
        }
    return defaultTiers

def setCustomTiers(filename="input.csv"):
    return