# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

import io
import re

from cog import BasePredictor, Input, Path
from PIL import Image, ImageStat
from cairosvg import svg2png
from typing import Tuple


class Logo:
    """A class representing the Replicate logo"""

    fill: str

    def __init__(self, fill: str = "black"):
        self.fill = fill

    @property
    def width(self) -> int:
        return 16

    @property
    def height(self) -> int:
        return 16

    @property
    def svg(self) -> str:
        return f"""
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
                    <g fill="{self.fill}" shape-rendering="crispEdges">
                        <polygon points="16 6.85 16 8.67 9.67 8.67 9.67 16 7.64 16 7.64 6.85 16 6.85" />
                        <polygon points="16 3.43 16 5.24 5.85 5.24 5.85 16 3.82 16 3.82 3.43 16 3.43" />
                        <polygon points="16 0 16 1.81 2.03 1.81 2.03 16 0 16 0 0 16 0" />
                    </g>
                </svg>
                """

    def image(self, size: Tuple[int, int], scale: float) -> Image:
        width, height = size
        return Image.open(
            io.BytesIO(
                svg2png(file_obj=io.StringIO(self.svg), scale=(width // self.width)),
            )
        ).resize((int(width * scale), int(height * scale)), resample=Image.NEAREST)


class Predictor(BasePredictor):
    def predict(
        self,
        background: Path = Input(description="Background image", default=None),
        fill: str = Input(
            description="Fill color for the logo. Automatic if unspecified.",
            default=None,
            choices=["black", "white"],
        ),
        scale: float = Input(
            description="Factor to scale logo by", ge=0, le=1, default=0.5
        ),
        dimension: int = Input(
            description="Dimension of the square image", ge=64, default=512
        ),
        format: str = Input(
            description="Format of the output images",
            choices=["png", "jpeg"],
            default="png",
        ),
    ) -> Path:
        """Run a single prediction on the model"""

        composition = Image.new("RGBA", (dimension, dimension), (0, 0, 0, 255))

        # Load the background image if specified
        if background is not None:
            background_image = Image.open(background)
            background_image.thumbnail((dimension, dimension))
            composition.paste(background_image, (0, 0))

        # Determine the fill color for the logo if not specified
        if fill is None:
            fill = "black" if ImageStat.Stat(composition).mean[0] > 192 else "white"

        # Generate the logo image
        logo_image = Logo(fill=fill).image(size=(dimension, dimension), scale=scale)

        # Calculate the position to center the SVG on the background image
        x = (dimension - logo_image.width) // 2
        y = (dimension - logo_image.height) // 2

        # Composite the SVG image on top of the background image
        composition.paste(logo_image, (x, y), logo_image)

        # Save the output image
        ext = re.sub(r"\W+", "", format)
        if format == "jpeg":
            composition = composition.convert("RGB")
            ext = "jpg"
        filename = f"/tmp/output.{ext}"
        composition.save(filename, format=format)

        return Path(filename)
