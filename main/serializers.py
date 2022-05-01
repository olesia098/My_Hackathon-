from rest_framework import serializers
from main.models import *


class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class BooksDescriptionSerializers(serializers.ModelSerializer):

    class Meta:
        model = BooksDescription
        fields = ('id', 'title', 'description', 'image', 'author', 'genre', 'speaker', 'rating', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['genre'] = instance.genre.name
        representation['speaker'] = instance.speaker.name
        representation['like'] = instance.like.filter(like=True).count()
        # ВОТ С ЭТИМ ПРОБЛЕМА
        representation['comments'] = CommentsSerializers(instance.comment).data
        rating_result = 0
        for i in instance.rating.all():
            rating_result += int(i.rating)
        if instance.rating.all().count() == 0:
            representation['rating'] = rating_result
        else:
            representation['rating'] = rating_result / instance.rating.all().count()

        return representation

    # ПРОБЛЕМА С ЭТИМ
    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     user_id = request.user.id
    #     validated_data['author_id '] = user_id
    #     post = BooksDescription.objects.create(**validated_data)
    #     return post


class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class SpeakerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'


class BookContentSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookContent
        fields = '__all__'


class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
