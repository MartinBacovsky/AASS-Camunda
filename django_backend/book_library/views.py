import json

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Book, Rental, Return
from .serializers import BookSerializer, RentalSerializer, ReturnSerializer
import requests
import logging


# In your Django views.py or api.py
from django.http import JsonResponse
from .models import Book

def check_availability(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
        return JsonResponse({'available': book.available})
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        # Initially check if the book is available
        book_available = book.available
        if not book_available:
            # Here, raise an exception if the book is not available
            raise Exception({'message': 'This book is not available for rental.'})

        instance = serializer.save()

        # Update the book's availability
        book.available = False
        book.save()

        # Start Camunda process, now including the result of the availability check
        self.start_camunda_process(instance, book_available)


    def start_camunda_process(self, rental_instance, book_available):
        url = "http://localhost:8080/engine-rest/process-definition/key/rental_process/start"
        payload = {
            "variables": {
                "book_id": {"value": str(rental_instance.book.id), "type": "String"},
                "user_id": {"value": str(rental_instance.id), "type": "String"},
                # Pass the result of the book availability check into Camunda
                "bookAvailable": {"value": book_available, "type": "Boolean"},
                # Ensure this matches Camunda's expected variable
                "result": {"value": False, "type": "Boolean"}
            },
            "withVariablesInReturn": True
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # This will raise an HTTP error if the status code was not 200-299
        except requests.RequestException as e:
            print(f"Failed to start Camunda process: {e}")


class ReturnViewSet(viewsets.ModelViewSet):
    queryset = Return.objects.all()
    serializer_class = ReturnSerializer

    def create(self, request, *args, **kwargs):
        rental_id = request.data.get('rental')
        if not rental_id:
            return Response({'error': 'Rental ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        rental = Rental.objects.get(id=rental_id)
#        if rental.return_detail:
#            return Response({'error': 'Return already processed'}, status=status.HTTP_404_NOT_FOUND)

        rental.book.available = True
        rental.book.save()
        response = super().create(request, *args, **kwargs)
        rental.delete()
        return response

class TrendingViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.order_by('?')[:3]
    serializer_class = BookSerializer
