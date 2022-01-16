from django.contrib.auth.backends import ModelBackend
from applications.accounts.models import User


class EmailModelBackend(ModelBackend):
    """
    authentication class to login with the email address.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):

        print(kwargs)
        if '@' in username:
            username = username.lower()
            kwargs = {'email': username}
        else:
            return None
        if password is None:
            return None
        try:
            user = User.objects.get(**kwargs)

        except User.DoesNotExist:
            User.set_password(password)

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
