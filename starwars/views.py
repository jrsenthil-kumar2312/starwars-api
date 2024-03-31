import logging

import petl as etl
import requests
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from petl.util.base import Table
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from starwars.repository import StarWarsCharactersFileMetadataRepository
from starwars.star_wars import StarWarsCharacters

logger = logging.getLogger(__name__)

############################## Improvement notes #############################
## 1. Permission to API should be restricted instead of allowing it to be accessed by anyone
## 2. These APIs do not have any authentication, a simple JWT implementation will be good to add.
## 3. I have not used any clean architecture concept here apart from the repository layer. It will
##    be good to have views -> service -> repository flow as this will create a clear separation.
## 4. Additionally, Pydantic model should be used as data transfer model between the layers stated above.
##    This will allow the layers to work together even if the underlying technology changes.
## 5. Another approach I usually take is to code out of the framework (django).This reduces dependencies.
##    I did not do it here in order to keep it simple.
#################################### Thank You ###############################


class StarWarsCharactersFileListView(APIView):
    """Endpoint to get star wars files details."""

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        """Get request for retrieving star wars characters files name."""

        star_wars_repository = StarWarsCharactersFileMetadataRepository()
        star_wars_characters_files_name = star_wars_repository.retrieve_all_files_name()
        paginator = Paginator(
            star_wars_characters_files_name, 10
        )  # Show 10 files per page
        page_number = request.GET.get("page")
        star_wars_characters_page = paginator.get_page(page_number)

        return render(
            request,
            "file_list.html",
            {"star_wars_characters_file_page": star_wars_characters_page},
        )


class StarWarsCharactersFileDuplicateRowCount(APIView):
    """Endpoint to handle duplicate data in star wars characters."""

    permission_classes = (permissions.AllowAny,)

    def _generate_star_wars_characters_duplicate_table(
        self, star_wars_characters_table: Table, selected_columns: list
    ) -> Table:
        """Return a table with star wars characters duplicate information."""

        # Identify duplicate rows based on selected columns
        duplicate_rows = etl.duplicates(
            star_wars_characters_table, key=selected_columns
        )
        # Count the number of duplicates for each duplicate row group
        grouped_duplicates_table = etl.aggregate(
            duplicate_rows, key=selected_columns, aggregation=len
        )

        renamed_grouped_duplicates_table = etl.rename(
            grouped_duplicates_table, {"value": "Count"}
        )

        # Construct a new table containing duplicate rows along with the count of duplicates
        star_wars_characters_duplicate_table = etl.leftjoin(
            star_wars_characters_table,
            renamed_grouped_duplicates_table,
            selected_columns,
            missing=1,
        )

        star_wars_characters_duplicate_table_selected = etl.cut(
            star_wars_characters_duplicate_table, *selected_columns, "Count"
        )

        return etl.distinct(star_wars_characters_duplicate_table_selected)

    def post(self, request) -> JsonResponse:
        """Post request to analyse and return duplicate rows data."""

        request_body = request.data
        star_wars_characters_file_name = request_body.get("file_name")
        selected_column_names = list(request_body.getlist("selected_columns"))

        if not star_wars_characters_file_name:
            return JsonResponse(
                {"status": "false", "message": "Missing file name"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        star_wars_characters_table = etl.fromcsv(star_wars_characters_file_name)

        if not selected_column_names:
            # Return the whole table if selected column field is empty.
            return JsonResponse(list(etl.dicts(star_wars_characters_table)), safe=False)

        star_wars_characters_duplicate_table_distinct = (
            self._generate_star_wars_characters_duplicate_table(
                star_wars_characters_table=star_wars_characters_table,
                selected_columns=selected_column_names,
            )
        )

        star_wars_characters_table = etl.dicts(
            star_wars_characters_duplicate_table_distinct
        )

        return JsonResponse(list(star_wars_characters_table), safe=False)


class StarWarsCharactersFileDetailView(APIView):
    """Endpoint to get star wars characters file details."""

    permission_classes = (permissions.AllowAny,)

    def get(self, request, star_wars_characters_file_name: str) -> HttpResponse:
        """Return content of the specified file."""
        try:
            star_wars_characters_data = None
            star_wars_characters_full_data = []
            star_wars_characters_data_by_page = None
            star_wars_characters_table = etl.fromcsv(star_wars_characters_file_name)
            star_wars_characters_data = list(star_wars_characters_table)

            # Show 10 rows per page
            paginator = Paginator(star_wars_characters_data, 10)
            page_number = request.GET.get("page", 1)

            for page_num in range(1, int(page_number) + 1):
                star_wars_characters_data_by_page = paginator.get_page(page_num)
                star_wars_characters_full_data.extend(
                    list(star_wars_characters_data_by_page)
                )

        except FileNotFoundError:
            pass

        return render(
            request,
            "file_details.html",
            {
                "star_wars_characters_full_data": star_wars_characters_full_data,
                "star_wars_characters_data_by_page": star_wars_characters_data_by_page,
                "star_wars_characters_file_name": star_wars_characters_file_name,
            },
        )


class StarWarsCharactersExtractionView(APIView):
    """Endpoint to get star wars characters."""

    permission_classes = (permissions.AllowAny,)

    columns_to_remove = ["url", "films", "species", "vehicles", "starships", "created",]

    def get(self, request) -> HttpResponseRedirect | Response:
        """Get star wars character and store it in a csv."""
        try:
            star_wars_characters_handler = StarWarsCharacters()
            star_wars_characters = (
                star_wars_characters_handler.get_star_wars_characters()
            )

            if not star_wars_characters:
                return Response(
                    {"message": "No data found from SWAPI"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            transformed_star_wars_table = (
                star_wars_characters_handler.transform_star_wars_characters_data(
                    star_wars_characters=star_wars_characters, columns_to_remove=self.columns_to_remove
                )
            )

            star_wars_csv_file_name = (
                star_wars_characters_handler.store_star_wars_characters_data_in_csv(
                    transformed_star_wars_table
                )
            )

            star_wars_characters_handler.save_star_wars_csv_file_metadata(
                star_wars_characters_file_name=star_wars_csv_file_name
            )

            return HttpResponseRedirect(reverse("file_list"))

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Failed to fetch data from SWAPI: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except (KeyError, IndexError) as e:
            return Response(
                {"error": f"Invalid data received from SWAPI: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
