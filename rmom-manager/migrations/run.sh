#!/bin/bash

export ROOT="$( readlink -f "$( dirname "${BASH_SOURCE[0]}" )" )"

DB_USER=postgres
DB_NAME=rmom_manager
DB_HOST="127.0.0.1"
DB_PORT=5432
DB_PASS=secret

export DATABASE_URL="postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

cd ${ROOT}/..
cargo sqlx migrate --source ${ROOT}/sql run
