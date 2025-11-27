_DISPLAY_WIDTH = 150

def _display_header(header, upper_left, upper_right, middle, center, lower_left, lower_right):
    upper_border = f"{upper_left}" + str(middle) * (_DISPLAY_WIDTH - 2) + f"{upper_right}"
    lower_border = f"{lower_left}" + str(middle) * (_DISPLAY_WIDTH - 2) + f"{lower_right}"
    centered_header = f"{center}" + str(header).center(_DISPLAY_WIDTH - 2) + f"{center}"

    print(upper_border)
    print(centered_header)
    print(lower_border)

def display_header(header):
    _display_header(header, '╔', '╗', '═', '║', '╚', '╝')

def display_subheader(header):
    _display_header(header, '+', '+', '-', '|', '+', '+')

def display_menu(guide_msg, options):
    print(guide_msg)
    for i, option in enumerate(options, start=1):
        print(f"\t[{i}] {option}")

def show_error(error):
    print(f"Error: {type(error).__name__}, Message: {str(error)}\n")

def displayTable(table_name, column_headers, records, column_sizes):
    table_width = _DISPLAY_WIDTH - len(column_headers)

    column_widths = [int(table_width * size) for size in column_sizes[:-1]]
    column_widths.append(table_width - sum(column_widths))

    def print_row(cells, column_widths):
        print("|", end="")
        for i, cell in enumerate(cells):
            centered = str(cell).center(column_widths[i]) if i != 0 else str(cell).center(column_widths[i] - 1)
            print(centered + "|", end="")
        print("\n" + "-" * _DISPLAY_WIDTH)

    display_subheader(table_name)
    print_row(column_headers, column_widths)
    for record in records:
        print_row(record, column_widths)

    print()