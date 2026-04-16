from django.urls import path
from .views import RegisterView, LoginView, MeView, UpdateMeView, UserDetailView, UserSearchView


urlpatterns = [
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),

    path("me", MeView.as_view()),
    path("me/update", UpdateMeView.as_view()),

    path("<int:id>", UserDetailView.as_view()),
    path("search", UserSearchView.as_view()),
]