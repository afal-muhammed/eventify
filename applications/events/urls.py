from django.urls import path
from applications.events import views
# from applications.accounts.views import handler500, handler404

urlpatterns = [
    path('create-event', views.CreateEventView.as_view(), name="create-event"),
    path('my-events/', views.MyEventsView.as_view(), name="my-events"),
    path('', views.LandingView.as_view(), name="landing")
    ]
