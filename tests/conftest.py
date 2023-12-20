from typing import TYPE_CHECKING
import hashlib
import json
import pytest
import os
import datetime
import cog

if TYPE_CHECKING:
    import cog


class Vibecheck:
    predictor: "cog.BasePredictor"
    records = []

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

        if isinstance(output, cog.Path):
            # Create a checksum for the file content
            contents = output.read_bytes()
            checksum = hashlib.md5(contents, usedforsecurity=False).hexdigest()
            unique_file = f"/tmp/{checksum}_{output.name}"
            with open(unique_file, "wb") as f:
                f.write(contents)
            output = cog.Path(unique_file)

        self.records.append({"input": kwargs, "output": output})
        return output


@pytest.fixture
def vibecheck():
    return Vibecheck


@pytest.fixture(scope="session", autouse=True)
def write_records(request):
    def _write_records():
        # Create a new directory with timestamp
        # timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # directory = f".vibecheck/{timestamp}"
        directory = ".vibecheck"
        os.makedirs(directory, exist_ok=True)

        # Write records to the new directory
        with open(f"{directory}/manifest.json", "w") as f:
            json.dump(
                [
                    {**record, "output": os.path.basename(record["output"])}
                    for record in Vibecheck.records
                ],
                f,
            )

        # For each output file (cog.Path), write the file to that directory
        for record in Vibecheck.records:
            output = record["output"]
            if isinstance(output, cog.Path):
                with open(f"{directory}/{output.name}", "wb") as f:
                    f.write(output.read_bytes())

    request.addfinalizer(_write_records)
