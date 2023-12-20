import pytest
from predict import Predictor
from cog import Path

from pathlib import PosixPath
from PIL import Image


@pytest.mark.parametrize("dimension", [64, 128, 256, 512])
@pytest.mark.parametrize("fill", ["black", "white"])
def test_predict(dimension, fill, vibecheck):
    predictor = Predictor()
    predictor.setup()

    input = {
        "background": None,
        "fill": fill,
        "scale": 0.5,
        "dimension": dimension,
        "format": "png",
    }
    output: PosixPath = predictor.predict(**input)

    assert isinstance(output, Path)
    assert output.name == "output.png"

    image = Image.open(output)
    assert image.width == dimension
    assert image.height == dimension

    assert output.exists()

    vibecheck.record(input, output)
