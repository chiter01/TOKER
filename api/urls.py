from django.urls import path
from .yasg import urlpatterns as url_doc
from .views import CategoryListView, FurnitureListView, FurnitureDetailView, ReviewListView, ReviewDetailView

urlpatterns = [
   path('categories/', CategoryListView.as_view(), name='category-list'),
    path('furnitures/', FurnitureListView.as_view(), name='furniture-list'),
    path('furnitures/<int:pk>/', FurnitureDetailView.as_view(), name='furniture-detail'),
    path('furnitures/<int:furniture_pk>/reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
urlpatterns += url_doc