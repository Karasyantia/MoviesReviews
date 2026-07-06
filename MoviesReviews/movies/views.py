from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from .models import Movie, Review
from .forms import MovieForm, ReviewForm


class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 12


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.select_related('user').all()
        if self.request.user.is_authenticated:
            user_review = self.object.reviews.filter(user=self.request.user).first()
            context['user_review'] = user_review
        return context


class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/movie_add.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'movies/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.movie = get_object_or_404(Movie, pk=self.kwargs['movie_pk'])
        existing = Review.objects.filter(movie=self.movie, user=request.user).first()
        if existing:
            return redirect('review_edit', pk=existing.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = self.movie  # передаём фильм
        return context

    def form_valid(self, form):
        form.instance.movie = self.movie
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.movie.pk})


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'movies/review_form.html'

    def test_func(self):
        review = self.get_object()
        return review.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = self.object.movie  # для редактирования
        return context

    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.object.movie.pk})


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'movies/review_confirm_delete.html'

    def test_func(self):
        review = self.get_object()
        return review.user == self.request.user

    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.object.movie.pk})