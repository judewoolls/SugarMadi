from django.urls import path
from . import views

urlpatterns = [
    path('create_exercise/', views.create_exercise, name='create_exercise'),
    path('manage_exercises/', views.manage_exercises, name='manage_exercises'),
    path('edit_exercise/<int:exercise_id>/', views.edit_exercise, name='edit_exercise'),
    path('delete_exercise/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),
    path('manage_blood_sugar_readings/', views.manage_blood_sugar_readings, name='manage_blood_sugar_readings'),
    path('create_blood_sugar_reading/', views.create_blood_sugar_reading, name='create_blood_sugar_reading'),
    path('delete_blood_sugar_reading/<int:reading_id>/', views.delete_blood_sugar_reading, name='delete_blood_sugar_reading'),
    path('view_entries/', views.view_entries, name='view_entries'),
    path('create_entry/', views.create_entry, name='create_entry'),
    path('complete_entry/<int:entry_id>/', views.complete_entry, name='complete_entry'),
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    # other urls...
]