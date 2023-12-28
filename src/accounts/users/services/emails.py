from accounts.core.bases.emails import EmailSender


class VkEmail(EmailSender):
    def send_registration_email(email: str, password: str, *args, **kwargs) -> None:
        pass
