from django.contrib import admin

from api.models import Category, Comment, Genre, Review, Title, User


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category', 'description')
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'reviews', 'pub_date')
    search_fields = ('author',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text', 'title', 'score', 'pub_date')
    search_fields = ('author',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'first_name', 'last_name', 'email', 'role',
        'is_staff')
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(Review, ReviewsAdmin)
admin.site.register(User, UserAdmin)
