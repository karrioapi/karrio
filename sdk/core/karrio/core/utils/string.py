import typing


class STRINGFORMAT:
    @staticmethod
    def concat_str(
        *values,
        join: bool = False,
        separator: str = " ",
    ) -> typing.Optional[typing.Union[str, typing.List[str]]]:
        """Concatenate a set of string values into a list of string or a single joined text.

        :param values: a set of string values.
        :param join: indicate whether to join into a single string.
        :param separator: the text separator if joined into a single string.
        :return: a string, list of string or None.
        """
        strings = [s for s in values if s not in ["", None]]

        if len(strings) == 0:
            return None

        if join:
            return separator.join(strings)

        return strings
