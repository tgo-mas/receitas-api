"""
Views para a API de Receitas
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Receita,
    Categoria,
    Ingrediente,
)
from receita import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'categorias',
                OpenApiTypes.STR,
                description='Lista de IDs de categorias separada por vírgula'
            ),
            OpenApiParameter(
                'ingredientes',
                OpenApiTypes.STR,
                description='Lista de IDs de ingredientes separada por vírgula'
            )
        ]
    )
)
class ReceitaViewSet(viewsets.ModelViewSet):
    """View para API de Receitas."""
    serializer_class = serializers.DetalhesReceitaSerializer
    queryset = Receita.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, queries):
        '''Transforma os parâmetros da URL em inteiros.'''
        return [int(str_id) for str_id in queries.split(',')]

    def get_queryset(self):
        """Retorna receitas criadas pelo user autenticado."""
        categorias = self.request.query_params.get('categorias')
        ingredientes = self.request.query_params.get('ingredientes')
        queryset = self.queryset

        if categorias:
            categoria_ids = self._params_to_ints(categorias)
            queryset = queryset.filter(categorias__id__in=categoria_ids)
        if ingredientes:
            ingrediente_ids = self._params_to_ints(ingredientes)
            queryset = queryset.filter(ingredientes__id__in=ingrediente_ids)
        
        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()


    def get_serializer_class(self):
        """Retorna a classe serializer da requisição."""
        if self.action == 'list':
            return serializers.ReceitaSerializer
        elif self.action == 'upload_imagem':
            return serializers.ImagemReceitaSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Cria uma nova receita."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-imagem')
    def upload_imagem(self, request, pk=None):
        '''Faz upload de uma imagem para uma receita.'''
        receita = self.get_object()
        serializer = self.get_serializer(receita, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BaseReceitaAttrViewSet(mixins.DestroyModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    '''ViewSet base para atributos de receitas.'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retorna a lista de categorias do usuário logado."""
        return self.queryset\
            .filter(user=self.request.user)\
            .order_by('-nome')  

class CategoriaViewSet(BaseReceitaAttrViewSet):
    """ViewSet para listar categorias."""
    serializer_class = serializers.CategoriaSerializer
    queryset = Categoria.objects.all()

class IngredienteViewSet(BaseReceitaAttrViewSet):
    """ViewSet para a listagem de ingredientes."""
    serializer_class = serializers.IngredienteSerializer
    queryset = Ingrediente.objects.all()

