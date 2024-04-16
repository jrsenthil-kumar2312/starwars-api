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
    path("save", StarWarsCharactersExtractionView.as_view(), name="extract_starwars_characters"),
    # path(
    #     "file_detail/<str:star_wars_characters_file_name>",
    #     views.StarWarsCharactersFileDetailView.as_view(),
    #     name="file_detail",
    # ),
    # path(
    #     "file_duplicate",
    #     views.StarWarsCharactersFileDuplicateRowCount.as_view(),
    #     name="file_duplicate",
    # ),
    # path(
    #     "star_wars_characters",
    #     views.StarWarsCharactersExtractionView.as_view(),
    #     name="get_star_wars_characters",
    # ),
]
