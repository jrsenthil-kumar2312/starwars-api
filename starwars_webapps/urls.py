from django.urls import path

from starwars_webapps.views import (
    StarWarsCharactersFilesView,
    ExampleStarWarsCharactersFilesView,
    StarWarsCharactersExtractionView,
)

urlpatterns = [
    path("", StarWarsCharactersFilesView.as_view(), name="clean_file_list"),
    path(
        "example",
        ExampleStarWarsCharactersFilesView.as_view(),
        name="example_clean_file_list",
    ),
    path(
        "save",
        StarWarsCharactersExtractionView.as_view(),
        name="extract_starwars_characters",
    ),
]
