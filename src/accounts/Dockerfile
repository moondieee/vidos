FROM python:3.10.12

RUN pip install poetry

COPY . .

RUN poetry install

CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "accounts.wsgi"]
