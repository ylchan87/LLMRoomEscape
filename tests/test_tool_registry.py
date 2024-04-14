from typing import Any
from LLMRoomEscape.ToolRegistry import *


def random_number_generator(
        seed: Annotated[int, 'The random seed used by the generator', True],
        range: Annotated[tuple[int, int], 'The range of the generated numbers', True],
) -> int:
    """
    Generates a random number x, s.t. range[0] <= x < range[1]
    """
    if not isinstance(seed, int):
        raise TypeError("Seed must be an integer")
    if not isinstance(range, tuple):
        raise TypeError("Range must be a tuple")
    if not isinstance(range[0], int) or not isinstance(range[1], int):
        raise TypeError("Range must be a tuple of integers")

    import random
    return random.Random(seed).randint(*range)


class Person:
    def __init__(self, name) -> None:
        self.name  = name

    def greet(self, 
              n: Annotated[int, 'The no. of times to greet', True],
              ):
        """
        A warm greeting
        """
        for i in range(n):
            print(f"hi i am {self.name}")


if __name__ == "__main__":
    toolbox = ToolRegistry("toolbox")
    
    personA = Person("Ann")
    personB = Person("Bob")
    toolbox.register_tool(personA.greet)
    toolbox.register_tool(personB.greet)
    print(toolbox.get_tool_descriptions())

    toolbox.dispatch_tool("greet", {"n":3})