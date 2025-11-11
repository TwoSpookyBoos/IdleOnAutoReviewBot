import hashlib
import json
import os
from typing import Callable
import consts.generated


def generate_data_dict(dumped_source_data: str, extractor_function: Callable[[str], dict], target_name: str, target_dict: dict):
    """
    Generate a static data dict in consts.generated from idleon source data.
    """
    dump_hash = hashlib.sha256(dumped_source_data.encode()).hexdigest()
    target_hash = target_dict.get('_hash', None)
    if dump_hash != target_hash:
        new_target = extractor_function(dumped_source_data)
        new_target['_hash'] = dump_hash
        with open(os.path.join(list(consts.generated.__path__)[0], f'{target_name}.py'), 'w') as target_file:
            target_file.write(f'{target_name} = ')
            target_file.write(json.dumps(new_target, indent=4))
            target_file.write("\n")
