class Student:
    def __init__(self):
        self.sr_code = None
        self.program_id = None
        self.year_level = None
        self.last_name = None
        self.middle_name = None
        self.first_name = None

    def set_sr_code(self, sr_code):
        self.sr_code = sr_code

    def set_program_id(self, program_id):
        self.program_id = program_id

    def set_year_level(self, year_level):
        self.year_level = year_level

    def set_last_name(self, last_name):
        self.last_name = last_name

    def set_middle_name(self, middle_name):
        return self.middle_name

    def set_first_name(self, first_name):
        return self.first_name


    def get_sr_code(self):
        return self.sr_code

    def get_program_id(self):
        return self.program_id

    def get_year_level(self):
        return self.year_level

    def get_last_name(self):
        return self.last_name

    def get_middle_name(self):
        return self.middle_name

    def get_first_name(self):
        return self.first_name
