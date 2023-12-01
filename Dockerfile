# Building stage
FROM python:3.11-slim-buster as builder

WORKDIR /app
COPY ./pyproject.toml ./poetry.lock /app/
RUN pip install poetry \
  && poetry config virtualenvs.create false \
  && poetry install --no-dev \
  && rm -rf ~/.cache

# Running stage
FROM python:3.11-slim-buster as runner

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

WORKDIR /app

# srcのみコピー。 dataはマウント対応
COPY src /app/src

CMD ["python", "-m", "src.main"]
