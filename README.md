A simple implementation of StarWars API (SWAPI) using 2 different approach:
1. Writing API within the framework (Django)
2. Writing API out of the framework (Django) - preferred approach with clean architecture with dependency injection. (refer to starwars_clean)

IMPORTANT NOTE:
1. This application uses sqlite as db for ease of development and testing.
2. Logging gets saved in a local file: debug.log
3. Migration runs automatically using docker-compose
4. QUICK_MODE flag = This is enabled by default for ease of testing. When enabled,
   only part of the star wars characters are extracted from SWAPI. To disable it, 
   simply change QUICK_MODE = False in settings.py file.
5. The spinner effect is a dummy spinner, it runs for a fixed period. At times,
   it may take longer for the file to be generated from SWAPI.
   ( do wait a while for the file to be generated.)
6. Files are formatted with isort, black and pylint.

Clone this repo anywhere you want and move into the directory:

```
git clone https://github.com/jrsenthil-kumar2312/tiretutor-starwars.git tiretutor_starwars
cd tiretutor_starwars
```

Build everything:
The initial run will require 1-2 minutes as it downloads a Python image and constructs the necessary dependencies.

```
docker-compose build
docker-compose up

or 

docker-compose up --build
```

The app should be accessible from : http://127.0.0.1:8000/

Swagger is available at the following url: http://127.0.0.1:8000/swagger/


To run the unit tests:
```
docker-compose run --rm web pytest
```

Future improvements:

> 1. Permission to APIs should be restricted instead of allowing it to be accessed by anyone
> 2. These APIs do not have any authentication, a simple JWT implementation will be good to add.
