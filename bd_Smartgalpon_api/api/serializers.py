from django.contrib.auth.models import User
from rest_framework import serializers


# =============================================================================
# SERIALIZERS DE AUTENTICACIÓN
# =============================================================================
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Las contraseñas no coinciden.'}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# =============================================================================
# SERIALIZERS DE VALIDACIÓN - ENGORDE
# =============================================================================
class LoteCreateSerializer(serializers.Serializer):
    cantidad_pollos = serializers.IntegerField(min_value=1)
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = serializers.DateField()


class InsumoSerializer(serializers.Serializer):
    lotes_id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=100)
    cantidad = serializers.IntegerField(min_value=1)
    unidad = serializers.CharField(max_length=50)
    precio = serializers.DecimalField(max_digits=10, decimal_places=2)
    tipo = serializers.ChoiceField(choices=[
        'Alimento', 'Medicamento', 'Vacuna', 'Vitamina', 'Desinfectante', 'Otro'
    ])
    fecha = serializers.DateField()


class RegistroPesoSerializer(serializers.Serializer):
    lotes_id = serializers.IntegerField()
    peso_promedio = serializers.DecimalField(max_digits=10, decimal_places=2)
    fecha = serializers.DateField(required=False)


class MortalidadSerializer(serializers.Serializer):
    lote_id = serializers.IntegerField()
    cantidad_muerta = serializers.IntegerField(min_value=1)


class EliminarInsumoSerializer(serializers.Serializer):
    lote_id = serializers.IntegerField()


# =============================================================================
# SERIALIZERS DE VALIDACIÓN - PONEDORAS
# =============================================================================
class LotePonedoraCreateSerializer(serializers.Serializer):
    cantidad_gallinas = serializers.IntegerField(min_value=1)
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = serializers.DateField()


class InsumoPonedoraSerializer(serializers.Serializer):
    lotes_id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=100)
    cantidad = serializers.IntegerField(min_value=1)
    unidad = serializers.CharField(max_length=50)
    precio = serializers.DecimalField(max_digits=10, decimal_places=2)
    tipo = serializers.ChoiceField(choices=[
        'Alimento', 'Medicamento', 'Vacuna', 'Vitamina', 'Desinfectante', 'Otro'
    ])
    fecha = serializers.DateField()


class RegistroHuevosSerializer(serializers.Serializer):
    lote_id = serializers.IntegerField()
    fecha = serializers.DateField()
    cantidad_huevos = serializers.IntegerField(min_value=1)


class RegistroPesoPonedoraSerializer(serializers.Serializer):
    lotes_id = serializers.IntegerField()
    fecha = serializers.DateField()
    peso_promedio = serializers.DecimalField(max_digits=10, decimal_places=2)


class PrecioHuevoSerializer(serializers.Serializer):
    lote_id = serializers.IntegerField()
    precio_por_huevo = serializers.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = serializers.DateField()
