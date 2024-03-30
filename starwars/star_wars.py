from datetime import datetime

import petl as etl
from django.conf import settings
from petl.util.base import Table

from starwars.constants import SWAPI_PEOPLE_API_URL
from starwars.repository import StarWarsCharactersFileMetadataRepository
from starwars.utils import fetch_data_from_url


class StarWarsCharacters:
    """Class to have all the functionalities related to star wars characters."""

    # Cache could have been used here to avoid the same
    # data being fetched again and again from the SWAPI API.
    # Excluded it for easier testing.

    def _generate_star_wars_characters_file_name(self) -> str:
        """Generate file name with timestamp."""
        return (
            f"star_wars_characters_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        )

    def _get_homeworld_name(self, homeworld_name_url: str) -> str | None:
        """Get homeworld name from the provided URL"""

        homeworld_info = fetch_data_from_url(fetch_url=homeworld_name_url)

        if homeworld_info:
            return homeworld_info.get("name")

        return None

    def get_star_wars_characters(self) -> list:
        """Return star wars characters data from the SWAPI URL."""
        swapi_api_url_with_next_page = SWAPI_PEOPLE_API_URL
        star_wars_characters = []

        counter = 0  # Added for quick mode (to assist on testing)

        while swapi_api_url_with_next_page:
            # Make a request to SWAPI
            swapi_data = fetch_data_from_url(fetch_url=swapi_api_url_with_next_page)

            # Extract results from the response data
            results = swapi_data.get("results", [])

            star_wars_characters.extend(results)

            swapi_api_url_with_next_page = swapi_data.get("next")

            counter += 1

            if settings.QUICK_MODE and counter >= 2:
                break

        return star_wars_characters

    def transform_star_wars_characters_data(
        self, star_wars_characters: list
    ) -> Table | None:
        """Transform data from swapi api."""

        star_wars_characters_table = etl.fromdicts(star_wars_characters)

        if not star_wars_characters_table:
            return None

        star_wars_characters_table = etl.cutout(
            star_wars_characters_table,
            "url",
            "films",
            "species",
            "vehicles",
            "starships",
            "created",
        )
        star_wars_characters_table = etl.convert(
            star_wars_characters_table,
            "edited",
            lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
                "%Y-%m-%d"
            ),
        )

        transformed_star_wars_characters_table = etl.convert(
            star_wars_characters_table,
            "homeworld",
            lambda v: self._get_homeworld_name(v),
        )

        return transformed_star_wars_characters_table

    def store_star_wars_characters_data_in_csv(self, star_wars_table: Table) -> str:
        """Save provided star wars table to csv file."""

        star_wars_characters_csv_file = self._generate_star_wars_characters_file_name()
        etl.tocsv(star_wars_table, star_wars_characters_csv_file)
        return star_wars_characters_csv_file

    @staticmethod
    def save_star_wars_csv_file_metadata(star_wars_characters_file_name: str) -> None:
        """Save saved filed metadata to database."""

        star_wars_repo = StarWarsCharactersFileMetadataRepository()
        star_wars_repo.save(
            star_wars_characters_file_name=star_wars_characters_file_name
        )
