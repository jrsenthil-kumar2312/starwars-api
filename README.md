You'll need to have Docker installed.

IMPORTANT NOTE:
1. This application uses sqlite as db for ease of development and testing
2. Logging gets saved in a local file: debug.log
3. Migration runs automatically using docker-compose

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
```
