DISPLAY_WIDTH = 150

def _display_header(header, upper_left, upper_right, middle, center, lower_left, lower_right):
    upper_border = f"{upper_left}" + str(middle) * (DISPLAY_WIDTH - 2) + f"{upper_right}"
    lower_border = f"{lower_left}" + str(middle) * (DISPLAY_WIDTH - 2) + f"{lower_right}"
    centered_header = f"{center}" + str(header).center(DISPLAY_WIDTH - 2) + f"{center}"

    print(upper_border)
    print(centered_header)
    print(lower_border)

def display_header(header):
    _display_header(header, '╔', '╗', '═', '║', '╚', '╝')

def display_subheader(header):
    _display_header(header, '+', '+', '-', '|', '+', '+')
