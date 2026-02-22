from django.shortcuts import render
from django.views.generic import ListView, CreateView
from apps.core.mixins import BasePermissionMixin
from django.urls import reverse_lazy
from .models import Teacher, Classroom
from apps.akademik.forms import TeacherForm

class TeacherListView(ListView):
    model = Teacher
    template_name = 'akademik/teacher_list.html'
    context_object_name = 'teachers'

class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'akademik/teacher_form.html'
    success_url = reverse_lazy('akademik:teacher_list')

def dashboard_akademik(request):
    context = {
        'total_guru': Teacher.objects.count(),
        'total_kelas': Classroom.objects.count(),
    }
    return render(request, 'akademik/dashboard.html', context)

class ClassroomListView(ListView):
    model = Classroom
    template_name = 'akademik/classroom_list.html'
    context_object_name = 'classrooms'

