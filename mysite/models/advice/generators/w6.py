from models.advice.advice import Advice
from models.general.session_data import session_data
from utils.number_formatting import round_and_trim


def get_summoning_bonus_advice(
        bonus_name: str,
        endless: bool = False,
        link_to_section: bool = True,
        picture_class: str = 'summoning'
) -> Advice:
    summoning = session_data.account.summoning
    if endless:
        section = 'Endless Summoning Bonuses'
        bonus_value = round_and_trim(summoning['Endless Bonuses'][bonus_name])
        progress_value = summoning['Battles']['Endless']
        next_winner_bonus = summoning['Battles']['Endless'] + 1
        endless_battles = summoning['BattleDetails']['Endless']
        while next_winner_bonus < summoning['Battles']['Endless'] + 20:
            if endless_battles[next_winner_bonus]['RewardType'] == bonus_name:
                break
            next_winner_bonus += 1
        max_value = next_winner_bonus
        picture_class = 'endless-summoning' if picture_class == 'summoning' else picture_class
    else:
        section = 'Summoning Bonuses'
        bonus = session_data.account.summoning['Bonuses'][bonus_name]
        bonus_value = round_and_trim(bonus['Value'])
        progress_value = bonus_value
        max_value = round_and_trim(bonus['Max'])
    value_pattern, _, view_bonus_name = bonus_name.partition(' ')
    link_to_section_text = f"{{{{{section}|#summoning}}}}: " if link_to_section else ''
    bonus_value = (
        value_pattern
        .replace('{', f"{int(bonus_value)}")
        .replace('<', f"{bonus_value}")
    )
    advice = Advice(
        label=f"{link_to_section_text}{view_bonus_name}: {bonus_value}",
        picture_class=picture_class,
        progression=progress_value,
        goal= max_value,
    )
    return advice
