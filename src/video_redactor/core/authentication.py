"""
Custom authentication policies.
"""
import logging

import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import (TokenAuthentication,
                                           get_authorization_header)

from .models import User

logger = logging.getLogger(__name__)


class RemoteAccountsServerAuthentication(TokenAuthentication):
    """
    Custom authentication for HTTP requests to the Vidos Accounts service.

    This authentication method relies on a Token provided in the request header.

    To use:
    - Include the token in the 'Authorization' header of the HTTP request.

    Example:
    ```
    Authorization: Token YOUR_TOKEN_HERE
    ```
    """
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        if len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError as exc:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg) from exc

        return self.remote_authentication(token)

    def remote_authentication(self, token):
        """
        Get user data from remote auth server.
        """
        response = requests.get(
            f'{settings.ACCOUNTS_API_URL}/users/me/',
            headers={'Authorization': f'Token {token}'},
            timeout=10
        )

        if response.status_code != 200:
            msg = 'Failed to authenticate by accounts server.'
            logger.critical = (
                '%s. %s, %s',
                msg,
                f'Status Code: {response.status_code}',
                f'Response: {response.text}',
            )
            raise exceptions.AuthenticationFailed('Failed to authenticate by accounts server.')

        user = User(**response.json())
        return user, None
