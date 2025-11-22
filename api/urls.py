from django.urls import path, include
from .views import VacancyListCreateView, VacancyRetrieveUpdateDeleteView, ResumeListCreateView, ResumeRetrieveUpdateDeleteView, ApplicationCreateView, FavoriteVacancyToggleView

urlpatterns = [
    path("vacancies/", VacancyListCreateView.as_view(), name="vacancy-list-create"),
    path("vacancies/<int:pk>/", VacancyRetrieveUpdateDeleteView.as_view(), name="vacancy-detail"),

    path("resumes/", ResumeListCreateView.as_view(), name="resume-list-create"),
    path("resumes/<int:pk>/", ResumeRetrieveUpdateDeleteView.as_view(), name="resume-detail"),

    path("vacancies/<int:vacancy_id>/apply/", ApplicationCreateView.as_view(), name="application-create"),

    path("vacancies/<int:vacancy_id>/favorite/", FavoriteVacancyToggleView.as_view(), name="favorite-toggle"),
]
