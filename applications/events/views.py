import datetime
import json
from applications.events.models import Events
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View


class LandingView(View):

    def get(self, request):
        now = datetime.datetime.now()
        events = Events.objects.filter(is_published=True, end_date__gte=datetime.datetime.now()).order_by('start_date')
        paginator = Paginator(events, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(self.request, 'landing.html', {'now': now, 'page_obj': page_obj})


class MyEventsView(View):

    @method_decorator(login_required)
    def get(self, request):
        now = datetime.datetime.now()
        events = Events.objects.filter(user_obj=self.request.user).order_by("start_date")
        print(events)
        paginator = Paginator(events, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'events/event-listing.html', {"page_obj": page_obj, 'now': now})


class CreateEventView(View):

    def post(self, request):
        data = dict()
        if not request.POST["title"] or not request.POST["location"] or not request.POST["start_date"]:
            data["result"] = "You are missing any of title, location or start date"
            return HttpResponse(json.dumps(data), content_type="application/json")
        formatted_date = datetime.datetime.fromisoformat(request.POST['start_date'])
        if datetime.datetime.now() >= formatted_date:
            data["result"] = "Start Date should be greater than today"
            return HttpResponse(json.dumps(data),
                                content_type="application/json")
        try:
            event_obj = Events.objects.get(id=request.POST['id'])
        except:
            event_obj = Events()
        event_obj.title = request.POST["title"]
        event_obj.location = request.POST["location"]
        event_obj.description = request.POST["description"]
        event_obj.user_obj = request.user
        event_obj.start_date = request.POST["start_date"]
        event_obj.end_date = request.POST["end_date"]
        if event_obj.end_date and event_obj.end_date <= event_obj.start_date:
            data["result"] = "End date should be greater than start date"
            return HttpResponse(json.dumps(data),
                                content_type="application/json")
        if datetime.datetime.now() >= formatted_date:
            data["result"] = "Start Date should be greater from current time"
            return HttpResponse(json.dumps(data),
                                content_type="application/json")
        if request.FILES:
            event_obj.banner = request.FILES["banner"]
        event_obj.save()
        if request.POST["publish"] == 'on':
            data["publish"] = "ON"
            data["result"] = "success"
            data["slug"] = event_obj.slug
            return HttpResponse(json.dumps(data),
                                content_type="application/json")
        else:
            data["publish"] = "OFF"
            data["result"] = "success"
            return HttpResponse(json.dumps(data),
                                content_type="application/json")
