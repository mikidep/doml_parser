from cerberus import rules_set_registry

ID_REGEX = r"[a-zA-Z_][a-zA-Z0-9_]*"

keywords = ["get_value", "get_attribute", "concat"]

ID = {
    "type": "string",
    "regex": ID_REGEX,
    "forbidden": keywords
}

C_QUALIFIED_NAME_REGEX = ID_REGEX + r"(\." + ID_REGEX + r")*"

c_qualified_name = {
    "type": "string",
    "regex": C_QUALIFIED_NAME_REGEX,
    "forbidden": keywords
}

C_QUALIFIED_NAME_WITH_WILDCARD_REGEX = C_QUALIFIED_NAME_REGEX + r"(\.\*)?"

c_qualified_name_with_wildcard = {
    "type": "string",
    "regex": C_QUALIFIED_NAME_WITH_WILDCARD_REGEX,
    "forbidden": keywords
}

c_const_value_expression = {
    "anyof": [
        {"type": "boolean"},
        {"type": "integer"},
        {"type": "float"},
        {"type": "string"},
        {"type": "list", "schema": "c_const_value_expression"},
        {
            "type": "dict",
            "keysrules": ID,
            "valuesrules": "c_const_value_expression"
        }
    ]
}

rules_set_registry.add("c_const_value_expression", c_const_value_expression)

simple_value_rules = [
    {"type": "boolean"},
    {"type": "integer"},
    {"type": "float"},
    {"type": "string"},
    {
        "type": "dict",
        "schema": {
            "get_value": {
                "type": "string",
                "regex": r"(super::)?" + C_QUALIFIED_NAME_REGEX,
                "forbidden": keywords
            }
        }
    },
    {
        "type": "dict",
        "schema": {
            "get_attribute": {
                "type": "string",
                "regex": ID_REGEX + r"\." + C_QUALIFIED_NAME_REGEX,
                "forbidden": keywords
            }
        }
    },
    {
        "type": "dict",
        "schema": {
            "concat": {
                "type": "list",
                "schema": "c_simple_value_expression"
            }
        }
    },
    {
        "type": "dict",
        "schema": {
            "get_input": c_qualified_name
        }
    }
]

c_simple_value_expression = {
    "anyof": simple_value_rules
}

rules_set_registry.add("c_simple_value_expression", c_simple_value_expression)

c_value_expression = {
    "anyof": simple_value_rules + [
        {"type": "list", "schema": "c_value_expression"},
        {
            "type": "dict",
            "keysrules": ID,
            "valuesrules": "c_value_expression"
        }
    ]
}

rules_set_registry.add("c_value_expression", c_value_expression)

c_value_data = {
    "anyof": [
        {
            "type": "string",
            "allowed": ["String", "Integer", "Float", "Boolean"]
        },
        c_qualified_name
    ]
}

c_property_body = {
    "type": c_value_data,
    "default": c_const_value_expression | {"required": False},
    "description": {
        "type": "string",
        "required": False
    },
    "required": {
        "type": "boolean",
        "required": False
    },
    "multiple": {
        "type": "boolean",
        "required": False
    }
}

c_data_type_data = {
    "description": {
        "type": "string",
        "required": False
    },
    "extends": c_qualified_name | {"required": False},
    "properties": {
        "keysrules": ID,
        "valuesrules": {
            "type": "dict",
            "schema": c_property_body
        }
    }
}

c_provider = {
    "alias": ID,
    "features": {
        "type": "dict",
        "keysrules": ID,
        "valuesrules": {
            "type": "dict",
            "schema": c_property_body
        }
    }
}

c_metadata = {
    "_version": {
        "type": "string"
    },
    "_provider": ID | {"required": False},
    "_description": {
        "type": "string",
        "required": False
    }
}

c_interface_configure = {
    "ansible_path": {"type": "string"},
    "executor": c_qualified_name | {"required": False},
    "run_data": {
        "type": "dict",
        "required": False,
        "keysrules": ID,
        "valuesrules": c_simple_value_expression
    }
}

c_node_capability_properties = {
    "default_instances": {"type": "integer"},
    "targets": {
        "type": "list",
        "required": False,
        "schema": c_qualified_name
    }
}

c_node_template = {
    "type": c_qualified_name,
    "properties": {
        "type": "dict",
        "required": False,
        "keysrules": c_qualified_name,
        "valuesrules": c_value_expression
    },
    "relationships": {
        "type": "dict",
        "required": False,
        "keysrules": ID,
        "valuesrules": {
            "anyof": [
                ID,
                {
                    "type": "list",
                    "schema": ID
                }
            ]
        }
    },
    "interfaces": {
        "type": "dict",
        "required": False,
        "keysrules": c_qualified_name,
        "valuesrules": {
            "type": "dict",
            "schema": {
                "configure": {
                    "type": "dict",
                    "schema": c_interface_configure
                }
            }
        }
    },
    "capabilities": {
        "type": "dict",
        "required": False,
        "keysrules": ID,
        "valuesrules": {
            "type": "dict",
            "schema": c_node_capability_properties
        }
    }
}

c_node_edge = {
    "type": c_qualified_name,
    "attribute": ID
}

c_node_type_data = {
    "description": {
        "type": "string"
    },
    "alias": ID | {"required": False},
    "extends": c_qualified_name | {"required": False},
    "properties": {
        "type": "dict",
        "required": False,
        "keysrules": ID,
        "valuesrules": {
            "type": "dict",
            "schema": c_property_body
        }
    },
    "node_templates": {
        "type": "dict",
        "required": False,
        "keysrules": ID,
        "valuesrules": {
            "type": "dict",
            "schema": c_node_template
        }
    },
    "edges": {
        "type": "dict",
        "required": False,
        "keysrules": ID,
        "valuesrules": {
            "type": "dict",
            "schema": c_node_edge
        }
    }
}

####################
#    RMDF Model    #
####################

rmdf_model = {
    "metadata": {
        "type": "dict",
        "schema": c_metadata
    },
    "provider": {
        "type": "dict",
        "schema": c_provider,
        "required": False
    },
    "imports": {
        "type": "list",
        "schema": c_qualified_name_with_wildcard,
        "required": False
    },
    "data_types": {
        "type": "dict",
        "keysrules": c_qualified_name,
        "valuesrules": {
            "type": "dict",
            "schema": c_data_type_data
        },
        "required": False
    },
    "node_types": {
        "type": "dict",
        "keysrules": c_qualified_name,
        "valuesrules": {
            "type": "dict",
            "schema": c_node_type_data
        },
        "required": False
    }
}

####################
#    DOML Model    #
####################

c_output = {
    "type": c_value_data,
    "value": c_value_expression
}

doml_model = {
    "metadata": {
        "type": "dict",
        "schema": c_metadata
    },
    "imports": {
        "type": "list",
        "schema": c_qualified_name_with_wildcard,
        "required": False
    },
    "input": {
        "type": "dict",
        "required": False,
        "keysrules": c_qualified_name,
        "valuesrules": {
            "type": "dict",
            "schema": c_property_body
        }
    },
    "node_templates": {
        "type": "dict",
        "required": False,
        "keysrules": ID,
        "valuesrules": {
            "type": "dict",
            "schema": c_node_template
        }
    },
    "output": {
        "type": "dict",
        "required": False,
        "keysrules": c_qualified_name,
        "valuesrules": {
            "type": "dict",
            "schema": c_output
        }
    }
}
