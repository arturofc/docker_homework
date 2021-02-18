## Installation

### TL;DR
```
# build all (relevant) services
docker-compose build

# run services in detached mode
docker-compose up -d

# clean up all services and clear database data
docker-compose down -v
```

### Services

#### Configuration
Using a `.env` in the project root directory, you can configure the following parameters
```
## app service
APP_PORT=<> # localhost port where app service is available
FLASK_RUN_PORT=<> # container port for app service
```
Note: overriding the following values will require updating application config's [SQLALCHEMY_DATABASE_URI](app/src/application.cfg)
```
## db service
DB_USER="<>" # name of database user used by the app service
DB_PASSWORD="<>" # password of database user used by the app service
DB_DATABASE="<>" # logical database used by the app service
```

#### Database
```
# Running stand-alone db service
docker-compose up db

# Stop db container and persist database data
docker-compose stop
```

#### App
```
# Running (still depends on the db service for startup)
docker-compose up app

# Rerun Flask database migrations manually
docker-compose run app -- flask db upgrade
```
Note: For local development, the application's source code ([src](app/src)) is mounted to the container at the flask app's main directory to avoid having to rebuild the image after each change


## Simple Intergration Testing
```
docker-compose up -d

# Upload provided test.csv. Should return 200 status and `Success!` html body after redirect
curl -i -L -F 'file=@test.tsv' http://localhost:${APP_PORT:-5000}/upload

# Upload invalid file. Should return 200 status and `Invalid file` html body
curl -i -L -F 'file=@README.md' http://localhost:${APP_PORT:-5000}/upload
```

## Potential Improvements / Next Steps:
- Replace with [application.cfg](app/src/application.cfg) with a `config.py` file to enable the following
    - Generate database uri connection string from environment variables for local development so database credentials can be defined in one place
    - Modularize database authentication to use different methods in other environments. Such as IAM-Based-Auth or Secrets Manager/Vault lookup for credentials
- Run unit testing framework(s) (pytest, coverage.py, etc.) in app service docker container
    - Example Usage: `docker-compose run app -- cd /home/app/test  && python -m pytest -v ./test-reports:/home/app/test/reports`
- Create a integration testing suite / playbook for testing more variations of test.csv