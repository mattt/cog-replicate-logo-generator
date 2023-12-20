import pytest
import cog
from PIL import Image

from predict import Predictor


@pytest.mark.parametrize("dimension", [64, 128, 256, 512])
# @pytest.mark.parametrize("fill", ["black", "white"])
@pytest.mark.parametrize("format", ["png", "jpeg"])
def test_predict(dimension, format, vibecheck):
    predictor = Predictor()
    predictor.setup()

    with vibecheck(predictor) as predict:
        output: cog.Path = predict(
            background=None, fill=None, scale=0.5, dimension=dimension, format=format
        )

        with Image.open(output) as image:
            try:
                image.verify()
            except Exception as e:
                assert False, f"Verification raised an exception: {e}"

            assert image.format == format.upper()
            assert image.width == dimension
            assert image.height == dimension
