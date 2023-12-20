import pytest


@pytest.fixture
def vibecheck():
    class Vibecheck:
        def __init__(self):
            pass

        def record(self, input: any, output: any):
            print("Input: ", input)
            print("Output: ", output)

    return Vibecheck()
