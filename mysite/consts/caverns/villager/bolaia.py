from consts.idleon.caverns.cavern import HolesInfo

studies_data = [
    {
        "Template": template.replace("_", " "),  # Description
        "PerLevel": int(HolesInfo[70][index]),  # Scaling value
    }
    for index, template in enumerate(HolesInfo[69])
]
