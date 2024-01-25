#!/bin/bash

# Start
echo "Прежде, чем начать создание сетапа:"
echo "Нужно добавить и заполнить .env"
echo "Нужно dev_widget.json с листом тестовых виджетов"
echo "Нужно добавить в директорию текущего уровня 3 видео"
echo "Также у них могут быть только такие названия"
echo "video1.mp4"
echo "video2.mp4"
echo "video3.mp4"

read -p "Введите 'y', если вы добавили эти видео: " response

if [[ "$response" =~ ^[Yy]$|^Yes$ ]]; then
    echo "Setting up is started"
else
    echo "Выход. Видео не добавлены."
    exit 0
fi

# Docker container
ACCOUNTS_ID=$(docker ps -qf "name=accounts")
MONGODB_ID=$(docker ps -qf "name=mongodb")
MINIO_ID=$(docker ps -qf "name=minio")

# loading .env variables
if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

# Checking variables
variables=(
    # MongoDB
    "MONGO_INITDB_ROOT_USERNAME" "MONGO_INITDB_ROOT_PASSWORD"
    "MONGO_HOST" "MONGO_PORT" "MONGO_DATABASE"
    # MinIO
    MINIO_ROOT_USER MINIO_ROOT_PASSWORD
    # Docker containers
    "ACCOUNTS_ID" MONGODB_ID MINIO_ID
)

# Checking the existence of a variable
for var in "${variables[@]}"; do
    if [ -n "${!var}" ]; then
        echo "The $var exists"
    else
        echo "Error: $var variable not found."
    fi
done


# backend accounts set up
echo "Setting up backend accounts"
if [ -n "$ACCOUNTS_ID" ]; then
    echo "The accounts container found"
    echo "Migrate to database"
    docker exec -it $ACCOUNTS_ID poetry run python manage.py migrate
    
    echo "Collecting static"
    docker exec -it $ACCOUNTS_ID poetry run python manage.py collectstatic --no-input
    
    echo "Creating superuser with credentials"
    echo "email: admin@mail.com password: admin"
    docker exec -it $ACCOUNTS_ID poetry run python manage.py createsuperuser --email=admin@mail.com --username=admin --noinput

    # Create password for admin@mail.com
    docker exec -it $ACCOUNTS_ID poetry run python manage.py shell -c "
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

# Get or create the user and print the token
user = get_user_model().objects.get(email='admin@mail.com')
user.set_password('admin')  # Set the desired password, replace 'admin' with the actual password
user.save()
"

    echo "Getting token for admin@mail.com"
    ADMIN_ID=$(docker exec -it $ACCOUNTS_ID poetry run python manage.py shell -c "from rest_framework.authtoken.models import Token; from django.contrib.auth import get_user_model; user = get_user_model().objects.get(email='admin@mail.com'); print(Token.objects.get_or_create(user=user)[0].key)")
    echo "Token for admin@mail.com: $ADMIN_ID"
else
    echo "Error: Container 'accounts' not found."
fi

# video widget schema set up
if [ -n "$MONGO_INITDB_ROOT_USERNAME" ] && [ -n "$MONGO_INITDB_ROOT_PASSWORD" ] && [ -n "$MONGO_HOST" ] && [ -n "$MONGO_PORT" ] && [ -n "$MONGO_DATABASE" ]; then
    echo "Importing dev_widget.json to MongoDB collection video_widgets"

    echo "Copying dev_widget.json to MongoDB container"
    docker cp dev_widget.json $MONGODB_ID:./dev_widget.json

    echo "Importing dev_widget.json to MongoDB collection video_widgets"
    docker exec -i $MONGODB_ID mongoimport --host $MONGO_HOST --port $MONGO_PORT --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin --db $MONGO_DATABASE --collection video_widgets --type json --file ./dev_widget.json --jsonArray

    echo "Removing dev_widget.json from MongoDB container"
    docker exec $MONGODB_ID rm ./dev_widget.json

    echo "dev_widget.json imported successfully."
else
    echo "Error: MongoDB variables not found."
fi

if [ -n "$MINIO_ID" ]; then
    # Creating media bucket with policy
    docker exec -it $MINIO_ID mc alias set play http://localhost:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD --api S3v4

    docker exec -it $MINIO_ID mc mb play/media
    docker exec -it $MINIO_ID mc anonymous set download play/media

    echo "Media bucket with policy created successfully."
else
    echo "Error: Minio container not found."
fi
