# Collect_data_web

Collect data from Brazilian courts' websites.

## Step with docker

    * Install docker: https://github.com/jobino/learning_docker

    * Running docker: ./docker/access_docker.sh
  
    * Running shell file: ./settings.sh

    * Run: ./run.sh

    * If Error: Error: That port is already in use. Solution: kill -9 -1 in your terminal.

    * Otherwise access: localhost:8000.

## Step without docker

    * install pip with python3
    * curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    * python3 get-pip.py
    * create a virtualenv. Suggestion name: "collect_env". Follow command -> (virtualenv collect_env)
    * pip install -r requirements.txt
    * python manage.py runserver
