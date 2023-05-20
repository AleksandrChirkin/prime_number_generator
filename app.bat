@echo OFF
IF NOT EXIST "db.sqlite3" (
  python manage.py migrate
  python manage.py makemigrations generator
  python manage.py sqlmigrate generator 0001
  python manage.py migrate
)
python manage.py runserver 8000
pause