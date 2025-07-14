import os


class BarCode:
    def _generate_unique_number(self):
        filename = "last_number.txt"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                last_number = int(f.read().strip())
        else:
            last_number = 0

        new_number = last_number + 1
        with open(filename, "w") as f:
            f.write(str(new_number))

        return str(new_number).zfill(6)

    def _calculate_controle_number(self):
        return self._char_to_code(self._get_barcode_for_control_number())

    def _char_to_code(self, text):
        result = 0
        text = text.upper()
        for char in text:
            if char.isdigit():
                result += int(char)
            elif "A" <= char <= "Z":
                result += ord(char) - ord("A") + 10
            else:
                raise ValueError(f"Invalid character: {char}")
        return result

    def _get_barcode_for_control_number(self):
        return f"{self.post_id}{self.client_id}{self.unique_number}"

    def __init__(self):
        self.post_id = "PS"
        self.client_id = "CHSI"
        self.unique_number = self._generate_unique_number()
        self.control_number = self._calculate_controle_number()

    def get_full_barcode(self):
        return (
            f"*{self.post_id}{self.client_id}{self.unique_number}{self.control_number}*"
        )
