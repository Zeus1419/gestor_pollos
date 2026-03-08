from datetime import date, datetime
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .factories.factory_insumo import InsumoFactory
from .serializers import (
    LoteCreateSerializer,
    InsumoSerializer,
    RegistroPesoSerializer,
    MortalidadSerializer,
    EliminarInsumoSerializer,
)


@api_view(['DELETE'])
def eliminar_insumo(request, insumo_id):
    serializer = EliminarInsumoSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    lote_id = serializer.validated_data['lote_id']
    try:
        with connection.cursor() as cursor:
            cursor.callproc('sp_eliminar_insumo', [lote_id, insumo_id])
        return Response({'success': True})
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def detalle_lote(request, lote_id):
    try:
        with connection.cursor() as cursor:
            cursor.callproc("sp_detalle_lote", [lote_id])

            # Primer resultado (Lote)
            result_lote = cursor.fetchall()
            columns_lote = [col[0] for col in cursor.description]
            lote_data = [dict(zip(columns_lote, row)) for row in result_lote]

            # Segundo resultado (Insumos)
            cursor.nextset()
            result_insumos = cursor.fetchall()
            columns_insumos = [col[0] for col in cursor.description]
            insumos_data = [dict(zip(columns_insumos, row)) for row in result_insumos]

            # Tercer resultado (Registros de peso)
            cursor.nextset()
            result_pesos = cursor.fetchall()
            columns_pesos = [col[0] for col in cursor.description]
            pesos_data = [dict(zip(columns_pesos, row)) for row in result_pesos]

        return Response({
            "lote": lote_data,
            "insumos": insumos_data,
            "registro_peso": pesos_data
        })
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def agregar_insumo(request):
    serializer = InsumoSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    insumo_data = InsumoFactory.build_insumo(serializer.validated_data)

    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                "sp_agregar_insumo",
                [
                    insumo_data["lotes_id"],
                    insumo_data["nombre"],
                    insumo_data["cantidad"],
                    insumo_data["unidad"],
                    insumo_data["precio"],
                    insumo_data["tipo"],
                    insumo_data["fecha"],
                ]
            )
        return Response({"success": True}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def crearLote(request):
    serializer = LoteCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    user_id = request.user.id
    
    try:
        with connection.cursor() as cursor:
            # Insertar lote con usuario_id
            cursor.execute('''
                INSERT INTO api_lote (usuario_id, nombre, cantidad_pollos, precio_unitario, fecha_inicio, cantidad_muerto, estado, edad_dias)
                VALUES (%s, %s, %s, %s, %s, 0, 0, 0)
            ''', [user_id, f"Lote {datetime.now().strftime('%Y%m%d%H%M%S')}", data['cantidad_pollos'], data['precio_unitario'], data['fecha_inicio']])
            
            # Obtener el lote creado
            cursor.execute('SELECT * FROM api_lote WHERE id = LAST_INSERT_ID()')
            columns = [col[0] for col in cursor.description]
            lote_data = dict(zip(columns, cursor.fetchone()))

        return Response({"success": True, "lote": lote_data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listarLotes(request):
    try:
        # Filtrar lotes por usuario autenticado
        user_id = request.user.id
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM api_lote WHERE usuario_id = %s', [user_id])
            results = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

        data = [dict(zip(columns, row)) for row in results]
        return Response(data)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def registrar_peso(request):
    serializer = RegistroPesoSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    lotes_id = data['lotes_id']
    peso_promedio = data['peso_promedio']
    fecha = data.get('fecha', date.today())

    try:
        with connection.cursor() as cursor:
            cursor.callproc('sp_registrar_peso', [lotes_id, fecha, peso_promedio])
            result = cursor.fetchone()

        return Response({
            'success': True,
            'message': 'Peso registrado correctamente',
            'registro_id': result[0] if result else None
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def eliminar_lote(request, lote_id):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('sp_eliminar_lote', [lote_id])
        return Response({'success': True})
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def registrar_mortalidad(request):
    """Registra nueva mortalidad - el trigger se encarga del registro"""
    serializer = MortalidadSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    lote_id = data['lote_id']
    cantidad_muerta = data['cantidad_muerta']

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE lote 
                SET cantidad_muerto = cantidad_muerto + %s
                WHERE id = %s
            """, [cantidad_muerta, lote_id])

            if cursor.rowcount == 0:
                return Response({'error': 'Lote no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Mortalidad registrada correctamente'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def historial_mortalidad(request, lote_id):
    """Obtiene el historial de mortalidad para un lote específico"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre, cantidad_muerto FROM lote WHERE id = %s", [lote_id])
            lote = cursor.fetchone()

            if not lote:
                return Response({'error': 'Lote no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, fecha, cantidad_muerta 
                FROM registro_mortalidad 
                WHERE lote_id = %s 
                ORDER BY fecha DESC
            """, [lote_id])
            registros = cursor.fetchall()

        historial_data = []
        for registro in registros:
            historial_data.append({
                'id': registro[0],
                'fecha': registro[1].strftime('%Y-%m-%d') if registro[1] else None,
                'cantidad_muerta': registro[2]
            })

        return Response({
            'lote_id': lote_id,
            'lote_nombre': lote[1],
            'cantidad_muerto_total': lote[2],
            'historial': historial_data
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def obtener_edad_lote(request, lote_id):
    """Obtiene específicamente la edad_dias de un lote usando conexión directa"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre, edad_dias FROM lote WHERE id = %s", [lote_id])
            lote = cursor.fetchone()

            if not lote:
                return Response({'error': 'Lote no encontrado'}, status=status.HTTP_404_NOT_FOUND)

            return Response({
                'lote_id': lote[0],
                'nombre': lote[1],
                'edad_dias': lote[2]
            })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
