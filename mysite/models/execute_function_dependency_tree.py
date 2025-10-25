import random
from typing import Callable, Any


def execute_function_dependency_tree(funcs_and_args: dict[Callable, list[Any]], dependencies: dict[Callable, list[Callable]]):
    while dependencies.keys():
        _dependencies = list(dependencies.items())
        next_function = random.sample([function for function, dependencies in _dependencies if not dependencies], k=1)[0]
        next_function(*funcs_and_args[next_function])
        del dependencies[next_function]
        for value in dependencies.values():
            if next_function in value:
                value.remove(next_function)