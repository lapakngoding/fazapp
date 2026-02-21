from django.urls import path
from .views import TeacherListView, TeacherCreateView

app_name = 'akademik'

urlpatterns = [
    path('teachers/', TeacherListView.as_view(), name='teacher_list'),
    path('teachers/add/', TeacherCreateView.as_view(), name='teacher_create'),
]
