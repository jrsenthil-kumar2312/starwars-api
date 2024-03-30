from django.urls import path
from . import views

urlpatterns = [
    path("", views.StarWarsCharactersFileListView.as_view(), name="file_list"),
    path(
        "file_detail/<str:star_wars_characters_file_name>",
        views.StarWarsCharactersFileDetailView.as_view(),
        name="file_detail",
    ),
    path(
        "file_duplicate",
        views.StarWarsCharactersFileDuplicateRowCount.as_view(),
        name="file_duplicate",
    ),
    path(
        "star_wars_characters",
        views.StarWarsCharactersExtractionView.as_view(),
        name="get_star_wars_characters",
    ),
]
