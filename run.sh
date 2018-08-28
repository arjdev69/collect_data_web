chromium-browser&
clear
source collect_env/bin/activate
cd collect/
python manage.py makemigrations
python manage.py migrate
python manage.py runserver