"""
URLs para a API de receitas.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from receita import views


router = DefaultRouter()
router.register('receita', views.ReceitaViewSet)

app_name = 'receita'

urlpatterns = [
    path('', include(router.urls))
]
