run:
    uv run python manage.py runserver
migrate-last:
    uv run python manage.py migrate
migrate-first:
    uv run python manage.py makemigrations
migrate: migrate-first migrate-last
format:
    uv run isort .
    uv run black .

clean:
    find "${@:-.}" -type f -name "*.py[co]" -delete
    find "${@:-.}" -type d -name "__pycache__" -delete
    find "${@:-.}" -depth -type d -name ".mypy_cache" -exec rm -r "{}" +
    find "${@:-.}" -depth -type d -name ".pytest_cache" -exec rm -r "{}" +
createadmin:
    uv run python manage.py createsuperuser
default: run