run:
    python3 -m app.source.main

edit:
    code ./.vscode/CRONOCOOK.code-workspace --profile="cronocook"

create-python:
    uv venv .env/python --python 3.14t --prompt="cronocook"

create-db:
    mariadb -u root -p < ./resources/database/config.sql
    mariadb -u root -p < ./resources/database/seed.sql
