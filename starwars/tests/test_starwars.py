import pytest

from unittest.mock import patch

from starwars.star_wars import StarWarsCharacters
from starwars.repository import StarWarsCharactersFileMetadataRepository


@pytest.mark.django_db
@patch("starwars.star_wars.fetch_data_from_url")
class TestStarWarsCharacters:

    def test_get_star_wars_characters(self, mocked_fetch_data):
        mocked_fetch_data.return_value = {"results": "test"}
        star_wars_char_handler = StarWarsCharacters()
        response = star_wars_char_handler.get_star_wars_characters()

        assert response == ["t", "e", "s", "t"]

    def test_save_star_wars_csv_file_metadata(self, mocked_fetched_data):
        star_wars_char_handler = StarWarsCharacters()
        star_wars_char_handler.save_star_wars_csv_file_metadata("testing.csv")

        file_names_qs = (
            StarWarsCharactersFileMetadataRepository().retrieve_all_files_name()
        )
        assert file_names_qs[0] == "testing.csv"
