import re


async def parse_string_to_dict(input_string):
    result = {}
    # Raqam va harf juftliklarini topish
    parts = re.findall(r'(\d+)([a-zA-Z])', input_string)

    for part in parts:
        key = int(part[0])  # Raqamni oling
        value = part[1]  # Harfni oling
        result[key] = value

    return result
