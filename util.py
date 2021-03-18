import enum

class ExtendedEnum(enum.Enum):
    @classmethod
    def is_valid_value(cls, value):
        return value in [member.value for member in cls]


@enum.unique
class IntEnum(int, ExtendedEnum):
    pass


@enum.unique
class StringEnum(str, ExtendedEnum):
    pass