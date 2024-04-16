import logging
from dependency_injector.wiring import inject, Provide

from starwars_clean.containers import StarWarsContainer
from starwars_clean.domain.ports.service_starwars import StarWarsServiceInterface
from starwars_clean.domain.models.model_file import File

logger = logging.getLogger(__name__)


class StarWarsApi:
    @inject
    def __init__(
        self,
        starwars_service: StarWarsServiceInterface = Provide[
            StarWarsContainer.starwars_service
        ],
    ) -> None:
        """Starwars api initialization."""
        self.starwars_service = starwars_service

    def get_starwars_characters_files(self) -> list[File]:
        """Get request for retrieving star wars characters files name."""

        return self.starwars_service.get_starwars_characters_files()

    def get_and_save_starwars_characters(self) -> None:
        """Get starwars characters from external API and save it."""

        return self.starwars_service.get_and_save_starwars_characters()
