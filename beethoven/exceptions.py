from beethoven.utils.casing import to_pascal_case


class ScaleIsNotDiatonic(Exception):
    def __init__(self, scale, message="Scale {} is not diatonic"):
        self.scale = scale
        self.message = message.format(scale.serialize())
        super().__init__(self.message)


class ScaleNotSet(Exception):
    def __init__(self, message="Scale is not set"):
        self.message = message
        super().__init__(self.message)


class InversionOutOfRange(Exception):
    def __init__(self, message="Out of range"):
        self.message = message
        super().__init__(self.message)


class ParserNotFound(Exception):
    def __init__(self, obj_name, message="Couldn't find parser for {obj_name}"):
        self.obj_name = obj_name
        self.message = message.format(obj_name=to_pascal_case(obj_name))
        super().__init__(self.message)


class CouldNotParse(Exception):
    def __init__(
        self, string, obj_name, message="Couldn't parse string='{string}' as {obj_name}"
    ):
        self.string = string
        self.obj_name = obj_name
        self.message = message.format(obj_name=to_pascal_case(obj_name), string=string)
        super().__init__(self.message)


class MixedAlteration(Exception):
    pass
