sudo pip3 install -r requirements.txt
if [ ! -f "secret_key.txt" ]; then
  python3 generate_secret.py
fi
if [ ! -f "db.sqlite3" ]; then
  rm generator/migrations/*_initial.py
  python3 manage.py migrate
  python3 manage.py makemigrations generator
  python3 manage.py sqlmigrate generator 0001
  python3 manage.py migrate
fi
python3 manage.py runserver 8000