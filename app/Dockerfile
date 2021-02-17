FROM python:3.7-slim AS base

ENV FLASK_RUN_HOST="0.0.0.0"
ENV FLASK_RUN_PORT="5000"
ENV DB_HOST=db
ENV DB_PORT=5432

RUN pip install --upgrade pip

## Compile Image ##
FROM base AS builder

WORKDIR /app

RUN mkdir -p /app/opt

# Python Dependencies
COPY ./src/requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Docker-Compose version 3 removes depends_on healthy condition support
# wait-for-it utility: https://docs.docker.com/compose/startup-order
RUN apt-get update && apt-get install -y wget
RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    -O /app/opt/wait-for-it.sh \
    && chmod +x /app/opt/wait-for-it.sh

## Release Image ##
FROM base

ENV HOME="/home/app"
ENV APP_HOME="/home/app/src"

COPY --from=builder "/app/opt" /opt

# Create non-root application user
RUN addgroup app && useradd -r -d $HOME -s /bin/bash -g app app
RUN mkdir -p $APP_HOME

# Copy compiled python packages
COPY --from=builder "/app/wheels" /wheels
RUN pip install --no-cache /wheels/*

# Setup app run
COPY entrypoint.sh .
RUN chmod +x /entrypoint.sh

COPY ./src $APP_HOME

RUN chown -R app:app $HOME
USER app

WORKDIR $APP_HOME

ENTRYPOINT ["/entrypoint.sh"]

CMD ["flask", "run"]