from consts.idleon.caverns.cavern import HolesInfo
from utils.number_formatting import parse_number
from utils.safer_data_handling import safer_convert

_resource_indexes = HolesInfo[50]
_scale_indexes = HolesInfo[52]
measurement_scales_name = [value.replace("_", " ").title() for value in HolesInfo[53]]
_value = HolesInfo[55]

measurements_data = [
    {
        "Template": (
            template.replace("|", " ")
            .replace("_", " ")
            .replace("+{%", "")
            .replace("访", "&")
            .title()
            .strip()
        ),
        "ScaleIndex": safer_convert(_scale_indexes[index], 0),
        "ResourceIndex": parse_number(_resource_indexes[index]),
        "IsLinear": "TOT" not in _value[index],
        "BaseValue": safer_convert(_value[index].split("TOT")[0], 1),
    }
    for index, template in enumerate(HolesInfo[54])
    if template != "i"  # i is a placeholder for not-implemented
]
max_measurements = len(measurements_data)
