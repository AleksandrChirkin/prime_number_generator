sudo apt install python3-django
if [ ! -f "secret_key.txt" ]; then
  ./generate_secret.py
fi
if [ ! -f "db.sqlite3" ]; then
  rm generator/migrations/*_initial.py
  ./manage.py migrate
  ./manage.py makemigrations generator
  ./manage.py sqlmigrate generator 0001
  ./manage.py migrate
fi
./manage.py runserver 8000