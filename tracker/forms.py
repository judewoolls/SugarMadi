from django import forms
from .models import BloodSugarReading, Entry, Exercise

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
        fields = ['exercise', 'duration_minutes', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'duration_minutes': forms.NumberInput(attrs={'min': 1}),
        }

class CompleteEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['before_reading', 'after_reading']
