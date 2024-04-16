from starwars_clean.domain.models.model_file import File


class StarWarsFileRepositoryInterface:
    """Interface for starwars file metadata repository."""

    def get_all_files(self) -> list[File]:
        """Get all the saved files metadata."""
        raise NotImplementedError

    def save(self, star_wars_characters_file_name: str) -> None:
        """Save file metadata."""
        raise NotImplementedError
