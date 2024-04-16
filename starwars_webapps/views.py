import requests
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import permissions, status


from starwars_clean.api.resources.v1.api_starwars import StarWarsApi


class ExampleStarWarsCharactersFilesView(APIView):
    """
    Example endpoint to get star wars files details. This demonstrates that
    with clean architecture, the client(django in this case), can customize the
    output based on it needs without any change to underlying codes.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        "To return file lists."
        star_wars_characters_files = StarWarsApi().get_starwars_characters_files()
        starwars_characters_files_name: list[str] = [
            file.name for file in star_wars_characters_files
        ]

        return JsonResponse({"files_name": starwars_characters_files_name})


class StarWarsCharactersFilesView(APIView):
    """Endpoint to get star wars files details."""

    permission_classes = (permissions.AllowAny,)

    def get(self, request) -> HttpResponse:
        """To display file list page."""

        star_wars_characters_files = StarWarsApi().get_starwars_characters_files()
        starwars_characters_files_name: list[str] = [
            file.name for file in star_wars_characters_files
        ]

        paginator = Paginator(
            starwars_characters_files_name, 10
        )  # Show 10 files per page
        page_number = request.GET.get("page")
        star_wars_characters_page = paginator.get_page(page_number)

        return render(
            request,
            "file_list.html",
            {"star_wars_characters_file_page": star_wars_characters_page},
        )


class StarWarsCharactersExtractionView(APIView):
    """Endpoint to get star wars characters."""

    permission_classes = (permissions.AllowAny,)

    def get(self, request) -> HttpResponseRedirect | Response:
        """Get star wars character and store it in a csv."""
        try:
            StarWarsApi().get_and_save_starwars_characters()
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

