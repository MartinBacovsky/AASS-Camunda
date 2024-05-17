import django.contrib.auth.models

# Create your models here.


from django.db import models


class Book(models.Model):
    book_title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200, blank=False, default='')
    author = models.CharField(max_length=50, blank=False, default='')
    #published_date = models.DateField(blank=False, default='')
    #isbn = models.CharField(max_length=20, blank=False, default='')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.book_title


class Rental(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rented_date = models.DateField(blank=False, default='')
    rented_by = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.rented_by.username}" + f" rented book: {self.book.book_title} on " + f"{self.rented_date}"


class Return(models.Model):
    rental = models.OneToOneField(Rental, on_delete=models.SET_NULL, related_name='return_detail',null=True)
    return_date = models.DateField(auto_now_add=True)
    condition = models.CharField(max_length=50, blank=True)  # Optional: track condition of book upon return
    returned_by = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"Return for {self.rental.book.book_title}"