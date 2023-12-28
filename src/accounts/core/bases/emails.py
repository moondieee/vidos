from abc import ABC, abstractmethod


class EmailSender(ABC):
    """Абстрактный класс для подключение сервисов отправки email"""

    @abstractmethod
    def send_registration_email(email: str, password: str) -> None:
        """
        Отправляет пользователю данные созданного и активного аккаунта.

        Создает пользователя по email
        Отправляет html шаблон с логином и паролем клиенту.
        """
        pass
