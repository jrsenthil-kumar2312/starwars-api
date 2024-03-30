from django.db.models import DateField

from starwars.models import StarWarsCharactersFileMetadata


class StarWarsCharactersFileMetadataRepository:
    """Star wars characters file metadata data repository."""

    def retrieve_all_files_name(self) -> list:
        "Retrieve all the star wars characters files name."

        return StarWarsCharactersFileMetadata.objects.order_by(
            "created_date"
        ).values_list("file_name", flat=True)

    def save(self, star_wars_characters_file_name: str) -> None:
        "Save the star wars file metadata"

        star_wars_file_metadata = StarWarsCharactersFileMetadata()
        star_wars_file_metadata.file_name = star_wars_characters_file_name
        star_wars_file_metadata.created_date = DateField(auto_now_add=True)
        star_wars_file_metadata.save()
