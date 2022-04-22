import datetime
import logging
import traceback

from django.contrib.auth import logout
from django.utils.translation import ugettext_lazy as _
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView

from api.settings import SIMPLE_JWT
from core.forms import AddVoteOffice
from globals.ordering import CustomOrdering
from globals.permissions import IsAdminUser
from globals.utils import format_form_errors_response
from .constants import REFRESH_TOKEN
from .constants import ROLE_SUPER_ADMIN
from .filters import UserFilter
from .forms import UserForm, UserUpdateForm, ProfileForm, LogOutForm
from .models import User, BlackListedToken
from .serializers import UserSerializer, ProfileSerializer, ChangePasswordSerializer


@api_view()
def error_404_page(request, exception=None):
    return Response({'errors': {'message': _('Page not found')}}, status=status.HTTP_404_NOT_FOUND)


class RefreshTokenView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            data = request.data
            blacklisted_token = BlackListedToken.objects.filter(token=data['refresh'], type=REFRESH_TOKEN)
            if blacklisted_token:
                raise InvalidToken()
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['post'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout_form = LogOutForm(request.data or {})
    if not logout_form.is_valid():
        return Response(
            data=format_form_errors_response(logout_form.errors),
            status=status.HTTP_400_BAD_REQUEST
        )
    user = request.user
    try:
        data = logout_form.cleaned_data
        now = datetime.datetime.now()
        user.last_login = now.strftime("%Y-%m-%d %H:%M:%S")
        token = request.auth.token.decode("utf-8")
        expired_at = now + SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        blacklisted = BlackListedToken.objects.filter(user=user, token=token).last()
        if not blacklisted:
            BlackListedToken.objects.create(user=user, token=token, jti=request.auth['jti'], expired_at=expired_at)
        blacklisted = BlackListedToken.objects.filter(user=user, token=data['refresh']).last()
        if not blacklisted:
            BlackListedToken.objects.create(user=user, token=data['refresh'], type=REFRESH_TOKEN)
        user.save()
        logout(request)
        return Response()
    except Exception as ex:
        tb = traceback.format_exc()
        logging.getLogger('errors_file').error(msg=tb)
        return Response(data={'detail': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View For User.
class UserView(viewsets.ModelViewSet):
    """
    Provides a get method handler.
    """
    renderer_classes = [JSONRenderer]
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend, CustomOrdering)
    filterset_class = UserFilter
    permission_classes = (IsAdminUser,)
    allowed_custom_filters = ['last_login', 'username', 'is_active', 'role', 'first_name', 'created_at', 'id']
    fields_related = {
        'last_login': 'last_login',
        'username': 'username',
        'is_active': 'is_active',
        'role': 'role',
        'first_name': 'profile__first_name',
        'created_at': 'created_at',
        'id': 'id',
    }

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        group = []
        if self.action == 'me':
            group = ['me']
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'group': group
        }

    def get_queryset(self):
        user = self.request.user
        if user.role == ROLE_SUPER_ADMIN:
            queryset = User.objects.filter(deleted=False)
        else:
            queryset = User.objects.filter(deleted=False).exclude(role=ROLE_SUPER_ADMIN)
        return queryset

    def create(self, request, *args, **kwargs):
        user_form = UserForm(request.data or {})
        profile_form = ProfileForm(request.data or {})
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save()
            user.profile = profile
            user.save()
            serializer = self.get_serializer(user, many=False)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        errors = {**user_form.errors, **profile_form.errors}
        return Response(
            data=format_form_errors_response(errors),
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user_form = UserUpdateForm(instance=instance, data=request.data or {})
        profile_form = ProfileForm(instance=instance.profile, data=request.data or {})
        if user_form.is_valid() and profile_form.is_valid():
            profile = profile_form.save()
            user_form.profile = profile
            user = user_form.save()
            serializer = self.get_serializer(user, many=False)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        errors = {**user_form.errors, **profile_form.errors}
        return Response(
            data=format_form_errors_response(errors),
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.username = user.username + "-1"
        user.deleted = True
        user.is_active = False
        user.deleted_at = datetime.datetime.now()
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], url_path='change-password')
    def change_password(self, request, *args, **kwargs):
        user = request.user
        change_password = ChangePasswordSerializer(data=request.data or {})
        if change_password.is_valid():
            passwords = change_password.data
            if user.check_password(passwords['old_password']):
                user.set_password(passwords['password'])
                user.save()
                serializer = self.get_serializer(user, many=False)
                return Response(
                    data=serializer.data,
                    status=status.HTTP_200_OK
                )
            errors = {"old_password": ["Wrong password."]}
        else:
            errors = change_password.errors
        return Response(
            data=format_form_errors_response(errors),
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['post'], url_path='username/exists')
    def check_username(self, request, *args, **kwargs):
        data = request.data
        errors = {"username": ["This field is required."]}
        if 'username' in data:
            users = User.objects.filter(username=data['username'])
            if users:
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(
            data=format_form_errors_response(errors),
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['put'], url_path='(?P<pk>.+)/vote-office')
    def vote_office(self, request, *args, **kwargs):
        instance = self.get_object()
        form = AddVoteOffice(data=request.data or {})
        if form.is_valid():
            data = form.cleaned_data
            instance.voteOffice = data['voteOffice']
            instance.save()
            serializer = self.get_serializer(instance, many=False)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(
            data=format_form_errors_response(form.errors),
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    if not isinstance(user, User):
        return Response(data={'message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    profile = user.profile
    profile_form = ProfileForm(instance=profile, data=request.data or {})
    if profile_form.is_valid():
        profile = profile_form.save()
        serializer = ProfileSerializer(profile, many=False)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    return Response(
        data=format_form_errors_response(profile_form.errors),
        status=status.HTTP_400_BAD_REQUEST
    )
