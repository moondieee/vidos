import logging

import requests
from fastapi import Depends, HTTPException, Request, status

from core.settings import settings

logger = logging.getLogger(__name__)


async def auth_header(request: Request) -> str | None:
    if authorization := request.headers.get('Authorization'):
        scheme, _, token = authorization.partition(' ')
        if scheme and token and scheme.lower() == 'token':
            return token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid Authorization Header',
        headers={'WWW-Authenticate': 'Token'},
    )


async def auth_base(token: str) -> dict:
    try:
        response = requests.get(
            f'{settings.AUTH_SERVICE_URL}/api/v1/accounts/users/me/',
            headers={
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json'
            }
        )
        if response.status_code == 200:
            user = response.json()
            return user

        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get('detail'),
            headers={'WWW-Authenticate': 'Token'},
        )

    except requests.exceptions.RequestException as err:
        logger.error(f'An error occurred: {err}')
        raise HTTPException(
            status_code=500, detail='An error occurred during the request to auth service'
        )


async def auth(token: str = Depends(auth_header)) -> dict:
    return await auth_base(
        token=token
    )
