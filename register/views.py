# coding: utf-8
from datetime import datetime


from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import FormView, TemplateView, ListView, View
from django.http import JsonResponse

from .models import Reception, Doctor
from .forms import ReceptionForm


class ReceptionView(ListView):
    template_name = 'base.html'
    queryset = Doctor.objects.all()
    context_object_name = 'doctors'


class DoctorView(View):

    def get(self, request, *args, **kwargs):
        date_raw = request.GET.get('date')
        doctor_id = int(kwargs.get('id', 0))
        time_raw = int(request.GET.get('time', 0))

        if not (date_raw and doctor_id):
            return JsonResponse({"type": "error", "message": "Bad data"})

        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return JsonResponse({"type": "error", "message": "Bad doctor_id"})


        date = datetime.strptime(date_raw, '%Y-%m-%d').date()

        if date.isoweekday() in [6, 7]:
            return JsonResponse({"type": "error", "message": "Выходной"})
        if date < datetime.now().date():
            return JsonResponse({"type": "error", "message": "Так нельзя"})

        receptions = doctor.reception_set.filter(datetime__contains=date)

        busy_time = []
        for r in receptions:
            busy_time.append(r.datetime.hour)

        if time_raw and time_raw in range(9, 18):
            r = receptions.filter(datetime__hour=time_raw)
            if r.exists():
                return JsonResponse({"type": "error", "message": "Время уже занято", "busy_time": busy_time})
            return JsonResponse({"type": "success"})

        return JsonResponse({"type": "success", "busy_time": busy_time})


    def post(self, request, *args, **kwargs):
        date_raw = request.POST.get('date')
        doctor_id = int(kwargs.get('id', 0))
        time_raw = int(request.POST.get('time', 0))
        fio = request.POST.get('fio', '')

        if not (date_raw and doctor_id and time_raw and fio):
            return JsonResponse({"type": "error", "message": "Bad data"})

        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return JsonResponse({"type": "error", "message": "Bad doctor_id"})


        date = datetime.strptime("{} {}".format(date_raw, time_raw), '%Y-%m-%d %H')

        if date < datetime.now():
            return JsonResponse({"type": "error", "message": "Так нельзя"})

        receptions = doctor.reception_set.filter(datetime__contains=date)

        if receptions.exists() and time_raw in range(9, 18):
            return JsonResponse({"type": "error", "message": "Время уже занято"})

        reception = Reception(doctor_id=doctor.id, patient=fio, datetime=date)
        reception.save()
        message = "{} записанн к {}. Время {:%d %B %Y %H:%M}".format(fio, doctor.name, date)
        return JsonResponse({"type": "success", "message": message})











