from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic, View

from tracking_system.forms import (
    RedactorCreateForm,
    RedactorExperienceUpdateForm,
    NewspaperForm,
    NewspaperUpdateForm,
    NewspaperSearchForm,
    RedactorSearchForm
)
from tracking_system.models import Redactor, Topic, Newspaper


User = get_user_model()


@login_required
def index(request: HttpRequest):
    today = timezone.now()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    newspapers_today = Newspaper.objects.filter(
        published_date__date=today.date()
    ).count()

    newspapers_week = Newspaper.objects.filter(
        published_date__gte=week_ago
    ).count()

    newspapers_month = Newspaper.objects.filter(
        published_date__gte=month_ago
    ).count()

    active_redactors = Redactor.objects.filter(
        newspapers__published_date__gte=week_ago
    ).distinct()
    inactive_redactors = Redactor.objects.exclude(
        newspapers__published_date__gte=week_ago
    ).distinct()


    latest_newspapers = (
        Newspaper.objects
        .select_related("topic")
        .prefetch_related("publishers")
        .order_by("-published_date")[:3]
    )
    num_topics = Topic.objects.count()
    num_newspapers = Newspaper.objects.count()
    num_redactors = Redactor.objects.count()

    context = {
        "newspapers_today": newspapers_today,
        "newspapers_week": newspapers_week,
        "newspapers_month": newspapers_month,
        "active_redactors": active_redactors,
        "inactive_redactors": inactive_redactors,
        "latest_newspapers": latest_newspapers,
        "num_topics": num_topics,
        "num_newspapers": num_newspapers,
        "num_redactors": num_redactors,
    }

    return render(
        request,
        "tracking_system/index.html",
        context
    )


def about_us(request: HttpRequest):
    return render(
        request,
        "tracking_system/about_us.html"
    )


def contact_us(request: HttpRequest):
    return render(
        request,
        "tracking_system/contact_us.html"
    )


class TopicListView(
    LoginRequiredMixin,
    generic.ListView
):
    model = Topic
    context_object_name = "topics"

    def get_queryset(self):
        return (
            Topic.objects
            .annotate(publications_count=Count("newspapers"))
        )


class TopicWithNewspapersDetailView(
    LoginRequiredMixin,
    generic.DetailView
):
    model = Topic
    context_object_name = "topic"

    def get_queryset(self):
        return Topic.objects.prefetch_related("newspapers__publishers")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    context_object_name = "redactors"
    template_name = "tracking_system/redactor_list.html"
    paginate_by = 4

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username")
        context["search_form"] = RedactorSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Redactor.objects.annotate(
            publications_count=Count("newspapers", distinct=True)
        )
        search_form = RedactorSearchForm(self.request.GET)

        if search_form.is_valid():
            username = search_form.cleaned_data.get("username")
            if username:
                queryset = queryset.filter(username__icontains=username)
        return queryset


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_newspapers"] = (
            self.object.newspapers
            .select_related("topic")
            .prefetch_related("publishers")
            .order_by("-published_date")
        )
        return context


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreateForm
    success_url = reverse_lazy("tracking_system:redactor-list")


class RedactorExperienceUpdateView(
    LoginRequiredMixin,
    generic.UpdateView
):
    model = User
    form_class = RedactorExperienceUpdateForm
    template_name = "tracking_system/redactor_update_experience.html"

    def get_success_url(self):
        return reverse_lazy(
            "tracking_system:redactor-detail",
            kwargs={"pk": self.object.pk}
        )


class RedactorAssignToNewspaperView(LoginRequiredMixin, View):
    def get(self, request, pk):
        newspaper = get_object_or_404(Newspaper, pk=pk)
        newspaper.publishers.add(request.user)
        return redirect(
            "tracking_system:newspaper-detail",
            pk=newspaper.pk
        )


class RedactorRemoveFromNewspaperView(LoginRequiredMixin, View):
    def get(self, request, pk):
        newspaper = get_object_or_404(Newspaper, pk=pk)
        newspaper.publishers.remove(request.user)
        return redirect(
            "tracking_system:newspaper-detail",
            pk=newspaper.pk
        )


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    context_object_name = "newspapers"
    paginate_by = 5
    queryset = (Newspaper.objects
                .select_related("topic")
                .prefetch_related("publishers")
                )

    def get_queryset(self):
        queryset = self.queryset
        now = timezone.now()

        period = self.request.GET.get("period")

        if period == "today":
            queryset = queryset.filter(published_date__date=now.date())

        elif period == "week":
            queryset = queryset.filter(
                published_date__gte=now - timedelta(days=7)
            )

        elif period == "month":
            queryset = queryset.filter(
                published_date__gte=now - timedelta(days=30)
            )

        form = NewspaperSearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data.get("title"):
            queryset = queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = NewspaperSearchForm(
            initial={
                "title": self.request.GET.get("title", "")
            }
        )
        context["current_period"] = self.request.GET.get("period", "all")
        return context


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("tracking_system:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperUpdateForm
    template_name = "tracking_system/newspaper_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "tracking_system:newspaper-detail",
            kwargs={"pk": self.object.pk}
        )


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("tracking_system:newspaper-list")
