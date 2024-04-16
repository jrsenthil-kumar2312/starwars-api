from dependency_injector import containers, providers
from starwars_clean.adapter.repository.repository_starwars import (
    StarWarsCharactersFileMetadataRepository,
)
from starwars_clean.domain.services.service_starwars import StarWarsService
from starwars_clean.adapter.swapi.swapi import SwapiHelper


class StarWarsContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "starwars_clean.domain.services.service_starwars",
            "starwars_clean.api.resources.v1.api_starwars",
        ]
    )

    starwars_file_repository = providers.Factory(
        StarWarsCharactersFileMetadataRepository,
    )

    starwars_helper = providers.Factory(SwapiHelper)

    starwars_service = providers.Factory(
        StarWarsService,
        starwars_file_repository=starwars_file_repository,
        starwars_helper=starwars_helper
    )
