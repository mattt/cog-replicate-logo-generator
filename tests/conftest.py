from typing import TYPE_CHECKING

import pytest
import cog

if TYPE_CHECKING:
    import cog


@pytest.fixture
def vibecheck():
    class Vibecheck:
        predictor: "cog.BasePredictor"

        def __init__(self, predictor: "cog.BasePredictor"):
            self.predictor = predictor

        def __enter__(self):
            return self.wrapper

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def wrapper(self, **kwargs):
            print("Input", kwargs)
            output = self.predictor.predict(**kwargs)
            print("Output: ", output)
            return output

    return Vibecheck
