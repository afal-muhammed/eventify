import datetime
from applications.events.models import Events
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View


class LandingView(View):

    def get(self, request):
        now = datetime.datetime.now()
        events = Events.objects.filter(is_published=True, end_date__gte=datetime.datetime.now()).order_by('start_date')
        paginator = Paginator(events, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(self.request, 'landing.html', {'now': now, 'page_obj': page_obj})
