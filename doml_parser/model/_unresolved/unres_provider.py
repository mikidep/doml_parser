from .unres_property_def import UnresPropertyDef


class UnresProvider:
    def __init__(self, p_dict: dict) -> None:
        self.alias: str = p_dict["alias"]
        self.features: dict[str, UnresPropertyDef] \
            = {pname: UnresPropertyDef(pname, pd)
               for pname, pd in p_dict["features"].items()}
