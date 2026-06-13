from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, MemberViewSet, IssuedBookViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'members', MemberViewSet)
router.register(r'issued', IssuedBookViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]