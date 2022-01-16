from django.urls import path
from applications.events import views
# from applications.accounts.views import handler500, handler404

urlpatterns = [
    path('', views.LandingView.as_view(), name="landing")
    ]