if [ ! -f "backup_params.txt" ]; then
  rm generator/migrations/*_initial.py
  rm db.sqlite3*
  python3 manage.py migrate
  python3 manage.py makemigrations generator
  python3 manage.py sqlmigrate generator 0001
  python3 manage.py migrate
fi
python3 manage.py runserver 8000