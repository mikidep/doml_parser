# DOML Parser

To check a DOML file, run

```
poetry run python -m doml_parser check <doml-path>
```

To explore the generated DOML model, use the `load_doml_from_path` in the
`doml_parser` module, as exemplified in `doml_parser/__main__.py`. The method
parses and checks the DOML model and the RMDF's in the current directory, and
returns a usable `doml_parser.model.doml_model.DOMLModel` object.