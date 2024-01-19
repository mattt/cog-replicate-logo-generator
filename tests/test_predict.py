import pytest
import cog
from PIL import Image

from predict import Predictor


COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "papayawhip": (255, 239, 213),
    "coral": (255, 127, 80),
    "mediumpurple": (147, 112, 219),
    "lightseagreen": (32, 178, 170),
    "deepskyblue": (0, 191, 255),
    "darkslateblue": (72, 61, 139),
}


@pytest.mark.parametrize("color", COLORS.keys())
@pytest.mark.parametrize("dimension", [64, 128, 256, 512])
@pytest.mark.parametrize("format", ["png", "jpeg"])
def test_predict(color, dimension, format, vibecheck):
    predictor = Predictor()
    predictor.setup()

    background = cog.Path(f"/tmp/{color}.png")
    image = Image.new("RGB", (dimension, dimension), color=COLORS[color])
    image.save(background, format="png")

    with vibecheck(predictor) as predict:
        output: cog.Path = predict(
            background=background,
            fill=None,
            scale=0.5,
            dimension=dimension,
            format=format,
        )

        with Image.open(output) as image:
            try:
                image.verify()
            except Exception as e:
                assert False, f"Verification raised an exception: {e}"

            assert image.format == format.upper()
            assert image.width == dimension
            assert image.height == dimension
