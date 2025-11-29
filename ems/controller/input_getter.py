import ems.view.displayer as displayer
from datetime import datetime

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

def getLine(prompt, allow_blank=False):
    while True:
        user_input = input(prompt)

        if user_input.strip():
            return user_input
        else:
            if allow_blank:
                return None

def getDate(prompt, allow_blank=False):
    while True:
        user_input = input(prompt + " (Ex. January 1, 2001 or Jan 1, 2001): ")

        if allow_blank and not user_input.strip():
            return None

        validDateFormats = ("%B %d, %Y", "%b %d, %Y")

        error = None
        for dateFormat in validDateFormats:
            try:
                date = datetime.strptime(user_input, dateFormat)
                if date > datetime.today(): return date
                else: error = ValueError("Date must be at least 1 day from now.")
            except ValueError as err:
                error = err
                continue

        displayer.show_error(error)


def getTime(prompt, allow_blank=False):
    while True:
        user_input = input(prompt + " (Ex. 7:00 am or 7 am): ")

        if allow_blank and not user_input.strip():
            return None

        validDateFormats = ("%I:%M %p", "%I %p")

        for dateFormat in validDateFormats:
            try:
                return datetime.strptime(user_input, dateFormat)
            except ValueError:
                continue

        try:
            raise ValueError("Invalid time format!")
        except ValueError as err:
            displayer.show_error(err)