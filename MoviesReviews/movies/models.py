from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    release_year = models.PositiveIntegerField(verbose_name="Год выпуска")
    poster = models.ImageField(upload_to='posters/', blank=True, null=True, verbose_name="Постер")
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='added_movies')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'pk': self.pk})


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Оценка")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['movie', 'user']  # один отзыв от пользователя на фильм
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв {self.user.username} на {self.movie.title}"
