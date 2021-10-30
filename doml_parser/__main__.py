from typing import cast, Union
from pathlib import Path
from glob import glob

from docopt import docopt

from . import load_doml_from_path


def main() -> None:
    args = docopt("Usage: doml_parser check <doml-path>")
    doml_path = args["<doml-path>"]
    rmdf_paths = cast(list[Union[str, Path]],
                      glob("**/*.rmdf", recursive=True))

    load_doml_from_path(doml_path, rmdf_paths)


main()
