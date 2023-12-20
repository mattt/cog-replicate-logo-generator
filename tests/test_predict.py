from predict import Predictor


def test_predict():
    predictor = Predictor()
    predictor.setup()

    input = {
        "background": None,
        "fill": "black",
        "scale": 0.5,
        "dimension": 64,
        "format": "png",
    }
    output = predictor.predict(**input)

    assert output.exists()
