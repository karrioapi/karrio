

class STRINGFORMAT:
    @staticmethod
    def concat_str(*args, join: bool = False):
        strings = [s for s in args if s != ""]
        if len(strings) == 0:
            return None
        return strings if not join else " ".join(strings)
