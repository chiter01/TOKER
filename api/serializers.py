from rest_framework import serializers
from furniture.models import Category, CommercialBuilding, Furniture, GardenAndOutbuildings, HouseAndResidentialBuilding, Review
from django.contrib.auth.models import User

class GardenAndOutbuildingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = GardenAndOutbuildings
        fields = ['id', 'name',]


class CommercialBuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommercialBuilding
        fields = ['id', 'name',]


class HouseAndResidentialBuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = HouseAndResidentialBuilding
        fields = ['id', 'name',]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ListFurnitureSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    garden = GardenAndOutbuildingsSerializer()
    commercial = CommercialBuildingSerializer()
    house = HouseAndResidentialBuildingSerializer()
    class Meta:
        model = Furniture
        fields = '__all__'



class DetailFurnitureSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    garden = GardenAndOutbuildingsSerializer()
    commercial = CommercialBuildingSerializer()
    house = HouseAndResidentialBuildingSerializer()
    class Meta:
        model = Furniture
        fields = '__all__'


class FurnitureSerializer(serializers.ModelSerializer):


    class Meta:
        model = Furniture
        fields = '__all__'



    def create(self, validated_data):

        product = super().create(validated_data)
        product.save()

        return product

    def update(self, instance, validated_data):
        product: Furniture = super().update(instance, validated_data)
        product.save()

        return product

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'stars', 'comment', 'created_at']

