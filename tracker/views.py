# tracker/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import ExerciseForm

@login_required
def dashboard(request):
    return render(request, 'tracker/dashboard.html')

@login_required
def create_exercise(request):
    if request.method == 'POST':
        # Handle form submission for creating an exercise
        pass
    else:
        form = ExerciseForm()
        return render(request, 'tracker/create_exercise.html', {'form': form})
    return redirect('dashboard')