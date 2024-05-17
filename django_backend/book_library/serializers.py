from rest_framework import serializers
from .models import Book, Rental
from django.contrib.auth.models import User

from .models import Return


class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'book_title', 'description', 'author', 'available']


class RentalSerializer(serializers.ModelSerializer):
    # rented_by = serializers.ReadOnlyField(source='rented_by.username')

    class Meta:
        model = Rental
        fields = ['id', 'book', 'rented_date', 'rented_by']
