from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Activity

class WeekView(ListView):
    model = Activity
    template_name = "schedule/week.html"
    context_object_name = "activities"

    def get_queryset(self):
        who = self.request.GET.get("who", "").strip()
        qs = Activity.objects.all().order_by("day", "start_time")
        if who:
            qs = qs.filter(who__iexact=who)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        who = self.request.GET.get("who", "").strip()
        ctx["who"] = who
        # group by day for easy rendering
        by_day = []
        for value, label in Activity.Day.choices:
            items = [a for a in ctx["activities"] if a.day == value]
            by_day.append({"label": label, "items": items})
        ctx["by_day"] = by_day
        return ctx

class ActivityCreate(CreateView):
    model = Activity
    fields = ["who", "day", "title", "start_time", "end_time", "location", "notes", "color"]
    success_url = reverse_lazy("week")

class ActivityUpdate(UpdateView):
    model = Activity
    fields = ["who", "day", "title", "start_time", "end_time", "location", "notes", "color"]
    success_url = reverse_lazy("week")

class ActivityDelete(DeleteView):
    model = Activity
    success_url = reverse_lazy("week")

def activities_json(request):
    who = request.GET.get("who", "").strip()
    qs = Activity.objects.all().order_by("day", "start_time")
    if who:
        qs = qs.filter(who__iexact=who)
    data = [{
        "id": a.id,
        "who": a.who,
        "day": a.day,
        "day_label": a.get_day_display(),
        "title": a.title,
        "start_time": str(a.start_time),
        "end_time": str(a.end_time),
        "location": a.location,
        "notes": a.notes,
        "color": a.color,
    } for a in qs]
    return JsonResponse({"results": data})
