# Описание

# Команды для запуска локально

```sh
$ chmod +x init-ssl.sh
```
```sh
$ ./init-ssl.sh
```
### PROD
```sh
$ docker-compose up -d --build
```

### DEV
```sh
$ docker-compose -f docker-compose.dev.yml up -d --build
```

```sh
$ docker exec -it <container_id> python manage.py createsuperuser
```

## Database dump/load
## Database dump/load
```sh
$ python manage.py dumpdata --natural-foreign --natural-primary --exclude=contenttypes --exclude=auth.Permission --exclude=admin.logentry --exclude=sessions.session --indent 4 > default_data.json

$ python manage.py loaddata default_data.json
```

