You'll need to have Docker installed.

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
7. I have added some unit tests but it does not cover all the lines.

Clone this repo anywhere you want and move into the directory:

```
git clone https://github.com/jrsenthil-kumar2312/tiretutor-starwars.git tiretutor_starwars
cd tiretutor_starwars
```

Build everything:
The first time you run this it's going to take 1-2 minutes. That's because it's going to download a Python images and build the dependencies.

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
> 3. I have not used any clean architecture concept here apart from the repository layer. It will
     be good to have views -> service -> repository flow as this will create a clear separation.
> 4. Additionally, Pydantic model should be used as data transfer model between the layers stated above.
     This will allow the layers to work together even if the underlying technology changes.
> 5. Another approach I usually take is to code out of the framework (django).This reduces dependencies.
     I did not do it here in order to keep it simple.
> 6. Dependency injection can be used instead of importing lower level module to higher level module. 
     This allows a more isolated unit testing and reduces coupling.
