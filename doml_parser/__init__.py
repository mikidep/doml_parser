__version__ = '0.1.0'

import os
from typing import Union

import yaml
import cerberus

from .errors import InvalidDocument
from . import _yaml_structure_schemas as yss
from .model.rmdf_model import RMDFModel


def rmdf_model_from_file(rmdf_path: Union[str, bytes, os.PathLike]) \
        -> RMDFModel:
    rmdf_v = cerberus.Validator(yss.rmdf_model, require_all=True)
    with open(rmdf_path) as f:
        rmdf_dict = yaml.load(f, Loader=yaml.Loader)
    if not rmdf_v.validate(rmdf_dict):  # type: ignore
        raise InvalidDocument(rmdf_v.error_handler)  # type: ignore
