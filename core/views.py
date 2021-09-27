from django.core.exceptions import ValidationError
from django.db.models import Avg, Count, F, Q
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils import MISSING_REQUIRED_FIELDS, response_http

from .models import Person, Rating, Review, Title
from .serializers import (
    BasicPersonSerializer,
    BasicTitleSerializer,
    PersonSerializer,
    ReviewSerializer,
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
        min_year = query_params.get("min_year")
        max_year = query_params.get("max_year")

        queryset = Title.objects.all().annotate(
            rating=Avg(F("ratings__rating"))
        )

        if sort:
            queryset = queryset.order_by(sort, "start_year")
        else:
            queryset = queryset.order_by("-rating", "start_year")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if genres:
            queryset = queryset.filter(genres__name__in=genres)
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        if max_rating:
            queryset = queryset.filter(rating__lte=max_rating)
        if min_year:
            queryset = queryset.filter(start_year__gte=min_year)
        if max_year:
            queryset = queryset.filter(start_year__lte=max_year)

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


class Watchlist(APIView):
    """
    View for adding/removing Titles from the user's watchlist
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Method for retrieving watchlist status of a Title. Return variable
        is True if the title is in the user's watchlist, and false otherwise.
        """

        try:
            query_params = self.request.query_params
            title_id = query_params.get("id")

            watchlist = request.user.watchlist
            return Response(
                {"is_watchlisted": watchlist.filter(id=title_id).exists()}
            )
        except (KeyError, ValueError):
            return response_http(
                MISSING_REQUIRED_FIELDS, status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        """
        Method for adding a Title to the user's watchlist.
        """

        try:
            title_id = request.data.get("id")
            request.user.watchlist.add(title_id)
            return response_http("Added to Watchlist", status.HTTP_200_OK)
        except KeyError:
            return response_http(
                MISSING_REQUIRED_FIELDS, status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        """
        Method for removing a Title from the user's watchlist.
        """

        try:
            query_params = self.request.query_params
            title_id = query_params.get("id")
            request.user.watchlist.remove(title_id)
            return response_http("Removed from watchlist", status.HTTP_200_OK)
        except KeyError:
            return response_http(
                MISSING_REQUIRED_FIELDS, status.HTTP_400_BAD_REQUEST
            )


class Favorite(APIView):
    """
    View for adding/removing Titles from the user's favorites.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Method for retrieving favorite status of a Title. Return variable
        is True if the title is in the user's favorites, and false otherwise.
        """

        try:
            query_params = self.request.query_params
            title_id = query_params.get("id")

            favorites = request.user.favorites
            return Response(
                {"is_favorite": favorites.filter(id=title_id).exists()}
            )
        except (KeyError, ValueError):
            return response_http(
                MISSING_REQUIRED_FIELDS, status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        """
        Method for adding a Title to the user's favourites.
        """

        try:
            title_id = request.data.get("id")
            request.user.favorites.add(title_id)
            return response_http("Added to favorites", status.HTTP_200_OK)
        except KeyError:
            return response_http(
                MISSING_REQUIRED_FIELDS, status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        """
        Method for removing a Title from the user's watchlist.
        """

        try:
            query_params = self.request.query_params
            title_id = query_params.get("id")
            request.user.favorites.remove(title_id)
            return response_http("Removed from favorites", status.HTTP_200_OK)
        except KeyError:
            return response_http(
                MISSING_REQUIRED_FIELDS, status.HTTP_400_BAD_REQUEST
            )


class ListWatchlist(ListAPIView):
    """
    View for retrieving the user's watchlist.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = BasicTitleSerializer

    def get_queryset(self):
        queryset = self.request.user.watchlist.all().annotate(
            rating=Avg(F("ratings__rating"))
        )

        return queryset


class ListFavorites(ListAPIView):
    """
    View for retrieving the user's favorites.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = BasicTitleSerializer

    def get_queryset(self):
        queryset = self.request.user.favorites.all().annotate(
            rating=Avg(F("ratings__rating"))
        )

        return queryset


class UserRating(APIView):
    """
    View for retrieving, creating or updating a Rating instance.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Method to retrieve the user's rating for a specific title. Returns
        0 if the user has not rated the title.
        """

        try:
            title_id = self.request.query_params.get("id")
        except KeyError:
            return response_http(
                MISSING_REQUIRED_FIELDS, status.HTTP_400_BAD_REQUEST
            )

        rating = request.user.ratings.filter(title=title_id)
        if rating.exists():
            return Response({"rating": rating.first().rating})
        else:
            return Response({"rating": 0})

    def post(self, request):
        """
        Method for creating or updating a Rating instance. If the user has
        already rated a title, then the same Rating instance will be updated
        instead of creating a new instance.
        """

        try:
            title_id = request.data.get("id")
            rating = request.data.get("rating")
        except KeyError:
            return Response(status.HTTP_400_BAD_REQUEST)

        rating_instance = Rating.objects.filter(
            title=title_id, user=request.user.id
        )

        if rating_instance.exists():
            rating_instance = rating_instance.first()
            rating_instance.rating = rating
        else:
            rating_instance = Rating(
                title_id=title_id, user=request.user, rating=rating
            )

        try:
            rating_instance.full_clean()
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        rating_instance.save()
        return response_http("Rating has been saved", status.HTTP_200_OK)


class UserReview(APIView):
    """
    View for retrieving, creating or updating a Review instance.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Method to retrieve the user's review for a specific title. Returns
        `None` if the user has not reviews the title.
        """

        try:
            title_id = self.request.query_params.get("id")
        except KeyError:
            return response_http(
                MISSING_REQUIRED_FIELDS, status.HTTP_400_BAD_REQUEST
            )

        review = request.user.reviews.filter(title=title_id)
        if review.exists():
            return Response({"review": review.first().review})
        else:
            return Response({"review": None})

    def post(self, request):
        """
        Method for creating or updating a Review instance. If the user has
        already reviewed a title, then the same Review instance will be updated
        instead of creating a new instance.
        """

        title_id = request.data.get("id")
        review = request.data.get("review")

        if title_id is None or review is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        review_instance = Review.objects.filter(
            title=title_id, user=request.user.id
        )

        if review_instance.exists():
            review_instance = review_instance.first()
            review_instance.review = review
        else:
            review_instance = Review(
                title_id=title_id, user=request.user, review=review
            )

        review_instance.save()
        return response_http("Review has been saved", status.HTTP_200_OK)


class TitleReviews(ListAPIView):
    """
    View for retrieving Reviews belonging to a specific Title.
    """

    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs["pk"]
        queryset = Review.objects.filter(title=title_id).prefetch_related(
            "title", "user"
        )

        return queryset
