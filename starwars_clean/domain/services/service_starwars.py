from dependency_injector.wiring import inject

from starwars_clean.domain.ports.file_repository_starwars import (
    StarWarsFileRepositoryInterface,
)
from starwars_clean.domain.ports.service_starwars import StarWarsServiceInterface
from starwars_clean.domain.ports.helper_starwars import SwapiHelperInterface
from starwars_clean.domain.models.model_file import File


class StarWarsService(StarWarsServiceInterface):

    columns_to_remove = [
        "url",
        "films",
        "species",
        "vehicles",
        "starships",
        "created",
    ]

    @inject
    def __init__(
        self,
        starwars_file_repository: StarWarsFileRepositoryInterface,
        starwars_helper: SwapiHelperInterface,
    ) -> None:
        self.starwars_file_repository = starwars_file_repository
        self.starwars_helper = starwars_helper

    def get_starwars_characters_files(self) -> list[File]:
        """Get all the saved starwars files metadata."""
        return self.starwars_file_repository.get_all_files()

    def get_and_save_starwars_characters(self) -> None:
        """Get and save starwars characters to a file."""
        star_wars_characters = self.starwars_helper.get_star_wars_characters()

        if not star_wars_characters:
            raise Exception("No data found from SWAPI")

        transformed_star_wars_table = (
            self.starwars_helper.transform_star_wars_characters_data(
                star_wars_characters=star_wars_characters,
                columns_to_remove=self.columns_to_remove,
            )
        )

        star_wars_csv_file_name = (
            self.starwars_helper.store_star_wars_characters_data_in_csv(
                transformed_star_wars_table
            )
        )

        return self.starwars_file_repository.save(
            star_wars_characters_file_name=star_wars_csv_file_name
        )
