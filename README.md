# Betting App Backend Made With Django 

## Table of contents
* [General info](#info)
* [Technologies](#technologies)
* [Prepare Env](#prepare-env)
* [Setup](#setup)
* [!!!! Documentation !!!!](#documentation)

## Info
This project is for test purpose and is a backend for a betting app.
It consumes data from external api source for competition, fixtures, odds, bet etc. 

The next challenges are:
- Making data retrieval from external api "live"
- Implement a catching system in order to improve the api
- etc
- ect
- ect

	
## Technologies
Main packages used in this project are:
* Django==3.2.19
* django-rest-knox==4.2.0
* djangorestframework==3.13.1

## Prepare Env
* Create an .env.prod file and add this attrs API_FOOTBALL_HOST, API_FOOTBALL_API_KEY, TIMEZONE,

## Setup
To run this project, install it locally using pipenv:

```
$ cd ../{BaseDir}
$ pipenv shell
$ pipenv install
$ python manage.py runserver
```

## Documentation
At the index page of the API, a swagger interface is generated to help on using it.
Postman is the other documentation tool used in this project. It is use for testing views and logics, and sample results are saved for each possible request/endpoint;
The environnement and the collection are saved under the following directory: *documentation/postman/*