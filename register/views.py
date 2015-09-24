# coding: utf-8
from datetime import datetime, time


from django.http import Http404
from django.views.generic import ListView
from django.http import JsonResponse

from .models import Reception, Doctor


class ReceptionView(ListView):
    template_name = 'base.html'
    queryset = Doctor.objects.all()
    context_object_name = 'doctors'


def doctorview(request, doctor_id):
    if request.is_ajax():
        try:
            doctor = Doctor.objects.get(id=int(doctor_id))
        except Doctor.DoesNotExist:
            return JsonResponse({"type": "error", "message": "Bad doctor_id"})

        fio = None
        time_raw = None

        if request.method == 'POST':
            date_raw = request.POST.get('date')
            time_raw = int(request.POST.get('time', 0))
            fio = request.POST.get('fio', '')
            if not fio:
                return JsonResponse({"type": "error", "message": "Укажите ФИО"})
        else:
            date_raw = request.GET.get('date')

        if not date_raw:
            return JsonResponse({"type": "error", "message": "Укажите дату"})

        date = datetime.strptime(date_raw, '%Y-%m-%d').date()
        if time_raw:
            if time_raw not in range(9, 18):
                return JsonResponse({"type": "error", "message": "Выберите рабочее время"})
            date = datetime.combine(date, time(hour=time_raw))
        else:
            date = datetime.combine(date, datetime.max.time())

        if date.isoweekday() in [6, 7]:
            return JsonResponse({"type": "error", "message": "Выходной"})
        if date < datetime.now():
            return JsonResponse({"type": "error", "message": "Прошедшее время"})

        receptions = doctor.reception_set.filter(datetime__contains=date.date())

        if request.method == 'POST':
            r = receptions.filter(datetime__hour=time_raw)
            if r.exists():
                return JsonResponse({"type": "timeerror", "message": "Время уже занято, попробуйте еще раз"})
            else:
                reception = Reception(doctor_id=doctor.id, patient=fio, datetime=date)
                reception.save()
                message = "ФИО: {}. \nДоктор: {}. \nДата: {:%d %m %Y}  \nВремя: {} часов.".format(fio, doctor.name, date, time_raw)
                return JsonResponse({"type": "success", "message": message})

        else:
            busy_time = []
            for r in receptions:
                busy_time.append(r.datetime.hour)

            return JsonResponse({"type": "success", "busy_time": busy_time})

    else:
       raise Http404("error")