class STRINGFORMAT:
    @staticmethod
    def concat_str(*args, join: bool = False, separator: str = " "):
        strings = [s for s in args if s not in ["", None]]
        if len(strings) == 0:
            return None
        return strings if not join else separator.join(strings)
