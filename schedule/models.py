from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError


class Activity(models.Model):
    class Day(models.IntegerChoices):
        MON = 0, "Mon"
        TUE = 1, "Tue"
        WED = 2, "Wed"
        THU = 3, "Thu"
        FRI = 4, "Fri"
        SAT = 5, "Sat"
        SUN = 6, "Sun"
        
        

    who = models.CharField("Student/Group", max_length=64)   # e.g., "SS1A" or "Ada"
    day = models.IntegerField(choices=Day.choices)
    title = models.CharField(max_length=100)                 # e.g., "Mathematics"
    start_time = models.TimeField(null=False, blank=False)
    end_time =  models.TimeField(null=False, blank=False)
    location = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    color = models.CharField(max_length=7, blank=True, default="#e5e7eb")  # optional tag color

    class Meta:
        ordering = ["who", "day", "start_time"]

    # def clean(self):
    #     if self.end_time <= self.start_time:
    #         raise ValidationError("end_time must be after start_time.")


    # def clean(self):
    #     if self.start_time and self.end_time:  # only compare if both are filled
    #         if self.start_time >= self.end_time:
    #             raise ValidationError("End time must be after start time.")

    #     # prevent overlaps per student/group & day
    #     qs = Activity.objects.filter(who=self.who, day=self.day)
    #     if self.pk:
    #         qs = qs.exclude(pk=self.pk)
    #     overlaps = qs.filter(start_time__lt=self.end_time, end_time__gt=self.start_time).exists()
    #     if overlaps:
    #         raise ValidationError("Overlaps with another activity for this student/group and day.")
        
        
        
        # from django.core.exceptions import ValidationError
from django.db.models import Q

def clean(self):
    # Only validate if both times are provided
    if self.start_time and self.end_time:
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")

        # Prevent overlapping activities
        if Activity.objects.filter(
            Q(start_time__lt=self.end_time) & Q(end_time__gt=self.start_time)
        ).exists():
            raise ValidationError("This activity overlaps with another one.")


    def __str__(self):
        return f"{self.who} • {self.title} • {self.get_day_display()} {self.start_time}-{self.end_time}"
    
    
    
