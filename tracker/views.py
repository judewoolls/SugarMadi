# tracker/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

@login_required
def dashboard(request):
    return render(request, 'tracker/dashboard.html')