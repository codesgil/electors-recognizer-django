from django.utils.translation import ugettext_lazy as _

ROLE_SUPER_ADMIN = 'ROLE_SUPER_ADMIN'
ROLE_ADMIN = 'ROLE_ADMIN'
ROLE_SUPERVISOR = 'ROLE_SUPERVISOR'
ROLE_USER = 'ROLE_USER'
TOKEN = 'TOKEN'
REFRESH_TOKEN = 'REFRESH_TOKEN'


class Form:
    TOKEN_TYPE = (
        (TOKEN, _('Pending')),
        (REFRESH_TOKEN, _('Validated')),
    )

    ROLES = (
        (ROLE_ADMIN, _('Administrator')),
        (ROLE_SUPERVISOR, _('Supervisor')),
        (ROLE_SUPER_ADMIN, _('Super Admin')),
        (ROLE_USER, _('User')),
    )
