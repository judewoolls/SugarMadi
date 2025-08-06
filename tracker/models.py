from django.db import models
from django.contrib.auth.models import User

class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    INTENSITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    intensity = models.CharField(max_length=10, choices=INTENSITY_CHOICES, default='medium')

    def __str__(self):
        return self.name 

class BloodSugarReading(models.Model):
    BEFORE = 'before'
    AFTER = 'after'
    READING_TYPES = [
        (BEFORE, 'Before Exercise'),
        (AFTER, 'After Exercise'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    value = models.DecimalField(        
        max_digits=4,
        decimal_places=1,
        help_text="Blood sugar level in mmol/L")
    reading_type = models.CharField(max_length=6, choices=READING_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_reading_type_display()} - {self.value} mmol/L ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"


class Entry(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    before_reading = models.OneToOneField(BloodSugarReading, on_delete=models.SET_NULL, null=True, blank=True, related_name='before_entry')
    after_reading = models.OneToOneField(BloodSugarReading, on_delete=models.SET_NULL, null=True, blank=True, related_name='after_entry')
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sugar_grams = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        null=True,     # allow null if user doesn't provide
        blank=True,    # allow form to be submitted without this
        help_text="Amount of sugar consumed (grams) during this exercise session",
        default=0.00
    )

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.before_reading and self.before_reading.reading_type != BloodSugarReading.BEFORE:
            raise ValidationError("Before reading must have type 'before'.")
        if self.after_reading and self.after_reading.reading_type != BloodSugarReading.AFTER:
            raise ValidationError("After reading must have type 'after'.")

    def save(self, *args, **kwargs):
        # Automatically set completed if both readings are present
        if self.before_reading and self.after_reading:
            self.completed = True
        else:
            self.completed = False
        super().save(*args, **kwargs)

    def blood_sugar_diff(self):
        if self.before_reading and self.after_reading:
            return self.after_reading.value - self.before_reading.value
        return None

    def __str__(self):
        return f"{self.exercise.name} on {self.date} ({'Completed' if self.completed else 'In Progress'})"

class Snack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    sugar_content = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Sugar content in grams",
        default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.sugar_content}g sugar"