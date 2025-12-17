# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pygeometa",
# ]
# ///
__version__ = "0.1.0"
import argparse
import pathlib
from pygeometa.core import read_mcf
from pygeometa.schemas.iso19139 import ISO19139OutputSchema


def parse_args() -> dict:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="Input path to the MCF files."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Output path to the XML files."
    )
    args = parser.parse_args()
    return vars(args)


def mcf_to_iso19139(input_path: str, output_path: str) -> None:
    """Convert MCF file to ISO 19139."""
    mcf_dict = read_mcf(input_path)
    iso_os = ISO19139OutputSchema()
    xml_string = iso_os.write(mcf_dict)
    with open(output_path, "w") as ff:
        ff.write(xml_string)


def main(input: str, output: str) -> None:
    """Main access point of the converter."""
    input_path = pathlib.Path(input)
    output_path = pathlib.Path(output)
    output_path.mkdir(exist_ok=True)
    mcf_files = list(input_path.glob("*.yml"))
    xml_files = [
        output_path / mcf.with_suffix(".xml").name for mcf in mcf_files
    ]
    for mcf_file, xml_file in zip(mcf_files, xml_files):
        mcf_to_iso19139(mcf_file, xml_file)


if __name__ == "__main__":
    args = parse_args()
    main(**args)
