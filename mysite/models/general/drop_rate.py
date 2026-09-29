from collections.abc import Callable
from dataclasses import dataclass, field
from math import prod

from consts.consts_autoreview import ValueToMulti
from consts.consts_general import max_card_stars
from consts.consts_w1 import get_seraph_cosmos_multi
from consts.consts_w2 import max_sigil_level, sigils_dict
from consts.general.drop_rate import (
    big_big_hampter_drop_rate,
    boss_battle_spillover_talent_index,
    card_set_drop_rate,
    deathbringer_pack_drop_rate,
    drop_rate_cards,
    drop_rate_flat_companions,
    drop_rate_multi_card_description,
    drop_rate_multi_codenames,
    drop_rate_multi_companions,
    flat_drop_rate_codenames,
    golden_food_stat,
    gown_drop_rate_codename,
    island_explorer_pack_multi,
    looty_booty_talent_index,
    passive_drop_rate_card_caps,
    robbinghood_talent_index,
    sneaking_mastery_drop_rate,
    summoning_gm_drop_rate,
)
from consts.general.friend_bonuses import friend_bonus_drop_rate_index
from consts.general.talents import dank_rank_talent_index, family_guy_talent_index
from consts.idleon.lava_func import lava_func
from consts.idleon.w7.research import minehead_drop_rate_bonus_index
from consts.w3.equinox import drop_rate_dream_number
from models.w1.star_signs import get_infinite_star_sign_levels
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class CardSetProgress:
    stars_sum: int
    star: int
    next_star_sum: int
    value: int


@dataclass
class CharacterDropRate:
    luk: float = 0
    cards: float = 0
    card_set: float = 0
    card_multi: float = 1
    family_multi: float = 1
    equipment: float = 0
    equipment_multi: float = 0
    gallery: float = 0
    gallery_multi: float = 0
    hatrack: float = 0
    hatrack_multi: float = 0
    equipment_multi_total: float = 1
    gown_multi: float = 1
    golden_food: float = 0
    silkrode_nanochip_equipped: bool = False
    seraph_cosmos_multi: float = 1
    star_signs: dict[str, float] = field(default_factory=dict)
    post_office: float = 0
    prayers: float = 0
    obols: float = 0
    clover_shrine_active: bool = False
    shrines: float = 0
    boss_battle_spillover_level: int = 0
    boss_battle_spillover: float = 0
    robbinghood_level: int = 0
    robbinghood: float | None = None
    looty_booty_level: int = 0
    looty_booty: float | None = None
    graded_rate: float = 0
    talents: float = 0
    flat_total: float = 0
    total: float = 100


class DropRate:
    def __init__(self):
        self.passive_cards: list[tuple[list, float]] = []
        self.flat_cards: list = []
        self.multi_cards: list = []
        self.card_sets: dict[str, CardSetProgress] = {}
        # Account-wide flat groups
        self.general = 0
        self.master_classes = 0
        self.world_1 = 0
        self.world_2 = 0
        self.world_3 = 0
        self.world_4 = 0
        self.world_5 = 0
        self.world_6 = 0.0
        self.world_7 = 0
        self.companions = 0.0
        self.total_flat = 0
        # Sources shown by the section
        self.deathbringer_pack = 0
        self.obols_family = 0
        self.trove_sigil = 0
        self.trove_sigil_max = 0
        self.ballot = 0
        self.big_big_hampter = 0
        self.summoning_gm = 0
        self.hatrack = 0
        self.hatrack_multi = 0
        self.gallery = 0
        self.gallery_multi = 0
        # Multis
        self.royal_statue_multi = 1
        self.archlord_multi = 1
        self.sneaking_mastery = 0
        self.island_explorer_multi = 1
        self.special_multi = 1
        self.companion_multi = 1
        self.characters: list[CharacterDropRate] = []

    def calculate(
        self,
        *,
        best_talent_level: Callable,
        class_kill_talent_value: Callable,
        characters,
        cards,
        guild_bonuses,
        friend_bonuses,
        vault,
        gemshop,
        grimoire,
        royal_armory,
        owl,
        stamps,
        arcade,
        obols,
        alchemy_bubbles,
        alchemy_p2w,
        alchemy_vials,
        artifacts,
        ballot,
        equinox,
        armor_sets,
        hat_rack,
        breeding,
        tome,
        caverns,
        achievements,
        farming,
        summoning,
        emperor,
        legend_talents,
        spelunk,
        research,
        gallery,
        world_progress,
        companions,
        class_kill_talents,
        sneaking,
        sushi_station,
        jelly_operator,
        glimbo,
        minehead,
        family_bonuses,
        beanstalk,
        star_signs,
        tesseract,
        prayers,
        shrines,
        lab_bonuses,
        reset_counters,
    ):
        self._calculate_cards(cards)
        self._calculate_account_wide(
            cards=cards,
            guild_bonuses=guild_bonuses,
            friend_bonuses=friend_bonuses,
            vault=vault,
            gemshop=gemshop,
            grimoire=grimoire,
            royal_armory=royal_armory,
            owl=owl,
            stamps=stamps,
            arcade=arcade,
            obols=obols,
            alchemy_bubbles=alchemy_bubbles,
            alchemy_p2w=alchemy_p2w,
            alchemy_vials=alchemy_vials,
            artifacts=artifacts,
            ballot=ballot,
            equinox=equinox,
            armor_sets=armor_sets,
            hat_rack=hat_rack,
            breeding=breeding,
            tome=tome,
            caverns=caverns,
            achievements=achievements,
            farming=farming,
            summoning=summoning,
            emperor=emperor,
            legend_talents=legend_talents,
            spelunk=spelunk,
            research=research,
            gallery=gallery,
            world_progress=world_progress,
            companions=companions,
            class_kill_talents=class_kill_talents,
            sneaking=sneaking,
            sushi_station=sushi_station,
            jelly_operator=jelly_operator,
            glimbo=glimbo,
            minehead=minehead,
        )
        self.characters = [
            self._calculate_character(
                character,
                best_talent_level=best_talent_level,
                class_kill_talent_value=class_kill_talent_value,
                characters=characters,
                legend_talents=legend_talents,
                research=research,
                family_bonuses=family_bonuses,
                gallery=gallery,
                beanstalk=beanstalk,
                star_signs=star_signs,
                breeding=breeding,
                tesseract=tesseract,
                prayers=prayers,
                shrines=shrines,
                artifacts=artifacts,
                lab_bonuses=lab_bonuses,
                reset_counters=reset_counters,
                royal_armory=royal_armory,
                farming=farming,
            )
            for character in characters
        ]

    def _calculate_cards(self, cards):
        self.passive_cards = [
            ([card for card in cards if card.name in names], cap)
            for names, cap in passive_drop_rate_card_caps
        ]
        self.flat_cards = sorted(
            (card for card in cards if card.name in drop_rate_cards),
            key=lambda c: c.getCurrentValue(),
            reverse=True,
        )
        self.multi_cards = [
            card
            for card in cards
            if card.description == drop_rate_multi_card_description
        ]
        for cardset, per_star in card_set_drop_rate.items():
            cards_in_set = [card for card in cards if card.cardset == cardset]
            stars_sum = sum(min(card.star, max_card_stars) + 1 for card in cards_in_set)
            star = min(stars_sum // len(cards_in_set), max_card_stars)
            next_star_sum = (star + 1) * len(cards_in_set)
            if stars_sum == next_star_sum:
                star += 1
            self.card_sets[cardset] = CardSetProgress(
                stars_sum, star, next_star_sum, per_star * star
            )

    def _calculate_account_wide(
        self,
        *,
        cards,
        guild_bonuses,
        friend_bonuses,
        vault,
        gemshop,
        grimoire,
        royal_armory,
        owl,
        stamps,
        arcade,
        obols,
        alchemy_bubbles,
        alchemy_p2w,
        alchemy_vials,
        artifacts,
        ballot,
        equinox,
        armor_sets,
        hat_rack,
        breeding,
        tome,
        caverns,
        achievements,
        farming,
        summoning,
        emperor,
        legend_talents,
        spelunk,
        research,
        gallery,
        world_progress,
        companions,
        class_kill_talents,
        sneaking,
        sushi_station,
        jelly_operator,
        glimbo,
        minehead,
    ):
        # General
        self.general = 0
        for group, cap in self.passive_cards:
            self.general += min(cap, sum(card.getCurrentValue() for card in group))
        self.general += guild_bonuses["Gold Charm"].value
        if friend_bonus_drop_rate_index in friend_bonuses:
            self.general += friend_bonuses[friend_bonus_drop_rate_index].value
        self.general += vault.upgrades["Drops for Days"].total_value
        self.deathbringer_pack = (
            deathbringer_pack_drop_rate if gemshop.bundles["bun_v"].owned else 0
        )
        self.general += self.deathbringer_pack

        # Master Classes
        self.master_classes = 0
        self.master_classes += grimoire.upgrades["Skull of Major Droprate"].total_value
        self.royal_statue_multi = ValueToMulti(royal_armory.statues[1].bonus_value)

        # World 1
        self.world_1 = 0
        self.world_1 += owl.bonuses["Drop Rate"].value
        self.world_1 += stamps["Golden Sixes Stamp"].total_value

        # World 2
        self.world_2 = 0
        self.world_2 += arcade[27].value
        self.obols_family = obols.family_bonus_totals.get("Total%_DROP_RATE", 0)
        self.world_2 += self.obols_family
        self.world_2 += alchemy_bubbles["Droppin Loads"].base_value
        trove_level = alchemy_p2w.sigils["Trove"].level
        trove_values = sigils_dict["Trove"]["Values"]
        try:
            self.trove_sigil = trove_values[trove_level] * artifacts.chilled_yarn_multi
        except (IndexError, KeyError):
            logger.error(
                f"Trove Sigil Level of {trove_level} not present in 'sigils_dict'. "
                f"Defaulting to max_sigil_level of {max_sigil_level}"
            )
            self.trove_sigil = (
                trove_values[max_sigil_level] * artifacts.max_chilled_yarn_multi
            )
        self.trove_sigil_max = (
            trove_values[max_sigil_level] * artifacts.max_chilled_yarn_multi
        )
        self.world_2 += self.trove_sigil
        self.ballot = ballot[27].value * ballot[27].active
        self.world_2 += self.ballot

        # World 3
        self.world_3 = 0
        self.world_3 += equinox.upgrades["Faux Jewels"].value
        self.world_3 += armor_sets["EFAUNT SET"].total_value
        self.hatrack = hat_rack.get_bonus_value("Drop Rate")
        self.hatrack_multi = hat_rack.get_bonus_value("Drop Rate Multi")

        # World 4
        self.world_4 = 0
        for species in breeding.species.values():
            for shiny in species.values():
                if shiny.shiny_bonus == "Drop Rate":
                    self.world_4 += shiny.shiny_level
        self.world_4 += tome.drop_rate_bonus

        # World 5
        self.world_5 = 0
        self.world_5 += caverns.villagers["Minau"].measurements[15].value
        schematics = caverns.villagers["Kaipu"].schematics
        self.world_5 += schematics["Gloomie Lootie"].value
        self.world_5 += schematics["Sanctum of LOOT"].value
        monument = caverns.caves["Wisdom Monument"]
        self.world_5 += monument.bonuses["Player Drop Rate"].value

        # World 6
        self.world_6 = 0.0
        self.big_big_hampter = (
            big_big_hampter_drop_rate if achievements["Big Big Hampter"].complete else 0
        )
        self.world_6 += self.big_big_hampter
        self.summoning_gm = (
            summoning_gm_drop_rate if achievements["Summoning GM"].complete else 0
        )
        self.world_6 += self.summoning_gm
        self.world_6 += farming.depot["Highlighter"].value
        self.world_6 += farming.land_rank["Seed of Loot"].value
        self.world_6 += farming.exotic_market["POMMELION SEED"].value
        self.world_6 += summoning.bonuses["Drop Rate"].value
        self.world_6 += emperor["Drop Rate"].value

        # World 7
        self.world_7 = 0
        self.world_7 += legend_talents["Greatest Drop Party Ever"].value
        self.world_7 += spelunk.shop["Golden Hardhat"].value
        self.world_7 += research.grid["Divine Design"].total_value
        self.gallery = 0
        self.gallery_multi = 0
        if world_progress.highest_reached >= 7:
            self.gallery = gallery.bonuses["Drop Rate"][1]
            self.gallery_multi = gallery.bonuses["Drop Rate Multi"][1]

        # Companions
        self.companions = sum(
            (companions[name].bonus for name in drop_rate_flat_companions), 0.0
        )

        # Special multis, applied after the flat bonuses
        archlord = class_kill_talents["Archlord of the Pirates"]
        self.archlord_multi = ValueToMulti(archlord.total_value)
        self.sneaking_mastery = (
            sneaking_mastery_drop_rate if sneaking.unlocked_mastery > 0 else 0
        )
        self.island_explorer_multi = (
            island_explorer_pack_multi if gemshop.bundles["bun_p"].owned else 1
        )
        self.special_multi = (
            ValueToMulti(sneaking.pristine_charms["Cotton Candy"].value)
            * self.royal_statue_multi
            * ValueToMulti(
                sushi_station.get_milestone_bonus_value("Drop Rate")
                + jelly_operator.obstructions["Gold Bangle"].bonus_value
            )
            * glimbo.drop_rate_multi
            * ValueToMulti(tome.drop_rate_multi_bonus)
            * ValueToMulti(minehead[minehead_drop_rate_bonus_index].value)
            * equinox.dreams[drop_rate_dream_number].bonus_multi
            * ValueToMulti(alchemy_vials["Shipinabottle (Pirate Ship Figurine)"].value)
        )
        self.companion_multi = prod(
            companions[name].get_multi("Drop Rate")
            for name in drop_rate_multi_companions
        )

        self.total_flat = (
            self.general
            + self.master_classes
            + self.world_1
            + self.world_2
            + self.world_3
            + self.world_4
            + self.world_5
            + self.world_6
            + self.world_7
            + self.companions
        )

    def _calculate_character(
        self,
        character,
        *,
        best_talent_level: Callable,
        class_kill_talent_value: Callable,
        characters,
        legend_talents,
        research,
        family_bonuses,
        gallery,
        beanstalk,
        star_signs,
        breeding,
        tesseract,
        prayers,
        shrines,
        artifacts,
        lab_bonuses,
        reset_counters,
        royal_armory,
        farming,
    ) -> CharacterDropRate:
        dr = CharacterDropRate()
        legend_talent_multi = ValueToMulti(
            legend_talents["Flopping a Full House"].value
        )
        well_dressed = research.grid["Well Dressed"].value

        # LUK, as a flat % instead of an additive multi
        luk = character.main_stats["LUK"]
        if luk < 1e3:
            dr.luk = (((luk + 1) ** 0.37) - 1) / 40
        else:
            dr.luk = 0.5 * ((luk - 1e3) / (luk + 2500)) + 0.297
        dr.luk *= 1.4
        dr.luk *= 100

        # Cards
        for card in self.flat_cards:
            if card.codename in character.equipped_cards_codenames:
                dr.cards += card.getCurrentValue(optional_character=character)
        dr.cards *= legend_talent_multi
        dr.card_multi = ValueToMulti(
            character.get_equipped_card_bonus(
                drop_rate_multi_card_description, legend_talent_multi
            )
        )
        cardset = self.card_sets.get(character.equipped_cardset)
        if cardset is not None:
            dr.card_set = cardset.value

        dr.family_multi = ValueToMulti(
            family_bonuses.get_character_value(
                "Royal Guardian",
                characters,
                character,
                character.get_talent_value(family_guy_talent_index),
            )
        )

        # Equipment, from worn misc lines
        dr.equipment = sum(
            character.get_gear_misc_bonus(codename, well_dressed)
            for codename in flat_drop_rate_codenames
        )
        dr.equipment_multi = sum(
            character.get_gear_misc_bonus(codename, well_dressed)
            for codename in drop_rate_multi_codenames
        )
        # Gallery/Hatrack join the misc totals once open for this character
        gallery_active = character.gallery_bonus_active
        hatrack_active = character.hatrack_bonus_active
        has_motherboard = "Silkrode Motherboard" in character.equipped_lab_chips
        dr.gallery = gallery_active * gallery.get_character_bonus_value(
            "Drop Rate", has_motherboard
        )
        dr.gallery_multi = gallery_active * gallery.get_character_bonus_value(
            "Drop Rate Multi", has_motherboard
        )
        dr.hatrack = self.hatrack * hatrack_active
        dr.hatrack_multi = self.hatrack_multi * hatrack_active
        dr.equipment_multi_total = ValueToMulti(
            dr.equipment_multi + dr.gallery_multi + dr.hatrack_multi
        )
        dr.gown_multi = ValueToMulti(
            character.get_gear_misc_bonus(gown_drop_rate_codename, well_dressed)
        )

        dr.golden_food = beanstalk.get_golden_food_bonus(character, golden_food_stat)

        # Star Signs
        dr.silkrode_nanochip_equipped = (
            "Silkrode Nanochip" in character.equipped_lab_chips
        )
        dr.seraph_cosmos_multi = get_seraph_cosmos_multi(
            tesseract.upgrades["Astrology Cultism"].level, character.summoning_level
        )
        applied_seraph_multi = (
            dr.seraph_cosmos_multi if star_signs["Seraph Cosmos"].unlocked else 1
        )
        infinite_star_sign_levels = get_infinite_star_sign_levels(
            breeding.total_shiny_levels["Infinite Star Signs"]
        )
        star_signs_total = 0
        for name, drop_rate in (("Pirate Booty", 5), ("Druipi Major", 12)):
            value = star_signs[name].value_for(
                character, drop_rate, infinite_star_sign_levels, applied_seraph_multi
            )
            dr.star_signs[name] = value
            star_signs_total += value

        dr.post_office = 0
        dr.post_office += character.po_boxes_invested[
            "Non Predatory Loot Box"
        ].bonus_1_value

        midas_minded_equipped = "Midas Minded" in character.equipped_prayers
        dr.prayers = 0
        dr.prayers += prayers["Midas Minded"].bonus_value * midas_minded_equipped

        dr.obols = 0
        dr.obols += character.obols.get("Total%_DROP_RATE", 0)

        # Clover Shrine
        clover_shrine = shrines["Clover Shrine"]
        if artifacts["Moai Head"].level > 0:
            dr.clover_shrine_active = True
        elif lab_bonuses["Shrine World Tour"].enabled:
            dr.clover_shrine_active = (character.current_map_index // 50) == (
                clover_shrine.map_index // 50
            )
        else:
            dr.clover_shrine_active = (
                character.current_map_index == clover_shrine.map_index
            )
        dr.shrines = 0
        dr.shrines += clover_shrine.value * dr.clover_shrine_active

        # Talents
        dr.talents = 0
        bbs = all_talentsDict[boss_battle_spillover_talent_index]
        dr.boss_battle_spillover_level = character.current_preset_talents.get(
            str(boss_battle_spillover_talent_index), 0
        )
        dr.boss_battle_spillover = (
            lava_func(
                funcType=bbs["funcX"],
                level=dr.boss_battle_spillover_level,
                x1=bbs["x1"],
                x2=bbs["x2"],
            )
            * reset_counters.weekly_boss_kills
        )
        dr.talents += dr.boss_battle_spillover
        if character.base_class == "Archer":
            dr.robbinghood_level, dr.robbinghood = self._class_talent(
                character, robbinghood_talent_index
            )
            dr.talents += dr.robbinghood
        if character.base_class == "Journeyman":
            dr.looty_booty_level, dr.looty_booty = self._class_talent(
                character, looty_booty_talent_index
            )
            dr.talents += dr.looty_booty
        dr.graded_rate = royal_armory.get_graded_rate_value(character)
        if dr.graded_rate > 0:
            dr.talents += dr.graded_rate

        # Land rank uses this character's Dank Rank level
        seed_of_loot = farming.land_rank["Seed of Loot"]
        seed_of_loot_own_value = seed_of_loot.get_value(
            farming.get_land_rank_multi(
                best_talent_level(dank_rank_talent_index, character)
            )
        )
        seed_of_loot_correction = seed_of_loot_own_value - seed_of_loot.value

        dr.flat_total = (
            seed_of_loot_correction
            + dr.luk
            + dr.golden_food
            + dr.cards
            + dr.card_set
            + dr.equipment
            + star_signs_total
            + dr.post_office
            + dr.prayers
            + dr.obols
            + dr.shrines
            + dr.talents
            + dr.gallery
            + dr.hatrack
        )

        dr.total = 100
        dr.total += self.total_flat + dr.flat_total
        dr.total *= ValueToMulti(
            class_kill_talent_value("Archlord of the Pirates", character)
        )
        dr.total += self.sneaking_mastery
        dr.total *= self.island_explorer_multi
        # TODO: Arcane Cultist Map-specific Bonus
        dr.total *= self.special_multi
        dr.total *= self.companion_multi
        dr.total *= (
            dr.equipment_multi_total * dr.gown_multi * dr.card_multi * dr.family_multi
        )
        return dr

    @staticmethod
    def _class_talent(character, talent_index: int) -> tuple[int, float]:
        talent = all_talentsDict[talent_index]
        level = character.current_preset_talents.get(str(talent_index), 0)
        if level > 0:
            level += character.total_bonus_talent_levels
        value = lava_func(
            funcType=talent["funcX"], level=level, x1=talent["x1"], x2=talent["x2"]
        )
        return level, value
