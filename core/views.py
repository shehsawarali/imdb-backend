from django.db.models import Avg, Count, F
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Person, Title
from .serializers import (
    BasicPersonSerializer,
    BasicTitleSerializer,
    PersonSerializer,
    TitleSerializer,
)


class TitleDetail(RetrieveAPIView):
    """
    View for retrieving Title instances. Requires the Title id in url
    params, and appends the average rating and rating count to the instance.
    """

    queryset = (
        Title.objects.all()
        .prefetch_related("genres", "type")
        .annotate(
            rating=Avg(F("ratings__rating")), rating_count=Count(F("ratings"))
        )
    )
    serializer_class = TitleSerializer


class PersonDetail(RetrieveAPIView):
    """
    View for retrieving Person instances. Requires the Person id in url params.
    """

    queryset = Person.objects.all().prefetch_related(
        "professions", "known_for_titles", "principals"
    )
    serializer_class = PersonSerializer


class TitleSearch(ListAPIView):
    """
    View for retrieving a paginated list of filtered/sorted Titles. Requires
    the particular filters in query params. If a query is not passed,
    the view will return a paginated list of all Title instances.

    The `sort` param must be a string which can be passed exactly to the
    queryset e.g. `rating` or `-rating`
    """

    serializer_class = BasicTitleSerializer

    def get_queryset(self):
        """
        Function to build a queryset according to the query params.
        """
        query_params = self.request.query_params
        sort = query_params.get("sort")
        name = query_params.get("name")
        genres = query_params.getlist("genre")
        min_rating = query_params.get("min_rating")
        max_rating = query_params.get("max_rating")

        queryset = Title.objects.all().annotate(
            rating=Avg(F("ratings__rating"))
        )

        if sort:
            queryset = queryset.order_by(sort, "start_year")
        else:
            queryset = queryset.order_by("-rating", "start_year")

        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        if genres:
            queryset = queryset.filter(genres__name__in=genres)
        if min_rating is not None:
            queryset = queryset.filter(rating__gte=-1)
        if max_rating is not None:
            queryset = queryset.filter(rating__lte=max_rating)

        return queryset


class PersonSearch(ListAPIView):
    """
    View for retrieving a paginated list of filtered Person objects. The
    search query must be passed in the query params with the `search` key.
    If a query is not passed, the view will return a paginated list of all
    Person instances.

    The resultant queryset is always sorted by `name`.
    """

    queryset = Person.objects.all().order_by("name", "id")

    serializer_class = BasicPersonSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]
