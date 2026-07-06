# Архитектура проекта MoviesReviews

## Схема базы данных (ER-диаграмма)

Сущности и связи:

- **User** (встроенная модель Django)
  - поля: id, username, email, password, first_name, last_name, ...
- **Profile**
  - поля: id, user (OneToOne → User), bio, avatar
- **Movie**
  - поля: id, title, description, release_year, poster, added_by (ForeignKey → User, null), created_at
- **Review**
  - поля: id, movie (ForeignKey → Movie), user (ForeignKey → User), text, rating (1-5), created_at, updated_at
  - ограничение: unique_together(movie, user)

Связи:
- User 1 — 1 Profile
- Movie 1 — * Review
- User 1 — * Review
- Movie * — 1 User (added_by)

## Диаграмма классов представлений

- `MovieListView` (ListView) — главная страница
- `MovieDetailView` (DetailView) — детальная страница фильма
- `MovieCreateView` (LoginRequiredMixin, CreateView) — добавление фильма
- `ReviewCreateView` (LoginRequiredMixin, CreateView) — создание отзыва
- `ReviewUpdateView` (LoginRequiredMixin, UserPassesTestMixin, UpdateView) — редактирование
- `ReviewDeleteView` (LoginRequiredMixin, UserPassesTestMixin, DeleteView) — удаление
- `RegisterView` (CreateView) — регистрация
- `ProfileView` (LoginRequiredMixin, TemplateView) — профиль
- `MyReviewsView` (LoginRequiredMixin, TemplateView) — список отзывов пользователя
- `ProfileEditView` (LoginRequiredMixin, UpdateView) — редактирование профиля
- `CustomPasswordChangeView` (LoginRequiredMixin, PasswordChangeView) — смена пароля