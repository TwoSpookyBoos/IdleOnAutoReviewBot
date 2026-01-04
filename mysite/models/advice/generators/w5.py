from consts.consts_w5 import max_sailing_artifact_level
from models.advice.advice import Advice
from models.general.session_data import session_data


def get_sailing_artifact_advice(artifact_name: str, include_island_name: bool = False, link_to_section: bool = True) -> Advice:
    artifact = session_data.account.sailing['Artifacts'][artifact_name]
    link_to_section_text = f'{{{{ Artifact|#sailing }}}} - ' if link_to_section else ''
    island_text = f"{artifact['Island']} - " if include_island_name else ''
    advice = Advice(
        label=f"{link_to_section_text}{island_text}{artifact_name}"
              f"<br>{artifact['Description']}"
              f"<br>{artifact['Form']} Bonus: {artifact['FormBonus']}",
        picture_class=artifact['Image'],
        progression=artifact['Level'],
        goal=max_sailing_artifact_level
    )
    return advice
