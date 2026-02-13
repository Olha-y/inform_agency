from django.urls import path


from tracking_system.views import (
    index,
    RedactorListView,
    TopicListView,
    NewspaperListView,
    RedactorDetailView,
    NewspaperDetailView,
    TopicWithNewspapersDetailView,
    RedactorCreateView,
    RedactorExperienceUpdateView,
    NewspaperCreateView,
    NewspaperUpdateView,
    NewspaperDeleteView,
    RedactorRemoveFromNewspaperView,
    RedactorAssignToNewspaperView,
    about_us,contact_us
)

urlpatterns = [
    path("", index, name="index"),
    path("about-us/", about_us, name="about-us"),
    path("contact-us/", contact_us, name="contact-us"),
    path(
        "redactors/",
        RedactorListView.as_view(),
        name="redactor-list"
    ),
    path(
        "redactors/create/",
        RedactorCreateView.as_view(),
        name="redactor-create"
    ),
    path(
        "redactors/<int:pk>/",
        RedactorDetailView.as_view(),
        name="redactor-detail"
    ),
    path(
        "redactors/<int:pk>/update/",
        RedactorExperienceUpdateView.as_view(),
        name="redactor-update-experience"
    ),
    path(
        "topics/",
        TopicListView.as_view(),
        name="topic-list"
    ),
    path(
        "topics/<int:pk>/",
        TopicWithNewspapersDetailView.as_view(),
        name="topic-detail"
    ),
    path(
        "newspapers/",
        NewspaperListView.as_view(),
        name="newspaper-list"
    ),
    path(
        "newspapers/create/",
        NewspaperCreateView.as_view(),
        name="newspaper-create"
    ),
    path(
        "newspapers/<int:pk>/",
        NewspaperDetailView.as_view(),
        name="newspaper-detail"
    ),
    path(
        "newspapers/<int:pk>/update/",
        NewspaperUpdateView.as_view(),
        name="newspaper-update"
    ),
    path(
        "newspapers/<int:pk>/delete/",
        NewspaperDeleteView.as_view(),
        name="newspaper-delete"
    ),
    path(
        "newspapers/<int:pk>/remove-redactor/",
        RedactorRemoveFromNewspaperView.as_view(),
        name="redactor-remove"
    ),
    path(
        "newspapers/<int:pk>/assign-redactor/",
        RedactorAssignToNewspaperView.as_view(),
        name="redactor-assign"
    ),
]

app_name = "tracking_system"
