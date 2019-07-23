"""
Provide implementation of single user password endpoint.
"""
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user.domain.errors import (
    SpecifiedUserPasswordIsIncorrectError,
    UserWithSpecifiedEmailAddressDoesNotExistError,
)
from user.domain.objects import ChangeUserPassword
from user.forms import ChangeUserPasswordForm
from user.models import User


class UserPasswordSingle(APIView):
    """
    Single user password endpoint implementation.
    """

    authentication_classes = (JSONWebTokenAuthentication,)

    def __init__(self):
        """
        Constructor.
        """
        self.user = User()

    def post(self, request):
        """
        Change user password.
        """
        email = request.user.email

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        form = ChangeUserPasswordForm({
            'old_password': old_password,
            'new_password': new_password,
        })

        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=HTTPStatus.BAD_REQUEST)

        try:
            ChangeUserPassword(user=self.user).do(email=email, old_password=old_password, new_password=new_password)
        except (
            SpecifiedUserPasswordIsIncorrectError,
            UserWithSpecifiedEmailAddressDoesNotExistError,
        ) as error:
            return JsonResponse({'error': error.message}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'result': 'Password has been changed.'}, status=HTTPStatus.OK)