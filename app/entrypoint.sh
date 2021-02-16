#!/bin/bash

# Peform Database Migrations
flask db upgrade

exec "$@"