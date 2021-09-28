from django.urls import path

from .views import PersonDetail, PersonSearch, TitleDetail, TitleSearch

urlpatterns = [
    path("title/<int:pk>/", TitleDetail.as_view(), name="title"),
    path("person/<int:pk>/", PersonDetail.as_view(), name="person"),
    path("search/title/", TitleSearch.as_view(), name="search-title"),
    path("search/person/", PersonSearch.as_view(), name="search-person"),
]
