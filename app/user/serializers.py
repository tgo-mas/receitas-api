"""
Serializers para a API de usuários
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer para o objeto User"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
            }
        }

    def create(self, validated_data):
        """Cria um usuário e o retorna com a senha criptografada"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Atualiza e retorna o novo usuário"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class TokenSerializer(serializers.Serializer):
    """Serializer para o token de usuário"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input-type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validar e autenticar o usuário"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Falha na autenticação: Credenciais inválidas.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
