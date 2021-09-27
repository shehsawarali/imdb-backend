from django.urls import path

from .views import (
    Favorite,
    ListFavorites,
    ListWatchlist,
    PersonDetail,
    PersonSearch,
    TitleDetail,
    TitleReviews,
    TitleSearch,
    UserRating,
    UserReview,
    Watchlist,
)

urlpatterns = [
    path("title/<int:pk>/", TitleDetail.as_view(), name="title"),
    path("person/<int:pk>/", PersonDetail.as_view(), name="person"),
    path("search/title/", TitleSearch.as_view(), name="search-title"),
    path("search/person/", PersonSearch.as_view(), name="search-person"),
    path("favorite/", Favorite.as_view(), name="favorite"),
    path("watchlist/", Watchlist.as_view(), name="watchlist"),
    path("get-watchlist/", ListWatchlist.as_view(), name="list-watchlist"),
    path("get-favorites/", ListFavorites.as_view(), name="list-favorites"),
    path("rate/", UserRating.as_view(), name="rate-title"),
    path("review/", UserReview.as_view(), name="review-title"),
    path("reviews/<int:pk>/", TitleReviews.as_view(), name="title-reviews"),
]
