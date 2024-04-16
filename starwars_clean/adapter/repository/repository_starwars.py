from django.db.models import DateField

from starwars.models import StarWarsCharactersFileMetadata
from starwars_clean.domain.models.model_file import File
from starwars_clean.domain.ports.file_repository_starwars import StarWarsFileRepositoryInterface


class StarWarsCharactersFileMetadataRepository(StarWarsFileRepositoryInterface):
    """Star wars characters file metadata data repository."""

    def get_all_files(self) -> list[File]:
        "Retrieve all the star wars characters files name."

        star_wars_files_queryset = StarWarsCharactersFileMetadata.objects.order_by(
            "created_date"
        ).values_list("file_name", "created_date")

        return [
            File(name=file[0], created_date=file[1])
            for file in star_wars_files_queryset
        ]

    def save(self, star_wars_characters_file_name: str) -> None:
        "Save the star wars file metadata"

        star_wars_file_metadata = StarWarsCharactersFileMetadata()
        star_wars_file_metadata.file_name = star_wars_characters_file_name
        star_wars_file_metadata.created_date = DateField(auto_now_add=True)
        star_wars_file_metadata.save()
