from django.shortcuts import render
from django.views.generic import ListView, CreateView
from apps.core.mixins import BasePermissionMixin
from django.urls import reverse_lazy
from .models import Teacher
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

