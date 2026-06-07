from django.contrib import admin
from .models import Author, Book, Member, IssuedBook

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'total_copies', 'available_copies']
    search_fields = ['title', 'isbn']
    list_filter = ['genre']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'membership_type']

@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'issued_date', 'due_date', 'return_date', 'fine_amount']