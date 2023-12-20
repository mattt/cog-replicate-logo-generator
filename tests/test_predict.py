import pytest
import cog
from PIL import Image

from predict import Predictor


@pytest.mark.parametrize("dimension", [64, 128, 256, 512])
@pytest.mark.parametrize("fill", ["black", "white"])
def test_predict(dimension, fill, vibecheck):
    predictor = Predictor()
    predictor.setup()

    with vibecheck(predictor) as predict:
        output = predict(
            background=None, fill=fill, scale=0.5, dimension=dimension, format="png"
        )

        assert isinstance(output, cog.Path)
        assert output.name == "output.png"

        image = Image.open(output)
        assert image.width == dimension
        assert image.height == dimension

        assert output.exists()
