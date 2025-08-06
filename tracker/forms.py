from django import forms
from .models import BloodSugarReading, Entry, Exercise, Snack

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'intensity', 'user']
        labels = {
            'name': 'Exercise Name',
            'description': 'Description (optional)',
            'intensity': 'Intensity Level',
            'user': ''
        }
        help_texts = {
            'name': 'Enter the name of the exercise.',
            'description': 'Optional description of the exercise.',
            'intensity': 'Select the intensity level of the exercise.',
            'user': 'This field is automatically set to the logged-in user.'
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Exercise Name'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Description (optional)'}),
            'intensity': forms.Select(choices=Exercise.INTENSITY_CHOICES, attrs={'class': 'form-select'}),
            'user': forms.HiddenInput()  # Automatically set to the logged-in user
        }


class BloodSugarReadingForm(forms.ModelForm):
    class Meta:
        model = BloodSugarReading
        fields = ['value', 'reading_type']
        widgets = {
            'value': forms.NumberInput(attrs={
                'step': '0.1',
                'placeholder': 'mmol/L'
            }),
            'reading_type': forms.Select()
        }


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['exercise', 'duration_minutes', 'notes', 'before_reading', 'after_reading', 'sugar_grams']
        labels = {
            'exercise': 'Exercise',
            'duration_minutes': 'Duration (minutes)',
            'notes': 'Notes (optional)',
            'before_reading': 'Before Reading',
            'after_reading': 'After Reading',
            'sugar_grams': 'Sugar Consumed (grams, optional)'
        }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'duration_minutes': forms.NumberInput(attrs={'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['before_reading'].queryset = BloodSugarReading.objects.filter(reading_type="before")
        self.fields['after_reading'].queryset = BloodSugarReading.objects.filter(reading_type="after")

class CompleteEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['before_reading', 'after_reading', 'sugar_grams', 'duration_minutes', 'notes']
        labels = {
            'before_reading': 'Before Reading',
            'after_reading': 'After Reading',
            'sugar_grams': 'Sugar Consumed (grams, optional)',
            'duration_minutes': 'Duration (minutes)',
            'notes': 'Notes (optional)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['before_reading'].queryset = BloodSugarReading.objects.filter(reading_type="before")
        self.fields['after_reading'].queryset = BloodSugarReading.objects.filter(reading_type="after")

class SnackForm(forms.ModelForm):
    class Meta:
        model = Snack
        fields = ['name', 'sugar_content', 'user', 'description']
        labels = {
            'name': 'Snack Name',
            'sugar_content': 'Sugar Content (grams)',
            'description': 'Description (optional)',
            'user': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Snack Name'}),
            'sugar_content': forms.NumberInput(attrs={'placeholder': 'Sugar Content (grams)', 'step': '0.1'}),
            'user': forms.HiddenInput()  # Automatically set to the logged-in user
        }