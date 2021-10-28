import glob
import yaml

rmdf_paths = glob.glob("tests/**/*.rmdf", recursive=True)

doml_paths = glob.glob("tests/**/*.doml", recursive=True)


def load_all_rmdf_yaml() -> list[tuple[str, dict]]:
    res = []
    for rmdf_path in rmdf_paths:
        with open(rmdf_path) as f:
            res.append((rmdf_path, yaml.load(f, Loader=yaml.Loader)))
    return res


def load_all_doml_yaml() -> list[tuple[str, dict]]:
    res = []
    for doml_path in doml_paths:
        with open(doml_path) as f:
            res.append((doml_path, yaml.load(f, Loader=yaml.Loader)))
    return res
