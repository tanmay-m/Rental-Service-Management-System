#!/bin/sh

echo "Migrate the Database at startup of project"

python3 manage.py makemigrations

echo "Done with make migrations"
# Wait for few minute and run db migraiton
while ! python manage.py migrate  2>&1; do
   echo "Migration is in progress status"
   sleep 3
done

echo "Django docker is fully configured successfully."

python3 manage.py runserver 0.0.0.0:8080

exec "$@"