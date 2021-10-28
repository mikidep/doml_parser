from doml_parser.model._unresolved.unres_rmdf_model import UnresRMDFModel
from doml_parser.model._unresolved.unres_doml_model import UnresDOMLModel

from .utils import load_all_rmdf_yaml, load_all_doml_yaml


def test_unres_rmdf_construction() -> None:
    for rmdf_path, rmdf_dict in load_all_rmdf_yaml():
        try:
            unres_rmdf = UnresRMDFModel(rmdf_dict)
            unres_rmdf = unres_rmdf
        except Exception:
            print("Error at path: " + rmdf_path)
            raise


def test_unres_doml_construction() -> None:
    for doml_path, doml_dict in load_all_doml_yaml():
        try:
            unres_doml = UnresDOMLModel(doml_dict)
            unres_doml = unres_doml
        except Exception:
            print("Error at path: " + doml_path)
            raise
