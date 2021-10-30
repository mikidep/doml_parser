__version__ = '0.1.0'

from typing import Union
from pathlib import Path

import yaml
import cerberus

from ._yaml_structure_schemas import rmdf_model, doml_model
from .model._unresolved.unres_rmdf_model import UnresRMDFModel
from .model._unresolved.unres_doml_model import UnresDOMLModel
from .model._unresolved.resolver import Resolver, ResolverCtx
from .model.doml_model import DOMLModel
from .errors import InvalidDocument


def load_doml_from_path(
    doml_path: Union[str, Path],
    rmdf_paths: list[Union[str, Path]]
) -> DOMLModel:
    with open(doml_path) as f:
        doml_dict = yaml.load(f, Loader=yaml.Loader)
    rmdf_dicts = []
    for rmdf_path in rmdf_paths:
        with open(rmdf_path) as f:
            rmdf_dicts.append(yaml.load(f, Loader=yaml.Loader))

    rmdf_v = cerberus.Validator(rmdf_model, require_all=True)
    doml_v = cerberus.Validator(doml_model, require_all=True)
    for rmdf_path, rmdf_dict in zip(rmdf_paths, rmdf_dicts):
        if not rmdf_v.validate(rmdf_dict):  # type: ignore
            raise InvalidDocument(
                rmdf_v.error_handler,  # type: ignore
                f"Could not validate document {rmdf_path}."
            )
    if not doml_v.validate(doml_dict):  # type: ignore
        raise InvalidDocument(
            doml_v.error_handler,  # type: ignore
            f"Could not validate document {doml_path}."
        )

    unres_rmdfs = [UnresRMDFModel(rmdf_dict) for rmdf_dict in rmdf_dicts]
    unres_doml = UnresDOMLModel(str(doml_path), doml_dict)
    resolver = Resolver(unres_rmdfs)
    doml = unres_doml.resolve(resolver, ResolverCtx(unres_doml))
    _ = [unres_rmdf.resolve(resolver, ResolverCtx(unres_rmdf))
         for unres_rmdf in unres_rmdfs]

    return doml
