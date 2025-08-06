from django.urls import path
from . import views

urlpatterns = [
    path('create_exercise/', views.create_exercise, name='create_exercise'),
    path('manage_exercises/', views.manage_exercises, name='manage_exercises'),
    path('edit_exercise/<int:exercise_id>/', views.edit_exercise, name='edit_exercise'),
    path('delete_exercise/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),
    # other urls...
]