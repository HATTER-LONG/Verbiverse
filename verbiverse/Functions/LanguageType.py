from enum import Enum


class ExplainLanguage(Enum):
    TARGET_LANGUAGE = 1
    MOTHER_TONGUE = 2

    def __eq__(self, other):
        if type(self).__qualname__ != type(other).__qualname__:
            return NotImplemented
        return self.name == other.name and self.value == other.value

    def __hash__(self):
        return hash((type(self).__qualname__, self.name))
