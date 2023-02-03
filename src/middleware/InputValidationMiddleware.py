class InputValidationMiddleware:
    ERR_CHAR = "Forbidden character"
    ERR_BOUNDARIES = "Category number is out of boundaries"
    ERR_RANGE_FORMAT = "Select a range between 2 numbers separated by a '-'"

    def __init__(self):
        self.input_result = {"value": set(), "valid": False, "message": ""}

    @staticmethod
    def _can_conv_to_int(num_str: str) -> bool:
        try:
            int(num_str)
            return True
        except ValueError:
            return False

    def _is_valid_str(self, num_str: str, last: int) -> bool:
        if not self._can_conv_to_int(num_str):
            self.input_result["message"] = self.ERR_CHAR
            return False
        if int(num_str) < 1 or int(num_str) > last:
            self.input_result["message"] = self.ERR_BOUNDARIES
            return False
        return True

    def _is_valid_range(self, range_str: str, last: int) -> bool:
        range_fragment = range_str.split("-")
        if not len(range_fragment) == 2:
            self.input_result["message"] = self.ERR_RANGE_FORMAT
            return False

        left_str, right_str = range_fragment
        if not self._is_valid_str(left_str, last) or not self._is_valid_str(
            right_str, last
        ):
            return False
        return True

    def decode_input(self, user_input: str, last: int) -> None:
        segments = [sub_str.strip() for sub_str in user_input.split(",")]

        for segment in segments:
            # One or two digits category number
            if len(segment) < 3:
                if not self._is_valid_str(segment, last):
                    return self.input_result
                else:
                    self.input_result["value"].add(int(segment))

            # Dash separated category numbers
            elif len(segment) < 6 and "-" in segment:
                if not self._is_valid_range(segment, last):
                    return self.input_result
                else:
                    left_str, right_str = [int(x) for x in segment.split("-")]
                    cat_range = sorted([left_str, right_str])
                    categories = [
                        x for x in range(cat_range[0], cat_range[1] + 1)
                    ]
                    for category_num in categories:
                        self.input_result["value"].add(category_num)

        if len(self.input_result["value"]) > 0:
            self.input_result["valid"] = True
        return self.input_result
