import ems.view.displayer as displayer

def getInt(highest, allow_blank=False):
    while True:
        user_input = input("Enter the number of your option: ")

        if allow_blank and not user_input.strip():
            return -1

        try:
            num_input = int(user_input)
            if num_input < 1 or num_input > highest:
                raise ValueError(f"Input invalid! Only positive integers between 1 and {highest} are allowed")
        except ValueError as err:
            displayer.show_error(err)
        else:
            print()
            return num_input