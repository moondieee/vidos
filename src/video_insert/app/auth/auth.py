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

        detail = response.json()
        detail['service'] = 'accounts'
        raise HTTPException(
            status_code=response.status_code,
            detail=detail,
            headers={'WWW-Authenticate': 'Token'},
        )

    except requests.exceptions.HTTPError as errh:
        logger.error(f'HTTP Error: {errh}')
        raise HTTPException(status_code=500, detail='HTTP Error occurred')
    except requests.exceptions.ConnectionError as errc:
        logger.error(f'Error Connecting: {errc}')
        raise HTTPException(status_code=500, detail='Connection Error occurred')
    except requests.exceptions.Timeout as errt:
        logger.error(f'Timeout Error: {errt}')
        raise HTTPException(status_code=500, detail='Timeout Error occurred')
    except requests.exceptions.RequestException as err:
        logger.error(f'Something went wrong: {err}')
        raise HTTPException(status_code=500, detail='Something went wrong')


async def auth(token: str = Depends(auth_header)) -> dict:
    return await auth_base(
        token=token
    )
