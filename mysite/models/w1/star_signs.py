from consts.consts_w1 import starsigns_dict


def get_infinite_star_sign_levels(infinite_shiny_levels: int) -> int:
    # Passives don't use up infinite levels
    infinite_levels = infinite_shiny_levels * 2 + 5
    i = 1
    while i < min(len(starsigns_dict), infinite_levels):
        infinite_levels += int(starsigns_dict[i]["Passive"])
        i += 1
    return infinite_levels


def is_infinite_star_sign(sign: dict, infinite_levels: int) -> bool:
    return sign["Unlocked"] and sign["Index"] <= infinite_levels


def star_sign_value(
    sign: dict, character, base: float, infinite_levels: int, seraph_multi: float
) -> float:
    # "StarSigns" in source. Last updated in v2.531.0
    infinite = is_infinite_star_sign(sign, infinite_levels)
    equipped = (sign["Index"] - 1) in character.equipped_star_signs
    if not (infinite or equipped):
        return 0
    value = base * seraph_multi
    if infinite and "Silkrode Nanochip" in character.equipped_lab_chips:
        value *= 2
    return value
