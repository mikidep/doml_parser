from typing import cast, Union
from pathlib import Path
from glob import glob

from doml_parser import load_doml_from_path

rmdf_paths = cast(list[Union[str, Path]],
                  glob("**/*.rmdf", recursive=True))
doml_paths = cast(list[Union[str, Path]],
                  glob("**/*.doml", recursive=True))

for doml_path in doml_paths:
    print("Path:", doml_path)
    load_doml_from_path(doml_path, rmdf_paths)
