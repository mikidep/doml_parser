import cerberus

from doml_parser._yaml_structure_schemas import rmdf_model, doml_model
from doml_parser.model._unresolved.unres_rmdf_model import UnresRMDFModel
from doml_parser.model._unresolved.unres_doml_model import UnresDOMLModel
from doml_parser.errors import InvalidDocument
from doml_parser.model._unresolved.resolver import Resolver, ResolverCtx

from tests.utils import load_all_doml_yaml, load_all_rmdf_yaml


def test_rmdf_validation():
    rmdf_v = cerberus.Validator(rmdf_model, require_all=True)
    for rmdf_path, rmdf_dict in load_all_rmdf_yaml():
        if not rmdf_v.validate(rmdf_dict):  # type: ignore
            raise InvalidDocument(
                rmdf_v.error_handler,  # type: ignore
                f"Could not validate document {rmdf_path}."
            )


def test_doml_validation():
    doml_v = cerberus.Validator(doml_model, require_all=True)
    for doml_path, doml_dict in load_all_doml_yaml():
        if not doml_v.validate(doml_dict):  # type: ignore
            raise InvalidDocument(
                doml_v.error_handler,  # type: ignore
                f"Could not validate document {doml_path}."
            )


test_rmdf_validation()
test_doml_validation()

unres_rmdfs = [UnresRMDFModel(rmdf_dict)
               for _, rmdf_dict in load_all_rmdf_yaml()]
unres_domls = [UnresDOMLModel(doml_dict)
               for _, doml_dict in load_all_doml_yaml()]

unres_doml = unres_domls[1]

resolver = Resolver(unres_rmdfs)
ctx = ResolverCtx(unres_doml)
doml = unres_doml.resolve(resolver, ctx)
print("Done!")
