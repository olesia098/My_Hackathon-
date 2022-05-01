
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from main.models import BooksDescription, BookContent, Genre, Rating, Comment, Like
from main.permissions import IsBooksAuthor
from main.serializers import BooksDescriptionSerializers, BookContentSerializers, GenreSerializers, RatingSerializers, \
    CommentsSerializers
from rest_framework.mixins import *

User = get_user_model()


class BooksDescriptionViewSet(viewsets.ModelViewSet):
    queryset = BooksDescription.objects.all()
    serializer_class = BooksDescriptionSerializers
    permission_classes = [AllowAny, ]

    def get_seializer_context(self):
        return {'request': self.request}

    @action(detail=False, methods=['get']) # выводит все посты определенного пользователя по сылке own
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializers = BookContentSerializers(queryset, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        serializers = BooksDescriptionSerializers(queryset, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(methods=['Post'], detail=True)
    def rating(self, request, pk):  # http://localhost:8000/product/id_product/rating/
        serializer = RatingSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            obj = Rating.objects.get(title=self.get_object(), author=request.user)
            obj.rating = request.data['rating']
        except Rating.DoesNotExist:
            obj = Rating(author=request.user, title=self.get_object(), rating=request.data['rating'])
        obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsBooksAuthor, ]
        else:
            permissions = [IsAuthenticated, ]

        return [permission() for permission in permissions]

    @action(methods=['POST'], detail=True)
    def like(self, request, *args, **kwargs):
        title = self.get_object()
        like_obj, _ = Like.objects.get_or_create(title=title, author=request.user)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'liked'
        if not like_obj.like:
            status = 'unlike'
        return Response({'status': status})


class BookContentViewSet(viewsets.ModelViewSet):
    queryset = BookContent.objects.all()
    serializer_class = BookContentSerializers
    permission_classes = [IsAuthenticated, ]

    # def get_permissions(self):
    #     if self.action in ['update', 'partial_update', 'destroy']:
    #         permissions = [IsBooksAuthor, ]
    #     else:
    #         permissions = [IsAuthenticated, ]
    #
    #     return [permission() for permission in permissions]


class GenreDeleteUpdateRetriveView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'name'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    permission_classes = [AllowAny, ]


class CommentsListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializers
    permission_classes = [IsAuthenticated, ]


class BookContentListViewDeleteUpdateRetriveView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = BookContent.objects.all()
    serializer_class = BookContentSerializers
    permission_classes = [IsAuthenticated]
