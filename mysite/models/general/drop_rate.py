from collections.abc import Callable
from dataclasses import dataclass, field
from math import prod

from consts.consts_autoreview import EmojiType, ValueToMulti
from consts.consts_general import cards_max_level, max_card_stars
from consts.consts_w1 import (
    get_seraph_cosmos_multi,
    get_seraph_cosmos_summ_level_goal,
    seraph_max,
)
from consts.consts_w2 import (
    max_sigil_level,
    obols_max_bonuses_dict,
    po_box_dict,
    sigils_dict,
)
from consts.consts_w3 import approx_max_talent_level_non_es_non_star, prayers_dict
from consts.consts_w4 import shiny_days_list
from consts.consts_w5 import max_sailing_artifact_level
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
    drop_rate_star_signs,
    flat_drop_rate_codenames,
    golden_food_stat,
    gown_drop_rate_codename,
    island_explorer_pack_multi,
    looty_booty_talent_index,
    max_weekly_boss_difficulties,
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
from models.advice.advice import Advice
from models.w1.star_signs import get_infinite_star_sign_levels
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger
from utils.text_formatting import kebab, notateNumber

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
    # Advice context
    equipped_cardset: str = ""
    summoning_level: int = 0
    seraph_cosmos_unlocked: bool = False
    seraph_cosmos_next_goal: int = 0
    silkrode_nanochip_owned: bool = False
    star_sign_states: dict[str, tuple[bool, bool]] = field(default_factory=dict)
    loot_box: object = None
    midas_minded: object = None
    midas_minded_equipped: bool = False
    clover_shrine: object = None
    chizoar_below_max: bool = False
    weekly_boss_kills: int = 0
    max_talent_level: int = 0

    def get_luk_advice(self) -> Advice:
        return Advice(
            label=f"Stats - LUK: +{round(self.luk, 2)}% Drop Rate",
            picture_class="luk",
        )

    def get_card_set_advice(self, name: str, progress: CardSetProgress) -> Advice:
        equipped = f"(EQUIPPED {EmojiType.CHECK.value}) " * (
            self.equipped_cardset == name
        )
        cap = card_set_drop_rate[name] * (1 + max_card_stars)
        next_level = (
            f"<br>Cards until next set level {progress.stars_sum}/"
            f"{progress.next_star_sum}"
            if progress.stars_sum < progress.next_star_sum
            else ""
        )
        return Advice(
            label=f"{equipped}{{{{ Card Sets|#cards }}}} - {name}: "
            f"+{progress.value}/{cap}% Drop Rate{next_level}",
            picture_class=kebab(name),
            progression=progress.star,
            goal=max_card_stars,
        )

    def get_silkrode_nanochip_advice(self) -> Advice:
        return Advice(
            label="Lab Chips - Silkrode Nanochip: "
            "2x Passive Star Sign Bonuses while equipped",
            picture_class="silkrode-nanochip",
            progression=int(self.silkrode_nanochip_equipped),
            goal=1,
        )

    def get_seraph_cosmos_advice(self) -> Advice:
        next_goal = (
            f"<br>{self.summoning_level}/{self.seraph_cosmos_next_goal} "
            f"summoning levels toward next multi increase."
            if self.seraph_cosmos_multi < seraph_max
            else ""
        )
        return Advice(
            label=f"{{{{ Star Signs|#star-signs }}}} - Seraph Cosmos: "
            f"{round(self.seraph_cosmos_multi, 3):g}/{seraph_max}x "
            f"Passive Star Sign Bonuses{next_goal}",
            picture_class="seraph-cosmos",
            progression=int(self.seraph_cosmos_unlocked),
            goal=1,
        )

    def get_star_sign_advice(self, name: str, picture_class: str) -> Advice:
        value = self.star_signs[name]
        infinite, equipped = self.star_sign_states[name]
        boosted = self.silkrode_nanochip_equipped and infinite
        passive = " (PASSIVE)" if infinite and not boosted else ""
        unboosted = (
            "<br>Not being boosted by Silkrode Nanochip. Equip the Lab Chip!"
            if infinite and self.silkrode_nanochip_owned and not boosted
            else ""
        )
        maxed = boosted or ((equipped or infinite) and not self.silkrode_nanochip_owned)
        return Advice(
            label=f"{{{{ Star Signs|#star-signs }}}} - {name}: "
            f"+{round(value, 1):g}% Drop Rate{passive}{unboosted}",
            picture_class=picture_class,
            progression=int(value > 0 and maxed),
            goal=1,
        )

    def get_loot_box_advice(self) -> Advice:
        box = self.loot_box
        info = next(b for b in po_box_dict.values() if b["Name"] == box.name)
        cap = lava_func(
            funcType=info["1_funcType"],
            level=info["Max Level"],
            x1=info["1_x1"],
            x2=info["1_x2"],
        )
        return Advice(
            label=f"{{{{ Post Office|#post-office }}}} - {box.name}: "
            f"+{round(self.post_office, 1):g}/{round(cap, 1):g}% Drop Rate",
            picture_class=box.name,
            progression=box.level,
            goal=box.max_level,
        )

    def get_midas_minded_advice(self) -> Advice:
        prayer = self.midas_minded
        info = next(p for p in prayers_dict.values() if p["Name"] == prayer.name)
        bonus_cap = lava_func(
            funcType=info["bonus_funcType"],
            level=info["MaxLevel"],
            x1=info["bonus_x1"],
            x2=info["bonus_x2"],
        )
        curse_cap = lava_func(
            funcType=info["curse_funcType"],
            level=info["MaxLevel"],
            x1=info["curse_x1"],
            x2=info["curse_x2"],
        )
        unequipped = (
            ""
            if self.midas_minded_equipped
            else "<br>Equip the prayer to gain its bonus!"
        )
        return Advice(
            label=f"{{{{ Prayers|#prayers }}}} - {prayer.name}: "
            f"+{round(prayer.bonus_value, 1):g}/{round(bonus_cap, 1):g}% Drop Rate | "
            f"+{round(prayer.curse_value, 1):g}/{round(curse_cap, 1):g}% "
            f"Max HP for Monsters CURSE.{unequipped}",
            picture_class=prayer.name,
            progression=prayer.level,
            goal=info["MaxLevel"],
            completed=prayer.level == info["MaxLevel"] and self.midas_minded_equipped,
        )

    def get_obols_advice(self) -> Advice:
        cap = obols_max_bonuses_dict["PlayerDropRateTrue"]
        return Advice(
            label=f"Obols - Personal Obols: +{self.obols}/{cap}% Drop Rate"
            f"<br>Note: Includes Rare and Hyper Obols, each rerolled with +1% DR",
            picture_class="dementia-obol-of-infinisixes",
            progression=self.obols,
            goal=cap,
        )

    def get_clover_shrine_advice(self) -> Advice:
        shrine = self.clover_shrine
        active = f"(ACTIVE {EmojiType.CHECK.value}) " * self.clover_shrine_active
        chizoar = (
            "<br>Note: Can be increased by getting more Chaotic Chizoar card stars"
            if self.chizoar_below_max
            else ""
        )
        return Advice(
            label=f"{active}Shrines - Clover Shrine: "
            f"+{round(shrine.value, 1):g}% Drop Rate{chizoar}",
            picture_class="clover-shrine",
            progression=shrine.level,
            goal=EmojiType.INFINITY.value,
        )

    def get_boss_battle_spillover_advice(self) -> Advice:
        talent = all_talentsDict[boss_battle_spillover_talent_index]
        max_level = 100
        cap = (
            lava_func(
                funcType=talent["funcX"],
                level=max_level,
                x1=talent["x1"],
                x2=talent["x2"],
            )
            * max_weekly_boss_difficulties
        )
        more = (
            "<br>Can be increased by defeating more weekly boss difficulties!"
            if self.weekly_boss_kills < max_weekly_boss_difficulties
            else ""
        )
        return Advice(
            label=f"Special Talent - Boss Battle Spillover: "
            f"+{round(self.boss_battle_spillover, 1)}/{cap}% Drop Rate{more}",
            picture_class="boss-battle-spillover",
            progression=self.boss_battle_spillover_level,
            goal=max_level,
            completed=self.boss_battle_spillover == cap,
        )

    def _class_talent_advice(
        self, talent_index: int, label: str, level: int, value: float
    ) -> Advice:
        talent = all_talentsDict[talent_index]
        cap = lava_func(
            funcType=talent["funcX"],
            level=self.max_talent_level,
            x1=talent["x1"],
            x2=talent["x2"],
        )
        return Advice(
            label=f"{label}: +{round(value, 1)}/{round(cap, 1)}% Drop Rate",
            picture_class=kebab(talent["name"]),
            progression=level,
            goal=self.max_talent_level,
            completed=value == cap,
        )

    def get_robbinghood_advice(self) -> Advice:
        return self._class_talent_advice(
            robbinghood_talent_index,
            "Archer Talent - Robbinghood",
            self.robbinghood_level,
            self.robbinghood,
        )

    def get_looty_booty_advice(self) -> Advice:
        return self._class_talent_advice(
            looty_booty_talent_index,
            "Journeyman Talent - Curse Of Mr Looty Booty",
            self.looty_booty_level,
            self.looty_booty,
        )


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
        # Advice context
        self._bundle_data_present = True
        self._has_deathbringer_pack = False
        self._has_island_explorer_pack = False
        self.chilled_yarn_level = 0
        self._chilled_yarn_multi = 1
        self._chilled_yarn_max = 1
        self._trove_sigil_level = 0
        self._ballot_buff = None
        self.shiny_pets: list[tuple[str, object]] = []
        self._achievements: dict[str, tuple[int, int, bool]] = {}
        self._archlord = None
        self._sneaking_mastery_level = 0
        self._chizoar_below_max = False

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
        chizoar = next(card for card in cards if card.name == "Chaotic Chizoar")
        self._chizoar_below_max = chizoar.getStars() < (cards_max_level - 1)
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
        self._bundle_data_present = gemshop.bundle_data_present
        self._has_deathbringer_pack = gemshop.bundles["bun_v"].owned
        self._has_island_explorer_pack = gemshop.bundles["bun_p"].owned
        self.deathbringer_pack = (
            deathbringer_pack_drop_rate if self._has_deathbringer_pack else 0
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
        self.chilled_yarn_level = artifacts["Chilled Yarn"].level
        self._chilled_yarn_multi = artifacts.chilled_yarn_multi
        self._chilled_yarn_max = artifacts.max_chilled_yarn_multi
        trove_level = alchemy_p2w.sigils["Trove"].level
        self._trove_sigil_level = trove_level
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
        self._ballot_buff = ballot[27]
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
        self.shiny_pets = [
            (name, pet)
            for species in breeding.species.values()
            for name, pet in species.items()
            if pet.shiny_bonus == "Drop Rate"
        ]
        for _, pet in self.shiny_pets:
            self.world_4 += pet.shiny_level
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
        self._achievements = {
            "Big Big Hampter": (
                self.big_big_hampter,
                big_big_hampter_drop_rate,
                achievements["Big Big Hampter"].complete,
            ),
            "Summoning GM": (
                self.summoning_gm,
                summoning_gm_drop_rate,
                achievements["Summoning GM"].complete,
            ),
        }
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
        self._archlord = class_kill_talents["Archlord of the Pirates"]
        self.archlord_multi = ValueToMulti(self._archlord.total_value)
        self._sneaking_mastery_level = sneaking.unlocked_mastery
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
        dr.equipped_cardset = character.equipped_cardset
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
        astrology_cultism = tesseract.upgrades["Astrology Cultism"].level
        dr.summoning_level = character.summoning_level
        dr.seraph_cosmos_multi = get_seraph_cosmos_multi(
            astrology_cultism, character.summoning_level
        )
        dr.seraph_cosmos_next_goal = get_seraph_cosmos_summ_level_goal(
            astrology_cultism, character.summoning_level
        )
        dr.seraph_cosmos_unlocked = star_signs["Seraph Cosmos"].unlocked
        dr.silkrode_nanochip_owned = star_signs.silkrode_owned
        applied_seraph_multi = (
            dr.seraph_cosmos_multi if dr.seraph_cosmos_unlocked else 1
        )
        infinite_star_sign_levels = get_infinite_star_sign_levels(
            breeding.total_shiny_levels["Infinite Star Signs"]
        )
        star_signs_total = 0
        for name, drop_rate, _ in drop_rate_star_signs:
            star_sign = star_signs[name]
            value = star_sign.value_for(
                character, drop_rate, infinite_star_sign_levels, applied_seraph_multi
            )
            dr.star_signs[name] = value
            dr.star_sign_states[name] = (
                star_sign.is_infinite(infinite_star_sign_levels),
                star_sign.is_equipped(character),
            )
            star_signs_total += value

        dr.loot_box = character.po_boxes_invested["Non Predatory Loot Box"]
        dr.post_office = 0
        dr.post_office += dr.loot_box.bonus_1_value

        dr.midas_minded = prayers["Midas Minded"]
        dr.midas_minded_equipped = "Midas Minded" in character.equipped_prayers
        dr.prayers = 0
        dr.prayers += dr.midas_minded.bonus_value * dr.midas_minded_equipped

        dr.obols = 0
        dr.obols += character.obols.get("Total%_DROP_RATE", 0)

        # Clover Shrine
        clover_shrine = shrines["Clover Shrine"]
        dr.clover_shrine = clover_shrine
        dr.chizoar_below_max = self._chizoar_below_max
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
        dr.weekly_boss_kills = reset_counters.weekly_boss_kills
        dr.max_talent_level = character.max_talents_over_books
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

    def _bundle_advice(self, name: str, owned: bool, value_text: str) -> Advice:
        missing = (
            ""
            if self._bundle_data_present
            else ("<br>Note: Could be inaccurate. Bundle data not found!")
        )
        return Advice(
            label=f"{{{{ Gem Shop|#gem-shop }}}} - {name}: {value_text}{missing}",
            picture_class="gem",
            progression=int(owned) if self._bundle_data_present else "IDK",
            goal=1,
        )

    def get_deathbringer_pack_advice(self) -> Advice:
        return self._bundle_advice(
            "Deathbringer Pack",
            self._has_deathbringer_pack,
            f"+{self.deathbringer_pack}/{deathbringer_pack_drop_rate}% Drop Rate",
        )

    def get_island_explorer_pack_advice(self) -> Advice:
        return self._bundle_advice(
            "Island Explorer Pack",
            self._has_island_explorer_pack,
            f"{self.island_explorer_multi}/{island_explorer_pack_multi}x "
            f"Drop Rate MULTI",
        )

    def get_obols_family_advice(self) -> Advice:
        cap = obols_max_bonuses_dict["FamilyDropRateTrue"]
        return Advice(
            label=f"Obols - Family Obols: +{self.obols_family}/{cap}% Drop Rate"
            f"<br>Note: Includes Rare and Hyper Obols, each rerolled with +1% DR",
            picture_class="hyper-six-obol",
            progression=self.obols_family,
            goal=cap,
        )

    def get_chilled_yarn_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Artifacts|#artifacts }}}} - Chilled Yarn: "
            f"{round(self._chilled_yarn_multi, 1):g}/"
            f"{round(self._chilled_yarn_max, 1):g}x Sigil Bonuses"
            f"<br>Note: Improves the sigil below",
            picture_class="chilled-yarn",
            progression=self.chilled_yarn_level,
            goal=max_sailing_artifact_level,
        )

    def get_trove_sigil_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Sigils|#sigils }}}} - Trove Sigil: "
            f"+{self.trove_sigil}/{self.trove_sigil_max}% Drop Rate",
            picture_class="trove",
            progression=self._trove_sigil_level,
            goal=max_sigil_level,
        )

    def get_ballot_advice(self) -> Advice:
        buff = self._ballot_buff
        return Advice(
            label=f"Weekly {{{{ Ballot|#bonus-ballot }}}} - Drop Rate: "
            f"+{round(self.ballot, 2)}/{round(buff.value, 2)}%"
            f"<br>(Buff {buff.status})",
            picture_class="ballot-27",
            progression=int(buff.active),
            goal=1,
            completed=True,
        )

    def get_shiny_pet_advice(self) -> list[Advice]:
        return [
            Advice(
                label=f"{{{{ Breeding|#breeding }}}} - Shiny {name}: "
                f"+{pet.shiny_level}/{len(shiny_days_list)}% Drop Rate",
                picture_class=name,
                progression=pet.shiny_level,
                goal=len(shiny_days_list),
            )
            for name, pet in self.shiny_pets
        ]

    def get_achievement_advice(self, name: str) -> Advice:
        value, cap, complete = self._achievements[name]
        return Advice(
            label=f"{{{{ Achievements|#achievements }}}} - {name}: "
            f"+{value}/{cap}% Drop Rate",
            picture_class=kebab(name),
            progression=int(complete),
            goal=1,
        )

    def get_archlord_advice(self) -> Advice:
        talent = self._archlord
        max_level = approx_max_talent_level_non_es_non_star
        max_multi = ValueToMulti(talent.value_at_level(max_level))
        goal = notateNumber("Basic", 1e6, 2)
        return Advice(
            label=f"Siege Breaker Talent - Archlord of the Pirates: "
            f"{round(self.archlord_multi, 5):g}/{round(max_multi, 5):g}x "
            f"Drop Rate MULTI"
            f"<br>Level {talent.highest_preset_level}/{max_level} "
            f"with your current kills",
            picture_class="archlord-of-the-pirates",
            progression=notateNumber("Match", talent.kills, 2, "", goal),
            goal=goal,
            resource="pirate-flag",
        )

    def get_sneaking_mastery_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Rift|#rift }}}} - Sneaking Mastery: "
            f"+{self.sneaking_mastery}/{sneaking_mastery_drop_rate}% Drop Rate",
            picture_class="sneaking-mastery",
            progression=min(1, self._sneaking_mastery_level),
            goal=1,
        )

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
