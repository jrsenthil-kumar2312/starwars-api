import pytest
from datetime import datetime

from unittest import mock
from django.urls import reverse
from rest_framework.test import APIClient

from starwars_clean.api.resources.v1.api_starwars import StarWarsApi
from starwars.models import StarWarsCharactersFileMetadata
from starwars_clean.domain.models.model_file import File

from starwars_clean import container
from starwars_clean.domain.services.service_starwars import StarWarsService


@pytest.mark.django_db
@pytest.mark.freeze_time("2024-04-16 00:00:00", tz_offset=-4)
class TestStarWarsApi:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def starwarsapi(self):
        return StarWarsApi()

    @pytest.fixture
    def load_initial_data(self):
        StarWarsCharactersFileMetadata.objects.create(file_name="testing_1.csv")
        StarWarsCharactersFileMetadata.objects.create(file_name="testing_2.csv")

    def test_get_starwars_characters_files(self, load_initial_data, starwarsapi):
        response = starwarsapi.get_starwars_characters_files()
        assert response[0].name == "testing_1.csv"
        assert response[1].name == "testing_2.csv"


@pytest.mark.django_db
@pytest.mark.freeze_time("2024-04-16 00:00:00", tz_offset=-4)
class TestStarWarsApi:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def load_initial_data(self):
        StarWarsCharactersFileMetadata.objects.create(file_name="testing_1.csv")
        StarWarsCharactersFileMetadata.objects.create(file_name="testing_2.csv")

    def test_get_starwars_characters_files(self, load_initial_data):
        starwars_service_mock = mock.Mock(spec=StarWarsService)
        starwars_service_mock.get_starwars_characters_files.return_value = [
            File(name="testing1.csv", created_date=datetime.now()),
            File(name="testing2.csv", created_date=datetime.now()),
        ]

        with container.starwars_service.override(starwars_service_mock):
            response = StarWarsApi().get_starwars_characters_files()
            assert response[0].name == "testing1.csv"
            assert response[1].name == "testing2.csv"
