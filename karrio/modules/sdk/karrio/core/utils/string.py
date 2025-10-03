import typing


class STRINGFORMAT:
    @staticmethod
    def concat_str(
        *values,
        join: bool = False,
        separator: str = " ",
        trim: bool = False,
    ) -> typing.Optional[typing.Union[str, typing.List[str]]]:
        """Concatenate a set of string values into a list of string or a single joined text.

        :param values: a set of string values.
        :param join: indicate whether to join into a single string.
        :param separator: the text separator if joined into a single string.
        :param trim: indicate whether to trim the string values.
        :return: a string, list of string or None.
        """
        strings = [
            "".join(s.split(" ")) if trim else s for s in values if s not in ["", None]
        ]

        if len(strings) == 0:
            return None

        if join:
            return separator.join(strings)

        return strings

    @staticmethod
    def to_snake_case(input_string: typing.Optional[str]) -> typing.Optional[str]:
        """Convert any string format to snake case."""
        if input_string is None:
            return None

        # Handle camelCase, PascalCase, and consecutive uppercase letters
        s = ""
        for i, char in enumerate(input_string):
            if char.isupper():
                if i > 0 and not input_string[i - 1].isupper():
                    s += "_"
                s += char.lower()
            else:
                s += char

        # Handle spaces, hyphens, and other separators
        s = "".join([c.lower() if c.isalnum() else "_" for c in s])

        # Remove leading/trailing underscores and collapse multiple underscores
        return "_".join(filter(None, s.split("_")))

    @staticmethod
    def to_slug(
        *values,
        separator: str = "_",
    ) -> typing.Optional[str]:
        """Convert a set of string values into a slug string."""

        processed_values = []
        for value in values:
            if value not in ["", None]:
                # Convert to lowercase and replace spaces with separator
                processed = value.lower().replace(" ", separator)
                # Replace other non-alphanumeric characters with separator
                processed = "".join(
                    c if c.isalnum() or c == separator else separator for c in processed
                )
                # Remove consecutive separators
                while separator * 2 in processed:
                    processed = processed.replace(separator * 2, separator)
                # Remove leading and trailing separators
                processed = processed.strip(separator)
                processed_values.append(processed)

        return separator.join(processed_values) if processed_values else None
