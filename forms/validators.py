from datetime import date
from dateutil.relativedelta import relativedelta
from wtforms import ValidationError


class AgeVerification:
    def __init__(self, min=-1, max=-1, message=f"Incorrect age"):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field):
        if not self.min <= relativedelta(date.today(), field.data).years <= self.max:
            raise ValidationError(self.message)
