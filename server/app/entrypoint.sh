#!/bin/bash

# Lance server.py en arrière-plan
python server.py &

# Lance le serveur Django (le & est volontairement omis pour garder le conteneur vivant)
python manage.py runserver 0.0.0.0:8000
