from django.urls import path
from applications.accounts import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('my-events/', views.MyEventsView.as_view(), name="my-events"),
    ]
# TODO: Uncomment below lines for final deployment
# handler404 = views.handler404
# handler500 = views.handler500