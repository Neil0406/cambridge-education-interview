from django.db.models import IntegerChoices
from django.utils.translation import gettext


class Gender(IntegerChoices):
    female = 0, gettext("女")
    male = 1, gettext("男")