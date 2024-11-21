from django.urls import path
from .yasg import urlpatterns as url_doc
from .views import CategoryDetailView, CategoryListView, CommercialBuildingDetailView, CommercialBuildingListView, FurnitureListView, FurnitureDetailView, GardenAndOutbuildingsDetailView, GardenAndOutbuildingsListView, HouseAndResidentialBuildingDetailView, HouseAndResidentialBuildingListView, ReviewListView, ReviewDetailView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('furnitures/', FurnitureListView.as_view(), name='furniture-list'),
    path('furnitures/<int:pk>/', FurnitureDetailView.as_view(), name='furniture-detail'),
    path('furnitures/<int:furniture_pk>/reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('garden-and-outbuildings/', GardenAndOutbuildingsListView.as_view(), name='garden-and-outbuildings-list'),
    path('garden-and-outbuildings/<int:pk>/', GardenAndOutbuildingsDetailView.as_view(), name='garden-and-outbuildings-detail'),
    path('commercial-buildings/', CommercialBuildingListView.as_view(), name='commercial-building-list'),
    path('commercial-buildings/<int:pk>/', CommercialBuildingDetailView.as_view(), name='commercial-building-detail'),
    path('house-and-residential-buildings/', HouseAndResidentialBuildingListView.as_view(), name='house-and-residential-building-list'),
    path('house-and-residential-buildings/<int:pk>/', HouseAndResidentialBuildingDetailView.as_view(), name='house-and-residential-building-detail'),
]
urlpatterns += url_doc