import cerberus

from doml_parser._yaml_structure_schemas import rmdf_model, doml_model

from .utils import load_all_doml_yaml, load_all_rmdf_yaml


def test_rmdf_validation():
    rmdf_v = cerberus.Validator(rmdf_model, require_all=True)
    for rmdf_path, rmdf_dict in load_all_rmdf_yaml():
        if not rmdf_v.validate(rmdf_dict):  # type: ignore
            print("Path:", rmdf_path)
            assert False


def test_doml_validation():
    doml_v = cerberus.Validator(doml_model, require_all=True)
    for doml_path, doml_dict in load_all_doml_yaml():
        if not doml_v.validate(doml_dict):  # type: ignore
            print("Path:", doml_path)
            assert False
