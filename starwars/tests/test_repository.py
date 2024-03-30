import pytest

from starwars.models import StarWarsCharactersFileMetadata
from starwars.repository import StarWarsCharactersFileMetadataRepository


@pytest.mark.django_db
class TestStarWarsCharactersFileMetadataRepository:
    @pytest.fixture
    def load_initial_data(self):
        StarWarsCharactersFileMetadata.objects.create(file_name="testing_1.csv")
        StarWarsCharactersFileMetadata.objects.create(file_name="testing_2.csv")

    def test_retrieve_all(self, load_initial_data):
        star_wars_metadata_repo = StarWarsCharactersFileMetadataRepository()
        file_name_results = star_wars_metadata_repo.retrieve_all_files_name()

        assert "testing_1.csv" in file_name_results
        assert "testing_2.csv" in file_name_results

    def test_save(self):
        star_wars_metadata_repo = StarWarsCharactersFileMetadataRepository()
        star_wars_metadata_repo.save(star_wars_characters_file_name="testing_save.csv")

        starwars_metadata = StarWarsCharactersFileMetadata.objects.all()

        assert starwars_metadata.count() == 1
        assert starwars_metadata[0].file_name == "testing_save.csv"
