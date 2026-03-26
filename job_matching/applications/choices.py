from django.db import models


class StatusLamaran(models.TextChoices):
    PENDING = "Pending", "Pending"
    REVIEW = "Direview", "Direview"
    TERDAFTAR = "Terdaftar", "Terdaftar"
    MENDAN1 = "Mendan 1", "Mendan 1"
    MENDAN2 = "Mendan 2", "Mendan 2"
    MENSETSU = "Mensetsu", "Mensetsu"
    GOUKAKU = "Goukaku", "Goukaku"
    FUGOUKAKU = "Fu Goukaku", "Fu Goukaku"
