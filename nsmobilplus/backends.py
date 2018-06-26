from django.contrib.auth.models import User


class EmailBackend():

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.MultipleObjectsReturned:
            user = User.objects.filter(email=username).order_by('id')[0]
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
            except User.MultipleObjectsReturned:
                user = User.objects.filter(username=username).order_by('id')[0]
            except User.DoesNotExist:
                return None

        if user.check_password(password): # getattr(user, 'is_active') and
            return user
        return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None