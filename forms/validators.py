from datetime import date
from dateutil.relativedelta import relativedelta
from wtforms import ValidationError
from wtforms.validators import InputRequired


class AgeVerification:
    def __init__(self, min=0, max=200, message="Insufficient age"):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field):
        if not self.min <= relativedelta(date.today(), field.data).years <= self.max:
            raise ValidationError(self.message)


class RequiredIf(InputRequired):
    def __init__(self, other_field_name, message=None, *args, **kwargs):
        self.other_field_name = other_field_name
        self.message = message

    def __call__(self, form, field):
        if form[self.other_field_name].data:
            super(RequiredIf, self).__call__(form, field)


class ClassCorrectness:
    def __init__(self, message='Specify the class in the format "{class number}-{class letter}", for example "8-A"'):
        self.message = message

    def __call__(self, form, field):
        data = field.data
        if data:
            try:
                if len(data) != 3 or data[1] != "-" or not 0 < int(data[0]) < 12 or data[2] not in ["А", "Б", "В"]:
                    raise Exception
            except Exception:
                raise ValidationError(self.message)
