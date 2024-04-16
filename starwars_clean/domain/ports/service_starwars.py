from typing import Optional

from starwars_clean.domain.ports.file_repository_starwars import (
    StarWarsFileRepositoryInterface,
)
from starwars_clean.domain.models.model_file import File


class StarWarsServiceInterface:
    """Interface for starwars service layer."""

    def __init__(
        self, starwars_file_repository: StarWarsFileRepositoryInterface
    ) -> None:
        """Starwars service initialization."""
        raise NotImplementedError

    def get_starwars_characters_files(self) -> Optional[list[File]]:
        """Get all the starwars character files name."""
        raise NotImplementedError

    def get_and_save_starwars_characters(self) -> None:
        """Get starwars characters from API and save it."""
        raise NotImplementedError
