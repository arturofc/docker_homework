FROM python:3.7-slim AS base

ENV FLASK_RUN_HOST="0.0.0.0"
ENV FLASK_RUN_PORT="5000"

RUN pip install --upgrade pip

## Compile Image ##
FROM base AS builder

WORKDIR /app

# Python Dependencies
COPY ./src/requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

## Release Image ##
FROM base

ENV HOME=/home/app
ENV APP_HOME=/home/app/src

# Create non-root application user
RUN addgroup app && useradd -r -d $HOME -s /bin/bash -g app app
RUN mkdir -p $APP_HOME

WORKDIR $APP_HOME

COPY --from=builder "/app/wheels" /wheels
RUN pip install --no-cache /wheels/*

COPY ./src $APP_HOME
RUN chown -R app:app $HOME

USER app

CMD ["flask", "run"]