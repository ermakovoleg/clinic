# coding: utf-8
from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=100, verbose_name='ФИО')
    # еще какая то инфа

    def __str__(self):
        return self.name


class Reception(models.Model):
    patient = models.CharField(max_length=100, verbose_name='Пациент')
    doctor = models.ForeignKey(Doctor)
    datetime = models.DateTimeField()

    def __str__(self):
        return "{} - {:%d %B %Y %H:%M} ({})".format(self.patient, self.datetime, self.doctor)