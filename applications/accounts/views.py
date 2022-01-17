import datetime
import json
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from applications.accounts.models import User


class LoginView(View):

    def get(self, request):
        return render(self.request, 'accounts/login.html')

    def post(self, request):
        data = dict()
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST.get('next')
        if username and password:
            user = authenticate(username=username, password=password)
        else:
            data['result'] = "please fill both fields"
            return HttpResponse(json.dumps(data), content_type="application/json")
        if user:
            login(self.request, user)
            if next_url:
                data['next'] = next_url
            data['result'] = "success"
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data['result'] = "invalid credentials"
            return HttpResponse(json.dumps(data), content_type="application/json")


class SignUpView(View):

    def get(self, request):
        return render(self.request, 'accounts/signup.html')

    def post(self, request):
        data = dict()
        if self.request.POST['email'] and self.request.POST['username'] and \
                self.request.POST['password1'] and self.request.POST["password2"]:
            user = User()
            user.first_name = self.request.POST.get('first_name', None)
            user.last_name = self.request.POST.get('last_name', None)
            user.username = self.request.POST['username']
            user.email = self.request.POST['email']
            try:
                validate_email(user.email)
            except ValidationError:
                data['result'] = "Please enter a valid email address"
                return HttpResponse(json.dumps(data),
                                    content_type="application/json")
            if not self.request.POST["password1"] == self.request.POST["password2"]:
                data['result'] = "Both password values should be same"
                return HttpResponse(json.dumps(data),
                                    content_type="application/json")
            user.set_password(self.request.POST['password1'])
            emails_usernames = list(User.objects.values_list("email", "username"))
            lookup_dict = dict(emails_usernames)
            if request.FILES:
                user.image = request.FILES['profile-image']
            if user.email not in lookup_dict.keys() and user.username not in lookup_dict.values():
                user.save()
                data['result'] = "success"
                # login(self.request,user, backend='applications.accounts.backends.EmailModelBackend')
                return HttpResponse(json.dumps(data),
                                    content_type="application/json")
            else:
                data['result'] = "User with same email ID or username already exist.Please login"
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data['result'] = "Fields marked * are mandatory"
            return HttpResponse(json.dumps(data),
                                content_type="application/json")


class LogoutView(View):

    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect('/accounts/login')


def handler404(request, exception, template_name="404.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)
