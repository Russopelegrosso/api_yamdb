from django.core.exceptions import ValidationError
from django.db.models import Avg
from rest_framework import serializers

from api.models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField('get_rating')
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    def get_rating(self, obj):
        rating = Review.objects.filter(title_id=obj.pk).aggregate(
            rating=Avg('score')).get('rating')
        reviews_exists = Review.objects.exists()
        return None if not reviews_exists else rating

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field='username')
    title = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field='pk')

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        request = self.context.get('request')
        if request.method != 'POST':
            return data

        title_id = self.context.get('view').kwargs.get('title_id')
        user = self.context.get('request').user
        queryset = Review.objects.filter(author=user, title=title_id)
        if queryset.exists():
            raise serializers.ValidationError('Not Allowed')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field='username')

    reviews = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field='pk')

    class Meta:
        fields = '__all__'
        model = Comment


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'role', 'email', 'first_name', 'last_name',
            'bio')
