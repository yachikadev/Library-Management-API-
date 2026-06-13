from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import date
from .models import Author, Book, Member, IssuedBook
from .serializers import AuthorSerializer, BookSerializer, MemberSerializer, IssuedBookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class IssuedBookViewSet(viewsets.ModelViewSet):
    queryset = IssuedBook.objects.all()
    serializer_class = IssuedBookSerializer

    @action(detail=False, methods=['post'])
    def borrow(self, request):
        book_id = request.data.get('book_id')
        member_id = request.data.get('member_id')
        due_date = request.data.get('due_date')

        
        if not all([book_id, member_id, due_date]):
            return Response(
                {'error': 'book_id, member_id, due_date required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            book = Book.objects.get(pk=book_id)
            member = Member.objects.get(pk=member_id)
        except (Book.DoesNotExist, Member.DoesNotExist):
            return Response({'error': 'Book or Member not found'}, status=status.HTTP_404_NOT_FOUND)

        
        if book.available_copies <= 0:
            return Response({'error': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)

        
        already_borrowed = IssuedBook.objects.filter(
            book=book, member=member, return_date__isnull=True
        ).exists()
        if already_borrowed:
            return Response({'error': 'Member already has this book'}, status=status.HTTP_400_BAD_REQUEST)

        
        issued = IssuedBook.objects.create(
            book=book,
            member=member,
            due_date=due_date
        )

        book.available_copies -= 1
        book.save()

        return Response(IssuedBookSerializer(issued).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        try:
            issued = IssuedBook.objects.get(pk=pk, return_date__isnull=True)
        except IssuedBook.DoesNotExist:
            return Response({'error': 'Active issue not found'}, status=status.HTTP_404_NOT_FOUND)

        today = date.today()
        issued.return_date = today

        
        if today > issued.due_date:
            overdue_days = (today - issued.due_date).days
            issued.fine_amount = overdue_days * 5  
        issued.save()

        # Increase available copies
        book = issued.book
        book.available_copies += 1
        book.save()

        return Response(IssuedBookSerializer(issued).data)