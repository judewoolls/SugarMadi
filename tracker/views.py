# tracker/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import ExerciseForm
from django.contrib import messages
from .models import Exercise


@login_required
def dashboard(request):
    return render(request, 'tracker/dashboard.html')

@login_required
def manage_exercises(request):
    user = request.user
    exercises = Exercise.objects.filter(user=user)
    return render(request, 'tracker/manage_exercises.html', {'exercises': exercises})

@login_required
def create_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)  # Do not save to the database yet
            exercise.user = request.user       # Set the user to the logged-in user
            exercise.save()                    # Save to the database
            messages.success(request, 'Exercise created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExerciseForm()
    return render(request, 'tracker/create_exercise.html', {'form': form})

@login_required
def edit_exercise(request, exercise_id):
    try:
        exercise = Exercise.objects.get(id=exercise_id, user=request.user)
    except Exercise.DoesNotExist:
        messages.error(request, 'Exercise not found.')
        return redirect('manage_exercises')

    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            exercise = form.save(commit=False)  # Do not save to the database yet
            exercise.user = request.user       # Ensure user is a User instance
            exercise.save() 
            messages.success(request, 'Exercise updated successfully!')
            return redirect('manage_exercises')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExerciseForm(instance=exercise)

    return render(request, 'tracker/edit_exercise.html', {'form': form, 'exercise': exercise})

@login_required
def delete_exercise(request, exercise_id):
    try:
        exercise = Exercise.objects.get(id=exercise_id, user=request.user)
        exercise.delete()
        messages.success(request, 'Exercise deleted successfully!')
    except Exercise.DoesNotExist:
        messages.error(request, 'Exercise not found.')
    return redirect('manage_exercises')