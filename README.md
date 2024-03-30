You'll need to have Docker installed.

Clone this repo anywhere you want and move into the directory:

git clone https://github.com/nickjj/docker-django-example tiretutor_starwars
cd tiretutor_starwars

# Optionally checkout a specific tag, such as: git checkout 0.10.0
Build everything:
The first time you run this it's going to take 1-2 minutes. That's because it's going to download a Python images and build the dependencies.

docker-compose build
docker-compose up
