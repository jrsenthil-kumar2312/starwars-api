import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from starwars.models import StarWarsCharactersFileMetadata


@pytest.mark.django_db
class TestStarWarsCharactersFileListView:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def load_initial_data(self):
        StarWarsCharactersFileMetadata.objects.create(file_name="testing_1.csv")
        StarWarsCharactersFileMetadata.objects.create(file_name="testing_2.csv")

    def test_star_wars_characters_file_list_api(self, load_initial_data, client):
        response = client.get(reverse("file_list"))

        assert response.status_code == 200
        assert "file_list.html" in (t.name for t in response.templates)
        assert "testing_1.csv" in str(response.content)
        assert "testing_2.csv" in str(response.content)

    def test_star_wars_characters_file_list_api_with_empty_list(self, client):
        response = client.get(reverse("file_list"))

        assert response.status_code == 200
        assert "file_list.html" in (t.name for t in response.templates)
        assert (
            str(response.context["star_wars_characters_file_page"]) == "<Page 1 of 1>"
        )


class TestStarWarsCharactersFileDuplicateRowCount:

    @pytest.fixture
    def client(self):
        return APIClient()

    def test_star_wars_characters_file_duplicate_api(self, client):
        response = client.post(
            reverse("file_duplicate"),
            {
                "file_name": "test_star_wars_characters.csv",
                "selected_columns": ["homeworld", "edited"],
            },
        )

        assert len(response.json()) == 4
        assert response.json()[0]["homeworld"] == "Alderaan"

    def test_star_wars_characters_file_duplicate_api_without_selected_columns(
        self, client
    ):
        response = client.post(
            reverse("file_duplicate"),
            {"file_name": "test_star_wars_characters.csv", "selected_columns": []},
        )

        assert len(response.json()) == 10
        assert response.json()[0]["name"] == "Luke Skywalker"

    def test_star_wars_characters_file_duplicate_api_without_file_name(self, client):
        response = client.post(
            reverse("file_duplicate"),
            {"file_name": "", "selected_columns": ["homeworld", "edited"]},
        )

        assert len(response.json()) == 2
        assert response.json()["message"] == "Missing file name"
        assert response.json()["status"] == "false"


class TestStarWarsCharactersFileDetailView:

    @pytest.fixture
    def client(self):
        return APIClient()

    def test_star_wars_characters_file_detail_api(self, client):
        response = client.get(
            reverse(
                "file_detail",
                kwargs={
                    "star_wars_characters_file_name": "test_star_wars_characters.csv"
                },
            )
        )

        assert response.status_code == 200
        assert "file_details.html" in (t.name for t in response.templates)
        assert (
            str(response.context["star_wars_characters_file_name"])
            == "test_star_wars_characters.csv"
        )
        assert (
            str(response.context["star_wars_characters_full_data"][1][0])
            == "Luke Skywalker"
        )

    def test_star_wars_characters_file_detail_api_invalid_file_name(self, client):
        response = client.get(
            reverse(
                "file_detail",
                kwargs={
                    "star_wars_characters_file_name": "test_star_wars_characters_invalid.csv"
                },
            )
        )

        assert response.status_code == 200
        assert (
            str(response.context["star_wars_characters_file_name"])
            == "test_star_wars_characters_invalid.csv"
        )
        assert len(response.context["star_wars_characters_full_data"]) == 0
