import cerberus.errors


class InvalidDocument(Exception):
    def __init__(self,
                 error_handler: cerberus.errors.BasicErrorHandler,
                 *args: object) -> None:
        super().__init__(*args)
        self.error_handler = error_handler


class InvalidRawValue(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class TypeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ReferenceNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MultipleDefinitions(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class StructureError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
