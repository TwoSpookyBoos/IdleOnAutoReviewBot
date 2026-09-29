from functools import cached_property

from consts.consts_autoreview import MultiToValue, lowest_accepted_version
from models.custom_exceptions import VeryOldDataException
from models.advice.advice import Advice
from models.general.achievements import Achievements
from models.general.class_kill_talents import ClassKillTalents
from models.general.crystal_spawn_chance import CrystalSpawnChance
from models.general.colo_scores import ColoScores
from models.general.assets import Assets
from models.general.cards import Cards
from models.general.character import Character, talent_bonus_banned
from models.general.characters import Characters
from models.general.companions import Companions
from models.general.drop_rate import DropRate
from models.general.dungeons import Dungeons
from models.general.event_shop import EventShop
from models.general.family_bonuses import FamilyBonuses
from models.general.friend_bonuses import FriendBonuses
from models.general.golden_food import calculate_golden_food_multis
from models.general.gem_shop import GemShop
from models.general.greenstacks import GreenStacks
from models.general.guild_bonuses import GuildBonuses
from models.general.inventory import Inventory
from models.general.item_filter import ItemFilter
from models.general.merits import Merits
from models.general.npc_tokens import NpcTokens
from models.general.quests import Quests
from models.general.reset_counters import ResetCounters
from models.general.storage import Storage
from models.general.world_progress import WorldProgress
from models.w1.stamps import Stamps
from models.w1.star_signs import StarSigns
from models.w1.basketball import Basketball
from models.w1.bribes import Bribes
from models.w1.darts import Darts
from models.w1.forge import ForgeUpgrades
from models.w1.owl import Owl
from models.w1.statues import Statues
from models.w1.upgrade_vault import Vault
from models.w2.alchemy_bubbles import AlchemyBubbles
from models.w2.alchemy_cauldrons import AlchemyCauldrons
from models.w2.alchemy_p2w import AlchemyP2W
from models.w2.alchemy_vials import AlchemyVials
from models.w2.arcade import Arcade
from models.w2.ballot import Ballot
from models.w2.islands import Islands
from models.w2.killroy import Killroy
from models.w2.obols import Obols
from models.w2.post_office import PostOffice
from models.w3.armor_sets import ArmorSets
from models.w3.atom_collider import AtomCollider
from models.w3.buildings import Buildings
from models.w3.cog_board import CogBoard
from models.w3.death_note import DeathNote
from consts.w3.equinox import ribbon_cloud_dream_number
from models.w3.equinox import Equinox
from models.w3.hat_rack import HatRack
from models.w3.library import Library
from models.w3.prayers import Prayers
from models.w3.printer import Printer
from models.w3.shrines import Shrines
from models.w3.refinery import Refinery
from models.w3.salt_lick import SaltLick
from models.w3.trapping import Trapping
from models.w3.worship import Worship
from models.w4.breeding import Breeding
from models.w4.cooking import Cooking, Meals
from models.w4.lab import LabBonuses, LabJewels, LabMainframe
from models.w4.lab_chips import LabChips
from models.w4.rift import Rift
from models.w4.tome import Tome
from models.w5.divinity import Divinity
from models.w5.gaming import Gaming
from models.w5.sailing import Sailing
from models.w5.slab import Slab
from models.w6.summoning import Summoning
from models.w6.farming import Farming
from models.w6.emperor import Emperor
from models.w6.beanstalk import Beanstalk
from models.w6.sneaking import Sneaking
from models.master_classes.compass import Compass
from models.master_classes.grimoire import Grimoire
from models.master_classes.royal_armory import RoyalArmory
from models.master_classes.tesseract import Tesseract
from models.w7.coral_kid import CoralKid
from models.w7.coral_reef import CoralReef
from models.w7.dancing_coral import DancingCoral
from models.w7.research import Research
from models.w7.sushi_station import SushiStation
from models.w7.the_button import TheButton
from models.w7.spelunk import Spelunk
from models.w7.advice_fish import AdviceFish
from models.w7.clam_work import ClamWork
from models.w7.meritocracy import Meritocracy
from models.w7.gallery import Gallery
from models.w7.jelly_operator import JellyOperator
from models.w7.glimbo import Glimbo
from models.w7.minehead import Minehead
from models.w7.legend_talents import LegendTalents
from models.w7.zenith_market import ZenithMarket
from models.caverns import Caverns
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_get
from utils.text_formatting import InputType
from flask import g

logger = get_logger(__name__)


def session_singleton(cls):
    def getinstance(*args, **kwargs):
        if not hasattr(g, "account"):
            return cls(*args, **kwargs)
        return g.account

    return getinstance

@session_singleton
class Account:

    def __init__(self, json_data, source_string: InputType, run_type: str):

        self.raw_data = safe_loads(json_data)
        self.version = safer_get(self.raw_data, 'DoOnceREAL', 0.00)
        if self.version < lowest_accepted_version:
            raise VeryOldDataException(self.version)
        self.data_source = source_string.value
        # Request switches
        self.max_subgroups = 3
        self.library_group_characters = g.library_group_characters
        self.tabbed_advice_groups = g.tabbed_advice_groups
        self.manual_tome_score = g.get("tome_score") if g.manual_tome else None
        self.alerts_Advices = {
            'General': [],
            'World 1': [],
            'World 2': [],
            'World 3': [],
            'World 4': [],
            'World 5': [],
            'The Caverns Below': [],
            'World 6': []
        }
        #General
        self.world_progress: WorldProgress = WorldProgress(self.raw_data)
        self.inventory: Inventory = Inventory()
        self.gemshop: GemShop = GemShop(self.raw_data)
        # Save data can turn Autoloot on, shown on the switch too
        self.autoloot: bool = (
            g.autoloot
            or self.raw_data.get("AutoLoot", 0) == 1
            or self.gemshop.bundles['bun_i'].owned
        )
        g.autoloot = self.autoloot
        self.reset_counters: ResetCounters = ResetCounters(self.raw_data)
        self.crystal_spawn_chance: CrystalSpawnChance = CrystalSpawnChance()
        self.drop_rate: DropRate = DropRate()
        self.achievements: Achievements = Achievements(self.raw_data)
        self.merits: Merits = Merits(self.raw_data)
        self.storage: Storage = Storage(self.raw_data)
        self.greenstacks: GreenStacks = GreenStacks(self.raw_data)
        self.colo_scores: ColoScores = ColoScores(self.raw_data)
        self.npc_tokens: NpcTokens = NpcTokens(self.raw_data)
        self.event_points_shop: EventShop = EventShop(self.raw_data)
        self.dungeons: Dungeons = Dungeons(self.raw_data)
        self.guild_bonuses: GuildBonuses = GuildBonuses(self.raw_data)
        self.family_bonuses: FamilyBonuses = FamilyBonuses()
        self.class_kill_talents: ClassKillTalents = ClassKillTalents(self.raw_data)
        self.item_filter: ItemFilter = ItemFilter(self.raw_data)
        self.characters: Characters = Characters(self.raw_data, run_type)
        self.quests: Quests = Quests(self.raw_data, len(self.characters))
        self.stored_assets: Assets = Assets.from_storage(
            self.raw_data, self.characters.safe_indexes
        )
        self.worn_assets: Assets = Assets.from_worn(self.characters.safe)
        self.all_assets: Assets = self.stored_assets + self.worn_assets
        self.cards: Cards = Cards(self.raw_data, self.characters)

        self.companions: Companions = Companions(
            self.raw_data, doot=g.doot, riftslug=g.riftslug, sheepie=g.sheepie
        )
        self.friend_bonuses: FriendBonuses = FriendBonuses(self.raw_data)

        #W1
        self.stamps: Stamps = Stamps(self.raw_data, self.version)
        self.basketball: Basketball = Basketball(self.raw_data)
        self.darts: Darts = Darts(self.raw_data)
        self.owl: Owl = Owl(self.raw_data)
        self.vault: Vault = Vault(self.raw_data, potluck_pack=g.potluck_pack)
        # Shows the switch on when the save has it, like Autoloot
        g.potluck_pack = self.vault.potluck_pack_owned
        self.forge_upgrades: ForgeUpgrades = ForgeUpgrades(self.raw_data)
        self.bribes: Bribes = Bribes(self.raw_data)
        self.star_signs: StarSigns = StarSigns(self.raw_data)
        self.statues: Statues = Statues(self.raw_data, self.characters.safe)

        # W2
        self.arcade: Arcade = Arcade(self.raw_data)
        self.ballot: Ballot = Ballot(self.raw_data)
        self.post_office: PostOffice = PostOffice(self.raw_data)
        self.islands: Islands = Islands(self.raw_data)
        self.killroy: Killroy = Killroy(self.raw_data)
        self.obols: Obols = Obols(self.raw_data)
        self.alchemy_vials: AlchemyVials = AlchemyVials(self.raw_data)
        self.alchemy_bubbles: AlchemyBubbles = AlchemyBubbles(self.raw_data)
        self.alchemy_cauldrons: AlchemyCauldrons = AlchemyCauldrons(self.raw_data)
        self.alchemy_p2w: AlchemyP2W = AlchemyP2W(self.raw_data)

        # W3
        self.saltlick: SaltLick = SaltLick(self.raw_data)
        self.library: Library = Library(self.raw_data)
        self.worship: Worship = Worship(self.raw_data)
        self.equinox: Equinox = Equinox(self.raw_data)
        self.death_note: DeathNote = DeathNote(self.raw_data)
        self.printer: Printer = Printer(self.raw_data)
        self.construction_buildings: Buildings = Buildings(self.raw_data)
        self.cog_board: CogBoard = CogBoard(self.raw_data)
        self.refinery: Refinery = Refinery(self.raw_data)
        self.shrines: Shrines = Shrines(self.raw_data)
        self.prayers: Prayers = Prayers(self.raw_data)
        self.armor_sets: ArmorSets = ArmorSets(self.raw_data)
        self.atom_collider: AtomCollider = AtomCollider(self.raw_data)
        self.hat_rack: HatRack = HatRack(self.raw_data)
        self.trapping: Trapping = Trapping(self.raw_data, len(self.characters))

        # W4
        self.lab_chips: LabChips = LabChips(self.raw_data)
        self.lab_bonuses: LabBonuses = LabBonuses()
        self.lab_jewels: LabJewels = LabJewels(self.raw_data)
        self.lab_mainframe: LabMainframe = LabMainframe(
            self.raw_data, self.lab_bonuses, self.lab_jewels
        )
        self.rift: Rift = Rift(self.raw_data)
        self.tome: Tome = Tome(self.raw_data)
        self.breeding: Breeding = Breeding(self.raw_data)
        self.meals: Meals = Meals(self.raw_data, self.version)
        self.cooking: Cooking = Cooking(self.raw_data, self.meals)

        # W5
        self.gaming: Gaming = Gaming(self.raw_data)
        self.divinity: Divinity = Divinity(self.raw_data)
        self.sailing: Sailing = Sailing(self.raw_data)
        self.slab: Slab = Slab(self.raw_data)

        # The Caverns Below
        self.caverns: Caverns = Caverns(self.raw_data)

        # W6
        self.summoning: Summoning = Summoning(self.raw_data)
        self.farming: Farming = Farming(self.raw_data)
        self.sneaking: Sneaking = Sneaking(self.raw_data)
        self.beanstalk: Beanstalk = Beanstalk(self.raw_data)
        self.emperor: Emperor = Emperor(self.raw_data)

        # Master Classes (World 6 mechanic)
        self.grimoire: Grimoire = Grimoire(self.raw_data)
        self.compass: Compass = Compass(self.raw_data)
        self.tesseract: Tesseract = Tesseract(self.raw_data)
        self.royal_armory: RoyalArmory = RoyalArmory(self.raw_data)

        # W7
        self.spelunk = Spelunk(self.raw_data)
        self.coral_reef = CoralReef(self.raw_data)
        self.legend_talents = LegendTalents(self.raw_data)
        self.advice_fish = AdviceFish(self.raw_data)
        self.clam_work = ClamWork(self.raw_data)
        self.meritocracy = Meritocracy(self.raw_data)
        self.gallery = Gallery(self.raw_data)
        self.zenith_market = ZenithMarket(self.raw_data)
        self.glimbo = Glimbo(self.raw_data)
        self.research = Research(
            self.raw_data, self.companions.has('King Doot'), self.glimbo.total_trades
        )
        self.minehead = Minehead(self.raw_data)
        self.sushi_station = SushiStation(self.raw_data)
        self.the_button = TheButton(self.raw_data)
        self.dancing_coral = DancingCoral(self.raw_data)
        self.coral_kid = CoralKid(self.raw_data)
        self.jelly_operator = JellyOperator(self.raw_data)

    def calculate(self):
        self._calculate_setup()
        # Each wave reads numbers the waves before it produce
        self._calculate_wave_1()
        self._calculate_wave_2()
        self._calculate_wave_3()
        self._calculate_wave_4()

    def _calculate_setup(self):
        self.caverns.link_account_systems(
            self.legend_talents["Whats in your Jar?"],
            self.stamps,
            self.gemshop.purchases["Conjuror Pts"],
        )
        self.family_bonuses.calculate_levels(self.characters.safe)
        self.inventory.calculate_owned(
            self.characters,
            self.autoloot,
            self.event_points_shop['Secret Pouch'].owned,
            self.gemshop.bundles['bon_f'].owned,
        )
        self.death_note.calculate_apocalypse_characters(
            self.characters.barbs, self.characters.bbs
        )
        self.death_note.calculate_kills(self.characters)
        self.death_note.calculate_rift_meowed(self.characters)
        self.equinox.calculate_unlocked(
            self.achievements, self.research.grid['Equinox Nightmares'].level
        )
        self.rift.calculate_unlocked(self.quests.by_character)
        self.breeding.calculate_egg_slots(
            self.gemshop.purchases['Royal Egg Cap'].owned, self.merits[3][2].level
        )
        self.divinity.link_characters(self.characters.safe)

    def _calculate_wave_1(self):
        self.caverns.villagers["Cosmos"].calculate_bonuses(self.companions.has("King Doot"))
        self.arcade.calculate_values(self.companions)
        self.tesseract.calculate_upgrades()
        # Emperor reads tesseract, sneaking, arcade and gemshop
        self.emperor.calculate_max_attempt(self.gemshop, self.sneaking.emporium)
        self.emperor.calculate_bonus_multi(self.arcade, self.tesseract)
        self.emperor.calculate_bonuses()
        self.summoning.calculate_winner_bonus_multi(
            self.sneaking.pristine_charms["Crystal Comb"].value,
            self.gemshop.purchases["King Of All Winners"],
            self.merits[5][4],
            self.sailing.artifacts["The Winz Lantern"].level,
            self.achievements,
            self.armor_sets["GODSHARD SET"].total_value,
            self.gemshop.bundles["ban_i"].owned,
            self.emperor["Summoning Winner Bonuses"].value,
        )
        self.summoning.calculate_bonuses()
        self.friend_bonuses.calculate_bonuses(
            self.companions,
            self.event_points_shop['Friendly Slot'].owned,
        )
        self.gallery.calculate_palette_bonuses(
            self.legend_talents['Picasso Gaming'].value
        )
        self.farming.calculate_exotic_market_bonus()

    def _calculate_wave_2(self):
        # General
        self.add_alert_list('General', self.item_filter.get_alerts(
            self.slab,
            self.stored_assets,
            self.all_assets,
            self.autoloot,
            self.equinox.dreams[17].completed,
        ))
        self.world_progress.calculate(self.achievements, self.death_note)
        self.storage.calculate_other_sources(
            self.event_points_shop, self.vault, self.construction_buildings, self.gemshop
        )

        # Lab connections gate bonuses read all through wave 2
        self.divinity.calculate(
            self.companions.has('King Doot')
            or 'Arctis' in self.caverns.villagers["Cosmos"].majiks.idleon["Pocket Divinity"].link
        )
        # Meals rerun when Black Diamond lights
        self.lab_mainframe.calculate(
            self.characters.safe,
            self.divinity.account_wide_arctis,
            self.gemshop.purchases['Souped Up Tube'].owned,
            self.sneaking.emporium,
            self.meals,
            next(card for card in self.cards if card.codename == 'Crystal3'),
            self.lab_chips['Conductive Motherboard'],
            self.breeding,
            self.merits[3][4].level,
            self.equinox.upgrades['Laboratory Fuse'].level
            + self.summoning.bonuses['Lab Con Range'].value,
            self._calculate_meals,
        )

        # Master Classes. Bones wait for wave 3's Gambit, dust for the Hat Rack
        self.grimoire.calculate_upgrades()
        self.compass.calculate_upgrades()

        # W1
        self.vault.calculate(self.glimbo, self.research.grid, self.event_points_shop)
        self.star_signs.calculate_seraph(
            self.tesseract.upgrades['Astrology Cultism'].level,
            self.characters.all_skills['Summoning'],
        )
        self.star_signs.calculate_silkrode(self.lab_chips['Silkrode Nanochip'])
        self.stamps.calculate_total_values(
            [
                self.atom_collider['Aluminium - Stamp Supercharger'].value,
                self.sneaking.pristine_charms['Jellypick'].value,
                self.compass.upgrades['Abomination Slayer XVII'].total_value,
                MultiToValue(self.armor_sets['EMPEROR SET'].total_value),
                20 * self.event_points_shop['Extra Exaltedness'].owned,
                # "PaletteBonus"(23) in source. Last updated in v2.531.0
                self.gallery.exalted_palette_bonus,
                # "ExoticBonusQTY"(49) in source. Last updated in v2.531.0
                self.farming.exotic_market['EXALTED ELDOU'].value,
                # "Spelunk[4][3]" in source. Last updated in v2.531.0
                self.spelunk.exalt_stamp_bonus,
                self.legend_talents['Wowa Woowa'].value,
                # "RoG_BonusQTY"(17) in source. Last updated in v2.531.0
                self.sushi_station.get_milestone_bonus_value('Exalted Stamp Bonus'),
                # "RoG_BonusQTY"(50) in source. Last updated in v2.531.0
                self.jelly_operator.obstructions['Fancy Facet'].bonus_value / 100,
            ],
            self.lab_bonuses['Certified Stamp Book'].enabled,
            self.sneaking.pristine_charms['Liqorice Rolle'].value,
        )
        self.owl.calculate(self.legend_talents, self.companions)
        self.basketball.calculate()
        self.darts.calculate()

        # W2
        self.alchemy_vials.calculate_values(self.vault, self.rift, self.lab_bonuses)
        self.alchemy_p2w.sigils.calculate_precharge_levels(
            self.sneaking.emporium['Ionized Sigils'].obtained
        )
        self.alchemy_bubbles.calculate_prisma_multi(
            self.tesseract,
            self.arcade,
            self.sushi_station,
            self.jelly_operator,
            self.gallery,
            self.alchemy_p2w.sigils,
            self.farming.exotic_market,
            self.legend_talents,
            self.companions,
        )
        self.ballot.calculate_values(
            self.equinox.upgrades['Voter Rights'].level,
            self.caverns.villagers["Cosmos"].majiks.idleon['Voter Integrity'].value,
            self.summoning.bonuses["Ballot Bonus"].value,
            self.event_points_shop['Gilded Vote Button'].owned,
            self.event_points_shop['Royal Vote Button'].owned,
            self.companions['Mashed Potato'].bonus,
            self.companions['Crystal Cuttlefish'].bonus,
            self.legend_talents['Democracy FTW'].value,
        )
        self.islands.calculate_trash_shop(self.stamps, self.stored_assets, self.bribes)
        self.killroy.calculate_available(self.equinox.upgrades['Shades of K'].level)
        # Tachyons read vials
        self.tesseract.calculate_tachyon_sources(
            self.characters.acs, self.lab_jewels, self.arcade, self.emperor,
            self.alchemy_bubbles, self.sneaking, self.gemshop, self.alchemy_vials,
            self.companions.has('Balloonfish'),
        )

        # W3
        self.refinery.calculate(self.companions['Panda'].bonus, self.merits[2][6].level)
        self.hat_rack.calculate_bonuses(
            self.companions, self.event_points_shop, self.minehead, self.sushi_station
        )
        self.trapping.calculate(
            characters=self.characters,
            quests_by_character=self.quests.by_character,
            emporium_new_critter=self.sneaking.emporium["New Critter"].obtained,
            call_me_ash_level=self.alchemy_bubbles['Call Me Ash'].level,
        )
        # Gambit's +100 Tower levels come in wave 3
        self.construction_buildings.calculate_max_levels(
            self.rift['SkillMastery'].unlocked,
            sum(self.characters.all_skills['Construction']),
            self.atom_collider['Carbon - Wizard Maximizer'].level,
        )
        self.atom_collider.calculate_max_levels(
            self.gaming.superbits['Isotope Discovery'].unlocked,
            self.compass.upgrades['Atomic Potential'],
            self.event_points_shop['Higgs Boson'].owned,
        )
        self.atom_collider.calculate_costs(
            self.merits[4][6].level,
            self.construction_buildings['Atom Collider'].level,
            self.gaming.superbits['Atom Redux'].unlocked,
            self.alchemy_bubbles['Atom Split'].base_value,
            self.stamps['Atomic Stamp'].total_value,
            self.grimoire.upgrades['Death of the Atom Price'].total_value,
            self.compass.upgrades['Atomic Cost Crash'].total_value,
        )
        self.shrines.calculate_values(
            next(c.getStars() for c in self.cards if c.name == 'Chaotic Chizoar')
        )

        # W4
        self.cooking.calculate_max_plate_level(
            self.sailing.artifacts['Causticolumn'].level,
            self.rift['EldritchArtifact'].unlocked,
            self.sneaking.emporium,
            self.grimoire.upgrades['Supreme Head Chef Status'],
            self.spelunk.caves["Lunarheim"],
        )
        self.lab_bonuses.calculate_nblb(
            self.lab_jewels['Pyrite Rhinestone'].enabled,
            self.sailing.artifacts['Amberite'].level,
            self.gaming.superbits['Moar Bubbles'].unlocked,
            self.gaming.superbits['Even Moar Bubbles'].unlocked,
            self.merits[3][6].level,
        )

        # W7
        self.spelunk.calculate_lore_bonus(self.sailing.artifacts["Pointagon"])
        self.advice_fish.calculate_bonuses()
        self.meritocracy.calculate_bonuses()
        self.zenith_market.calculate_bonuses()
        self.research.calculate_bonuses(
            self.companions["Pirate Deckhand"].bonus,
            self.equinox.dreams,
            self.sushi_station.get_milestone_bonus_value("Research Upgrade Bonus Multi"),
        )
        self.glimbo.calculate_drop_rate_multi(self.research)
        self.sushi_station.calculate_bonuses()
        self.dancing_coral.calculate_bonuses(self.construction_buildings)
        self.coral_kid.calculate_bonuses(
            sum(self.characters.all_skills["Divinity"]),
            self.coral_reef.total_level,
            self.divinity.god_rank,
        )
        self.jelly_operator.calculate_bonuses(
            self.research.grid["Jelly Operator Linguistics"].value,
            self.atom_collider["Sulfur - Jelly Bloodcell Juicer"].value,
            self.arcade[72].value,
        )
        self.gallery.calculate_bonuses(
            highest_world_reached=self.world_progress.highest_reached,
            characters=self.characters,
            cards=self.cards,
            alchemy_bubbles=self.alchemy_bubbles,
            coral_reef=self.coral_reef,
            artifacts=self.sailing.artifacts,
            gemshop=self.gemshop,
            emporium=self.sneaking.emporium,
            spelunk=self.spelunk,
            legend_talents=self.legend_talents,
            event_shop=self.event_points_shop,
            clam_work=self.clam_work,
            companions=self.companions,
            sushi_station=self.sushi_station,
        )

    def _calculate_meals(self):
        self.meals.calculate_values(
            self.lab_jewels['Black Diamond Rhinestone'].active_value,
            self.breeding.total_shiny_levels['Bonuses from All Meals'],
            self.summoning.bonuses["Meal Bonuses"].as_multi,
            self.companions.get_multi('Wickerlight Spirit', 'Meal Bonus'),
            emperor_set=MultiToValue(self.armor_sets['EMPEROR SET'].total_value),
            cloud_73=self.equinox.dreams[ribbon_cloud_dream_number].completed,
            jelly_rog_60=self.jelly_operator.obstructions['Soldier Shiv'].bonus_value,
            max_summoning_level=max(self.characters.all_skills['Summoning'], default=0),
        )

    def _calculate_wave_3(self):
        # Talent levels, and everything reading them
        self.library.calculate_max_book_levels(
            self.construction_buildings,
            self.achievements,
            self.atom_collider,
            self.sailing,
            self.merits,
            self.saltlick,
            self.summoning,
        )
        self.equinox.calculate_max_levels(
            self.summoning.bonuses["Equinox Max LV"].value,
            self.gaming.superbits['Equinox Unending'].unlocked,
        )
        self.library.calculate_bonus_talents(
            self.armor_sets, self.companions, self.family_bonuses, self.equinox,
            self.achievements, self.sneaking, self.grimoire, self.tesseract,
        )
        self.characters.calculate_bonus_talent_levels(
            account_wide_bonus=self.library.account_wide_bonus_talents,
            account_wide_arctis=self.divinity.account_wide_arctis,
            big_p_value=self.alchemy_bubbles['Big P'].base_value,
            coral_kid_level=self.coral_kid[3].level,
            timmy_talented=self.gaming.superbits['Timmy Talented'].unlocked,
            max_book_level=self.library.max_book_level,
            es_family_value=self.family_bonuses['Elemental Sorcerer'].value,
            spelunk=self.spelunk,
            super_talent_levels=self.super_talent_levels,
        )

        # Tome reads meals, stamps, meritocracy and bonus talent levels
        self.tome.calculate_live_talent_max(self.meals['Buncha Banana'].value)
        self.tome.calculate_star_talents(
            self.characters.safe,
            self.family_bonuses['Wizard'].value,
            self.stamps['Talent S Stamp'].total_value,
            self.guild_bonuses['Star Dazzle'].value,
            self.alchemy_p2w.sigils['Two Starz'],
            self.sailing.artifacts.chilled_yarn_multi,
            self.meritocracy[21].value,
            self.bribes['Star Scraper'],
            self.companions['Flying Worm'].bonus,
        )
        self.tome.calculate_score(self.manual_tome_score)
        self.tome.calculate_bonuses(self.grimoire, self.armor_sets, self.event_points_shop)

        # Minau measures Tome score, Gambit points read Minau
        self.caverns.villagers["Minau"].calculate_bonuses(
            lengthmeister_multi=(
                self.caverns.villagers["Cosmos"].majiks.village["Lengthmeister"].as_multi
            ),
            crops_found=self.farming.crops.unlocked,
            all_skills=self.characters.all_skills,
            tome_score=self.tome.score,
            death_note=self.death_note,
            highest_dmg=self.highest_dmg,
            slab_items=len(self.slab),
            studies_done=self.caverns.villagers["Bolaia"].studies.total,
            golem_kills=self.caverns.caves["The Temple"].current_kills,
        )
        self.construction_buildings.calculate_gambit_levels(
            self.caverns.caves['Gambit'].bonuses[9].unlocked
        )
        self.summoning.calculate_doublers(
            self.caverns.caves["Gambit"].bonuses[0].value,
            self.event_points_shop["Summoning Star"].owned,
        )

        self.crystal_spawn_chance.calculate(
            next(card for card in self.cards if card.name == 'Poop'),
            next(card for card in self.cards if card.name == 'Demon Genie'),
            self.lab_chips['Omega Nanochip'].owned + self.lab_chips['Omega Motherboard'].owned,
            self.stamps['Crystallin'].total_value,
            self.characters,
            self.shrines['Crescent Shrine'].value,
        )
        self.sneaking.calculate_gemstones_values(
            self.get_current_max_talent("Generational Gemstones")
        )
        self.sneaking.calculate_pristine_chance(
            self.compass.upgrades['Pristine Collector'].total_value
        )
        self.grimoire.calculate_bone_sources(
            self.characters.dbs, self.sneaking, self.caverns, self.all_assets,
            self.hat_rack.get_bonus_value('Extra Bones'),
            self.arcade, self.lab_jewels, self.emperor,
        )
        self.compass.calculate_dust_sources(
            self.characters.wws, self.sneaking, self.all_assets,
            self.hat_rack.get_bonus_value('Dust Multi'),
            self.arcade, self.lab_jewels, self.emperor,
        )
        self.class_kill_talents.calculate_values(
            self.characters.safe, self.get_best_talent_level
        )

        # Farming: Land Rank multi reads talents, crop evo reads summoning
        self.farming.calculate_market_bonus(
            self.gemshop.purchases['Plot Of Land'].owned, self.merits[5][2].level
        )
        self.farming.calculate_land_rank_bonus(self.get_current_max_talent("Dank Rank"))
        self.farming.calculate_crop_depot_bonus(
            self.lab_bonuses['Depot Studies PhD'], self.lab_jewels['Pure Opal Rhombol'],
            self.grimoire, self.vault, self.sneaking.emporium,
        )
        self.farming.calculate_crop_value_multi(self.ballot)
        self.farming.calculate_crop_evo_multi(
            self.characters,
            self.alchemy_bubbles,
            self.alchemy_vials,
            self.tome.score,
            self.stamps['Crop Evo Stamp'].total_value,
            self.meals,
            self.star_signs,
            self.characters.all_skills['Farming'],
            self.rift['SkillMastery'],
            self.ballot[29],
            self.achievements,
            self.killroy.skull_shop,
            self.caverns.caves['The Lamp'].wishes['World 6 Majigers'],
            self.summoning.bonuses,
        )
        self.farming.calculate_crop_speed(self.alchemy_vials, self.summoning.bonuses)
        self.farming.calculate_bean_bonus(
            self.sneaking.emporium['Deal Sweetening'].value, self.achievements
        )
        self.farming.calculate_og(
            self.achievements,
            self.star_signs,
            self.merits[5][2].level,
            self.sneaking.pristine_charms['Taffy Disc'].value,
        )

    def _calculate_wave_4(self):
        # Reads wave 3 talent levels
        self.statues.calculate_values(
            [char.max_talents.get('56', 0) for char in self.characters.vmans],
            self.sailing.artifacts['The Onyx Lantern'].level,
            self.zenith_market['TRUE ZEN'].value,
            self.meritocracy[26].value,
            self.event_points_shop['Smiley Statue'].owned,
            self.vault.upgrades['Statue Bonanza'].total_value,
        )
        self.beanstalk.calculate_unlocked_tier(self.sneaking.emporium)
        self.beanstalk.calculate_golden_food_multi(calculate_golden_food_multis(
            characters=self.characters,
            best_talent_level=self.get_best_talent_level,
            companions=self.companions,
            armor_sets=self.armor_sets,
            family_bonuses=self.family_bonuses,
            death_note=self.death_note,
            sigils=self.alchemy_p2w.sigils,
            artifacts=self.sailing.artifacts,
            meritocracy=self.meritocracy,
            star_signs=self.star_signs,
            breeding=self.breeding,
            tesseract=self.tesseract,
            cards=self.cards,
            achievements=self.achievements,
            jelly_operator=self.jelly_operator,
            stamps=self.stamps,
            meals=self.meals,
            bribes=self.bribes,
            pristine_charms=self.sneaking.pristine_charms,
            ballot=self.ballot,
            legend_talents=self.legend_talents,
            vault=self.vault,
            alchemy_bubbles=self.alchemy_bubbles,
        ))
        self.beanstalk.calculate_bonuses()
        self.forge_upgrades.calculate_ore_capacity(
            arcade_bonus=self.arcade[26].value,
            godshard_stars=next(
                c.getStars() for c in self.cards if c.name == 'Godshard Ore'
            ),
            forge_stamp=self.stamps['Forge Stamp'].total_value,
            bribe=self.bribes['Forge Cap Smuggling'].bonus,
            vault_beeg_forge=self.vault.upgrades['Beeg Forge'].total_value,
            majik_beeg_forge=self.caverns.villagers["Cosmos"].majiks.idleon[
                'Beeg Beeg Forge'
            ].value,
            vitamin_d_complete=self.achievements['Vitamin D-licious'].complete,
            skill_mastery_unlocked=self.rift['SkillMastery'].unlocked,
            total_smithing_levels=sum(self.characters.all_skills['Smithing']),
        )
        self.printer.calculate_sample_rate(
            snow_slurry=self.alchemy_vials['Snow Slurry (Snow Ball)'].value,
            sample_it=self.alchemy_bubbles['Sample It'].base_value,
            salt_lick_level=self.saltlick.upgrades['Printer Sample Size'].level,
            merit_level=self.merits[2][4].level,
            merit_max_level=self.merits[2][4].max_level,
            maestro_family=self.family_bonuses['Maestro'].value,
            stample=self.stamps['Stample Stamp'].total_value,
            amplestample=self.stamps['Amplestample Stamp'].total_value,
            arcade_bonus=self.arcade[5].value,
            saharan_skull=self.achievements['Saharan Skull'].complete,
            max_book_level=self.library.max_book_level,
            characters=self.characters,
        )
        self.printer.calculate_output(
            skill_mastery_unlocked=self.rift['SkillMastery'].unlocked,
            all_skills=self.characters.all_skills,
            gold_relic_level=self.sailing.artifacts['Gold Relic'].level,
            supreme_wiring_owned=self.event_points_shop['Supreme Wiring'].owned,
            biggole_mole_bonus=self.companions['Biggole Mole'].bonus,
            moon_of_print=self.compass.upgrades['Moon of Print'],
            death_bringers=self.characters.dks,
            max_book_level=self.library.max_book_level,
            king_of_the_remembered_kills=(
                self.class_kill_talents['King of the Remembered'].kills
            ),
            lolly_flower=self.sneaking.pristine_charms['Lolly Flower'].value,
            ballot_multi=self.ballot[11].active_multi,
            has_king_doot=self.companions.has('King Doot'),
            wired_in_enabled=self.lab_bonuses['Wired In'].enabled,
            harriep_unlocked=self.divinity[4].unlocked,
        )
        self.breeding.calculate_pet_damage(
            electrolyte_vial=self.alchemy_vials['Electrolyte (Condensed Zap)'].value,
            barley_lost=self.achievements['Barley Lost'].complete,
            croissant=self.meals['Croissant'].value,
            wedding_cake=self.meals['Wedding Cake'].value,
            characters=self.characters.safe,
            power_bowower_unlocked=self.star_signs['Power Bowower'].unlocked,
            arcade_bonus=self.arcade[30].value,
            vault_pet_punchies=self.vault.upgrades['Pet Punchies'].total_value,
        )
        self.sailing.calculate_speed(
            purrmep=self.divinity.named('Purrmep'),
            goharut=self.divinity.named('Goharut'),
            bagur=self.divinity.named('Bagur'),
            characters=self.characters.safe,
            crawler_level=next(c.level for c in self.cards if c.name == 'Crawler'),
            kattlekruk_level=next(
                c.level for c in self.cards if c.name == 'Kattlekruk'
            ),
            boaty_bubble=self.alchemy_bubbles['Boaty Bubble'].base_value,
            big_p=self.alchemy_bubbles['Big P'].base_value,
            ballot_buff=next(
                buff for buff in self.ballot.values()
                if 'Sailing Speed' in buff.description
            ),
            slab_count=len(self.slab),
            slab_sovereignty=self.lab_bonuses['Slab Sovereignty'],
            sailboat_stamp=self.stamps['Sailboat Stamp'].total_value,
            boat_statue=self.statues['Boat Statue'],
            popped_corn=self.meals['Popped Corn'].value,
            oj_jooce=self.alchemy_vials['Oj Jooce (Orange Slice)'].value,
            skill_mastery_unlocked=self.rift['SkillMastery'].unlocked,
            total_sailing_level=sum(self.characters.all_skills['Sailing']),
            msa_sailing=self.gaming.superbits['MSA Sailing'].unlocked,
            total_worship_waves=self.worship.total_waves,
            c_shanti_unlocked=self.star_signs['C. Shanti Minor'].unlocked,
            davey_jones_owned=self.gemshop.purchases['Davey Jones Training'].owned,
            davey_jones_returns=self.legend_talents['Davey Jones Returns'].value,
        )
        self.coral_reef.calculate_daily_corals(
            shellslug_multi=self.companions['Shellslug'].get_multi('Daily Corals'),
            coolral_owned=self.event_points_shop['Coolral'].owned,
            more_coral_owned=self.gemshop.purchases['More Coral'].owned,
            coral_kid=self.coral_kid[5].value,
            dancing_coral=self.dancing_coral[0].value,
            clam_work_level=self.clam_work.level,
            killroy_coral_level=self.killroy.coral_level,
            corale_stamp=self.stamps['Corale Stamp'].total_value,
            scale_on_ice=self.alchemy_vials['Scale On Ice (Scaled Fragment)'].value,
            coral_restoration=self.legend_talents['Coral Restoration'].value,
            arcade_bonus=self.arcade[57].value,
            coral_conservationism=self.sneaking.emporium['Coral Conservationism'].value,
            demonblub_card=next(
                c for c in self.cards if c.name == 'Demonblub'
            ).getCurrentValue(),
            coral_statue=self.statues['Coral Statue'],
        )
        self.cards.calculate(
            ruby_cards_unlocked=self.rift['RubyCards'].unlocked,
            rustbelt_03_obtained=self.spelunk.caves['Rustbelt 03'].bonus_obtained,
            five_aces_bribe=self.bribes['Five Aces in the Deck'].bonus,
            pokaminni_unlocked=self.star_signs['Pokaminni'].unlocked,
            anearful_vial=self.alchemy_vials['Anearful (Glublin Ear)'].value,
            card_stamp=self.stamps['Card Stamp'].total_value,
            card_spotter=self.guild_bonuses['C2 Card Spotter'].value,
            card_champ_bubble=self.alchemy_bubbles['Card Champ'].base_value,
        )
        self.alchemy_p2w.sigils.calculate_speed(
            chilled_yarn=self.sailing.artifacts['Chilled Yarn'],
            chilled_yarn_multi=self.sailing.artifacts.chilled_yarn_multi,
            max_chilled_yarn_multi=self.sailing.artifacts.max_chilled_yarn_multi,
            vial_junkee=self.achievements['Vial Junkee'].complete,
            sigil_supercharge_owned=self.gemshop.purchases['Sigil Supercharge'].owned,
            willow_vial=self.alchemy_vials['Willow Sippy (Willow Logs)'].value,
            sigil_stamp=self.stamps['Sigil Stamp'].total_value,
            summoning_multi=self.summoning.bonuses['Sigil SPD'].as_multi,
            tuttle_vial=self.alchemy_vials['Turtle Tisane (Tuttle)'].value,
            ballot_multi=self.ballot[17].active_multi,
            arcade_bonus=self.arcade[43].value,
            big_sig_fig=self.legend_talents['Big Sig Fig'].value,
        )
        # Reads nearly everything, so last
        self.drop_rate.calculate(
            best_talent_level=self.get_best_talent_level,
            class_kill_talent_value=self.get_class_kill_talent_value,
            characters=self.characters,
            cards=self.cards,
            artifacts=self.sailing.artifacts,
            guild_bonuses=self.guild_bonuses,
            friend_bonuses=self.friend_bonuses,
            vault=self.vault,
            gemshop=self.gemshop,
            grimoire=self.grimoire,
            royal_armory=self.royal_armory,
            owl=self.owl,
            stamps=self.stamps,
            arcade=self.arcade,
            obols=self.obols,
            alchemy_bubbles=self.alchemy_bubbles,
            alchemy_p2w=self.alchemy_p2w,
            alchemy_vials=self.alchemy_vials,
            ballot=self.ballot,
            equinox=self.equinox,
            armor_sets=self.armor_sets,
            hat_rack=self.hat_rack,
            breeding=self.breeding,
            tome=self.tome,
            caverns=self.caverns,
            achievements=self.achievements,
            farming=self.farming,
            summoning=self.summoning,
            emperor=self.emperor,
            legend_talents=self.legend_talents,
            spelunk=self.spelunk,
            research=self.research,
            gallery=self.gallery,
            world_progress=self.world_progress,
            companions=self.companions,
            class_kill_talents=self.class_kill_talents,
            sneaking=self.sneaking,
            sushi_station=self.sushi_station,
            jelly_operator=self.jelly_operator,
            glimbo=self.glimbo,
            minehead=self.minehead,
            family_bonuses=self.family_bonuses,
            beanstalk=self.beanstalk,
            star_signs=self.star_signs,
            tesseract=self.tesseract,
            prayers=self.prayers,
            shrines=self.shrines,
            lab_bonuses=self.lab_bonuses,
            reset_counters=self.reset_counters,
        )

    def add_alert_list(
        self, group_name: str, advice_list: list[Advice | None] | set[Advice | None]
    ):
        advice_list = [item for item in advice_list if item is not None]
        self.alerts_Advices[group_name].extend(advice_list)

    def get_current_max_talent(self, name: str) -> int:
        """
        Get the max level of characters talents from their current preset set.

        :param name: talent name.
        :returns: Max talent level or 0.
        """
        char_list = []
        talent_num = "-1"
        if name == "Generational Gemstones":
            char_list = self.characters.wws
            talent_num = "432"
        elif name == "Dank Rank":
            char_list = self.characters.dbs
            talent_num = "207"
        return max(
            [
                talent_level + char.total_bonus_talent_levels
                + self.super_talent_levels * self.spelunk.has_super_talent(
                    char.character_index, int(talent_num)
                )
                for char in char_list
                if (talent_level := char.current_preset_talents.get(talent_num, 0)) > 0
            ],
            default=0,
        )

    def get_class_kill_talent_level(
        self,
        talent_name: str,
        character: Character
    ) -> int:
        return self.get_best_talent_level(
            self.class_kill_talents[talent_name].talent_number, character
        )

    def get_best_talent_level(self, talent_index: int, character: Character) -> int:
        # "getbonus2"(1, t, -1) in source: best base across chars + current char's
        # bonus levels. Last updated in v2.531.0
        # Super levels if in either preset, unlike AllTalentLV's active one
        # Talents under 100 and banned ones get no bonus or super levels
        gets_bonus = talent_index >= 100 and not talent_bonus_banned(talent_index)
        bonus = character.get_bonus_levels(talent_index) if gets_bonus else 0
        return max(
            [
                base + bonus
                + gets_bonus * self.super_talent_levels * self.spelunk.has_super_talent(
                    char.character_index, talent_index
                )
                for char in self.characters.safe
                if (base := char.current_preset_talents.get(str(talent_index), 0)) > 0
            ],
            default=0,
        )

    def get_class_kill_talent_value(
        self,
        talent_name: str,
        character: Character
    ) -> float:
        level = self.get_class_kill_talent_level(talent_name, character)
        return (
            self.class_kill_talents[talent_name].value_at_level(level)
            if level > 0
            else 0
        )

    @property
    def super_talent_levels(self) -> int:
        # "SuperTalentPTS_LVgiven" in source. Last updated in v2.531.0
        return round(
            50
            + self.legend_talents['Super Duper Talents'].value
            + self.zenith_market['SUPER DUPERS'].level
            * self.zenith_market['SUPER DUPERS'].bonus_per_level
        )

    @cached_property
    def highest_dmg(self) -> float:
        # "Highest Dmg" from W2 Task
        raw_tasks = safe_loads(self.raw_data.get('TaskZZ0', []))
        try:
            return float(raw_tasks[1][0])
        except ValueError:
            logger.exception(
                f"Failed to cast Highest Damage of {raw_tasks[1][0]} from W2 Task. "
                f"Defaulting to e20 idk"
            )
            return 1e20
        except IndexError:
            logger.exception(
                "No TaskZZ0[1][0] for Highest Damage from W2 Tasks"
            )
            return 1
        except:
            logger.exception(
                "TaskZZ0[1][0] has bad value for Highest Damage from W2 Tasks"
            )
            return 1
