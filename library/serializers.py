from rest_framework import serializers
from .models import Author, Book, Member, IssuedBook


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_name', 'isbn', 'genre', 'total_copies', 'available_copies']


class MemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'username', 'membership_type']


class IssuedBookSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    member_username = serializers.CharField(source='member.user.username', read_only=True)

    class Meta:
        model = IssuedBook
        fields = ['id', 'book', 'book_title', 'member', 'member_username', 'issued_date', 'due_date', 'return_date', 'fine_amount']
        