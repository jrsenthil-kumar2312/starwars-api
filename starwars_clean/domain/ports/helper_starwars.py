from petl.util.base import Table

class SwapiHelperInterface:
    """Class to have all the functionalities related to star wars characters."""

    # Cache could have been used here to avoid the same
    # data being fetched again and again from the SWAPI API.
    # Excluded it for easier testing.

    def get_star_wars_characters(self) -> list:
        """Return star wars characters data from the SWAPI URL."""
        raise NotImplementedError

    def transform_star_wars_characters_data(
        self, star_wars_characters: list, columns_to_remove: list | None = None
    ) -> Table | None:
        """Transform data from swapi api."""

        raise NotImplementedError

    def store_star_wars_characters_data_in_csv(self, star_wars_table: Table) -> str:
        """Save provided star wars table to csv file."""

        raise NotImplementedError

    @staticmethod
    def save_star_wars_csv_file_metadata(star_wars_characters_file_name: str) -> None:
        """Save saved filed metadata to database."""

        raise NotImplementedError
