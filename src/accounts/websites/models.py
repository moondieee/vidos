from django.db import models


class Website(models.Model):
    user = models.ForeignKey(
        'users.User',
        verbose_name='Клиент',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Название сайта',
        max_length=255,
        blank=True,
        null=True
    )
    url = models.URLField(
        verbose_name='url адрес',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время добавления сайта',
        db_index=True
    )

    class Meta:
        verbose_name = 'Вебсайт клиента'
        verbose_name = 'Вебсайты клиентов'
        ordering = ('created',)
