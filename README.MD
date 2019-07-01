# Arquitectura microservicios con 12 facto app by Vanessa


[![Build Status](https://api.travis-ci.com/vanessapalacios/s-pedidos.svg?branch=master)](https://travis-ci.org/vanessapalacios/s-pedidos)

## build

```
docker-compose -f docker-compose-dev.yml up -d --build
```


## recreate DB
```
docker-compose -f docker-compose-dev.yml run orders python manage.py recreate_db
```
## test
```
docker-compose -f docker-compose-dev.yml run orders python manage.py test
```
## test COVERAGE
```
docker-compose -f docker-compose-dev.yml exec orders python manage.py cov
```