# Vidos - видеовиджет

### Микросервисная архитектура

backend сервисы:
  
- Accounts: Отвечает за взаимодействие с пользователями. Используется Django REST Framework (DRF).

- Video Insert: Отвечает за загрузку видео на сервис. Используется FastAPI, MongoDB, MinIO

- Video Redactor: Отвечает за создание структуры виджета. Используется Django REST Framework (DRF), DRFmongoengine, MongoDB

- Video widget schema provider: Отвечает за то, чтобы виджеты получали свои структуры и на основе них отображали контент. Используется FastAPI, MongoDB

### Стек используемых основных технологий

| Программа    | Версия |
|--------------|--------|
| Docker       | [не заполнено] |
| Django       | [не заполнено] |
| FastAPI      | [не заполнено] |
| MongoDB      | [не заполнено] |
| PostgreSQL   | [не заполнено] |
| MinIO        | [не заполнено] |
| openCV       | [не заполнено] |

### Документация

https://www.notion.so/Doc-vidos-d3309a619b584c24938aae212edb64b6

### Запуск проекта в dev режиме

Запустите докер compose. Проект будет доступен по 3000 порту

```
docker-compose -f docker-compose.dev.yml up -d
```

Запустить скрипт, создающий сетап
```
dev_set_up.sh
```

Будут созданы после запуска сетап скрипта

- Accounts: пользователь admin. Login: admin@mail.com password: admin
- Объект виджет из файла dev_widget.json
- Бакет для медиа с правами anon read в MinIO

В сервисе accounts через ip или Django admin получить Token для авторизации

Проект доступен по 3000 порту

Через video_insert отправить файлы-видео сервису

Получить схему виджета через video widget schema provider service.
Этот сервис предоставляет свободных доступ схемы виджета.
