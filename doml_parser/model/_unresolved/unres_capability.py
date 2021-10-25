from . import unres_types as ut


class UnresCapability:
    def __init__(self, name: str, c_dict: dict) -> None:
        self.name = name
        self.default_instances: int = c_dict["default_instances"]
        self.targets: list[ut.Unres] = c_dict.get("targets", [])
