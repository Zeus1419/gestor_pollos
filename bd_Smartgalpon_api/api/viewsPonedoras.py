from datetime import datetime
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    LotePonedoraCreateSerializer,
    InsumoPonedoraSerializer,
    RegistroHuevosSerializer,
    RegistroPesoPonedoraSerializer,
    PrecioHuevoSerializer,
)


@api_view(['POST'])
def crearLotePonedora(request):
    serializer = LotePonedoraCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    user_id = request.user.id
    
    try:
        with connection.cursor() as cursor:
            # Insertar lote ponedora con usuario_id
            cursor.execute('''
                INSERT INTO api_loteponedora (usuario_id, nombre, cantidad_gallinas, precio_unitario, fecha_inicio, cantidad_muerto, estado, edad_semanas, muertos_semanales)
                VALUES (%s, %s, %s, %s, %s, 0, 0, 0, 0)
            ''', [user_id, f"Ponedora {datetime.now().strftime('%Y%m%d%H%M%S')}", data['cantidad_gallinas'], data['precio_unitario'], data['fecha_inicio']])
            
            # Obtener el lote creado
            cursor.execute('SELECT * FROM api_loteponedora WHERE id = LAST_INSERT_ID()')
            columns = [col[0] for col in cursor.description]
            lote_data = dict(zip(columns, cursor.fetchone()))

        return Response({
            'success': True,
            'message': 'Lote creado correctamente',
            'lote': lote_data
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def detalleLotePonedora(request, lote_id):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('sp_detalle_lote_ponedora', [lote_id])

            # Primer conjunto → Lote
            columns = [col[0] for col in cursor.description]
            lote_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            # Siguiente conjunto → Insumos
            cursor.nextset()
            columns = [col[0] for col in cursor.description]
            insumos_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            # Siguiente conjunto → Registros de peso
            cursor.nextset()
            columns = [col[0] for col in cursor.description]
            registros_peso_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            # Siguiente conjunto → Registros de huevos
            cursor.nextset()
            columns = [col[0] for col in cursor.description]
            registros_huevos_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if not lote_data:
            return Response({'success': False, 'error': 'Lote no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'success': True,
            'lote': lote_data[0],
            'insumos': insumos_data,
            'registros_peso': registros_peso_data,
            'registros_huevos': registros_huevos_data
        })
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ListaPonedoras(request):
    try:
        # Filtrar ponedoras por usuario autenticado
        user_id = request.user.id
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM api_loteponedora WHERE usuario_id = %s', [user_id])
            columns = [col[0] for col in cursor.description]
            lotes = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response({'success': True, 'lotes': lotes})
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def agregarInsumoPonedora(request):
    serializer = InsumoPonedoraSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    try:
        with connection.cursor() as cursor:
            cursor.callproc('sp_agregar_insumo_ponedora', [
                data['lotes_id'],
                data['nombre'],
                data['cantidad'],
                data['unidad'],
                data['precio'],
                data['tipo'],
                data['fecha']
            ])
            result = cursor.fetchone()

        return Response({
            'success': True,
            'message': 'Insumo agregado correctamente',
            'insumo_id': result[0] if result else None
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminarInsumoPonedora(request, insumo_id):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('sp_eliminar_insumo_ponedora', [insumo_id])
            result = cursor.fetchone()

        return Response({
            'success': True,
            'message': result[0] if result else 'Insumo eliminado correctamente',
            'insumo_eliminado': result[1] if result else insumo_id
        })
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def agregarRegistroHuevos(request):
    serializer = RegistroHuevosSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    try:
        with connection.cursor() as cursor:
            cursor.callproc('sp_agregar_registro_huevos', [
                data['lote_id'],
                data['fecha'],
                data['cantidad_huevos']
            ])
            result = cursor.fetchone()

        return Response({
            'success': True,
            'message': 'Registro de huevos agregado correctamente',
            'registro_id': result[0] if result else None
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def agregarRegistroPeso(request):
    serializer = RegistroPesoPonedoraSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    try:
        with connection.cursor() as cursor:
            cursor.callproc('sp_agregar_registro_peso', [
                data['lotes_id'],
                data['fecha'],
                data['peso_promedio']
            ])
            result = cursor.fetchone()

        return Response({
            'success': True,
            'message': 'Registro de peso agregado correctamente',
            'registro_id': result[0] if result else None
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def establecerPrecioHuevo(request):
    serializer = PrecioHuevoSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    try:
        with connection.cursor() as cursor:
            cursor.callproc('sp_establecer_precio_huevo', [
                data['lote_id'],
                data['precio_por_huevo'],
                data['fecha_inicio']
            ])
            result = cursor.fetchone()

        return Response({
            'success': True,
            'message': 'Precio establecido correctamente',
            'precio_id': result[0] if result else None
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def calcularGananciaHuevos(request, lote_id):
    try:
        fecha_inicio = request.query_params.get('fecha_inicio', None)
        fecha_fin = request.query_params.get('fecha_fin', None)

        if not fecha_inicio or not fecha_fin:
            return Response({
                'success': False,
                'error': 'Los parámetros fecha_inicio y fecha_fin son requeridos'
            }, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.callproc('sp_calcular_ganancia_lote', [
                lote_id, fecha_inicio, fecha_fin
            ])
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response({
            'success': True,
            'lote_id': lote_id,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'ganancia': result[0] if result else {}
        })
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def resumenGananciaLote(request, lote_id):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('sp_resumen_ganancia_lote', [lote_id])

            if cursor.description:
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:
                result = []

        if not result:
            return Response({
                'success': False,
                'error': f'Lote {lote_id} no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'success': True,
            'resumen': result[0]
        })
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminarLotePonedora(request, lote_id):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('sp_eliminar_lote_ponedora', [lote_id])
            result = cursor.fetchone()

        return Response({
            'success': True,
            'message': result[0] if result else 'Lote eliminado correctamente',
            'lote_eliminado': result[1] if result else lote_id
        })
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)