from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, GenericAPIView,ListAPIView,ListCreateAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.generics import RetrieveUpdateDestroyAPIView,RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import (ListModelMixin, DestroyModelMixin)

from api.filters import FurnitureFilter
from api.mixins import UltraGenericAPIView
from .paginations import SimplePagintion
from .permissions import IsOwnerOrReadOnly
from furniture.models import Category, Furniture, Review
from .serializers import CategorySerializer, DetailFurnitureSerializer, FurnitureSerializer, ListFurnitureSerializer, ReviewSerializer
from .clone import clone_furniture
from api.auth.permissions import IsSuperUser

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = SimplePagintion
    permission_classes = [IsAuthenticatedOrReadOnly]

class FurnitureListView(ListAPIView):
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer
    pagination_class = SimplePagintion
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_classes = {
        'get': ListFurnitureSerializer,
        'post': FurnitureSerializer,
    }
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    search_fields = ['name', 'description',]
    ordering = ['-price','price']
    filterset_class = FurnitureFilter
    # def get_serializer_class(self):
        
    #     assert self.serializer_classes is not None, (
    #             "'%s' should either include a `serializer_classes` attribute, "
    #             "or override the `get_serializer_class()` method."
    #             % self.__class__.__name__
    #     )

    #     method = self.request.method.lower()
    #     return self.serializer_classes[method]

    # def get_read_serializer(self, *args, **kwargs):
    #     assert self.serializer_classes.get('get') is not None, (
    #             "'%s' should either include a serializer class for get method,"
    #             "if want to use read serializer, please set serializer class for get method"
    #             "or override the `get_serializer_class()` method."
    #             % self.__class__.__name__
    #     )
    #     serializer = self.serializer_classes.get('get')

    #     kwargs.setdefault('context', self.get_serializer_context())
    #     return serializer(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        furniture = self.filter_queryset(self.get_queryset())
        furniture = self.paginate_queryset(furniture)

        # clone_furniture(5)

        serializer = self.get_serializer(furniture, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save(user=request.user)
        read_serializer = self.get_read_serializer(product)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

class FurnitureDetailView(ListModelMixin, DestroyModelMixin, UltraGenericAPIView):
    queryset = Furniture.objects.all()
    serializer_classes = {
        'get': ListFurnitureSerializer,
        'patch': FurnitureSerializer,
        'delete': DetailFurnitureSerializer,  
    }
    permission_classes = [IsAuthenticatedOrReadOnly | IsSuperUser]

    def get(self, request, *args, **kwargs):
        bike = self.get_object()  
        serializer = self.get_serializer(Furniture)  
        return Response(serializer.data) 

    def get_object(self):
        return get_object_or_404(Furniture, id=self.kwargs.get('id'))

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return FurnitureSerializer
        return super().get_serializer_class()

    def patch(self, request, *args, **kwargs):
        bike = self.get_object()
        serializer = self.get_serializer(instance=bike, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        bike = serializer.save()
        read_serializer = DetailFurnitureSerializer(instance=bike, context={'request': request})
        return Response(read_serializer.data)

    def delete(self, request, *args, **kwargs):
        bike = self.get_object()
        bike.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

class ReviewListView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        furniture = get_object_or_404(Furniture, pk=self.kwargs['furniture_pk'])
        serializer.save(user=self.request.user, furniture=furniture)

    def get_queryset(self):
        furniture = get_object_or_404(Furniture, pk=self.kwargs['furniture_pk'])
        return Review.objects.filter(furniture=furniture)
