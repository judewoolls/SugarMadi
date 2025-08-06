# tracker/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import ExerciseForm, BloodSugarReadingForm, EntryForm, CompleteEntryForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Exercise, BloodSugarReading, Entry


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

@login_required
def create_blood_sugar_reading(request):
    if request.method == 'POST':
        form = BloodSugarReadingForm(request.POST)
        if form.is_valid():
            reading = form.save(commit=False)
            reading.user = request.user
            reading.save()
            messages.success(request, 'Blood sugar reading created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BloodSugarReadingForm()
    return render(request, 'tracker/create_blood_sugar_reading.html', {'form': form})

@login_required
def manage_blood_sugar_readings(request):
    user = request.user
    readings = BloodSugarReading.objects.filter(user=user).order_by('-timestamp')
    return render(request, 'tracker/manage_blood_sugar_readings.html', {'readings': readings})

@login_required
def view_entries(request):
    user = request.user
    entries = Entry.objects.filter(user=user).order_by('-created_at')
    return render(request, 'tracker/view_entries.html', {'entries': entries})

@login_required
def create_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, 'Entry created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EntryForm()
    return render(request, 'tracker/create_entry.html', {'form': form})

@login_required
def complete_entry(request, entry_id):
    try:
        entry = Entry.objects.get(id=entry_id, user=request.user)
    except Entry.DoesNotExist:
        messages.error(request, 'Entry not found.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = CompleteEntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, 'Entry completed successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CompleteEntryForm(instance=entry)

    return render(request, 'tracker/complete_entry.html', {'form': form, 'entry': entry})