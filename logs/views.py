from rest_framework import viewsets
from .models import LogEntry
from .serializers import LogEntrySerializer
from permissions import IsAdmin
from django.utils.dateparse import parse_date # Importar para las fechas

class LogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogEntry.objects.all().order_by('-timestamp')
    serializer_class = LogEntrySerializer
    permission_classes = [IsAdmin]

    # --- (NUEVO) AÑADIDO PARA FILTROS (CU-Bitácora) ---
    def get_queryset(self):
        """
        Sobrescribimos este método para aplicar filtros de la URL.
        """
        # Empezamos con la consulta base
        queryset = LogEntry.objects.all().order_by('-timestamp')

        # Obtenemos los parámetros de la URL (ej: /log/?user=admin)
        user_param = self.request.query_params.get('user', None)
        start_date_param = self.request.query_params.get('start_date', None)
        end_date_param = self.request.query_params.get('end_date', None)

        # 1. Aplicar filtro de usuario (búsqueda parcial en username)
        if user_param:
            queryset = queryset.filter(user__username__icontains=user_param)

        # 2. Aplicar filtro de fecha de inicio (mayor o igual)
        if start_date_param:
            start_date = parse_date(start_date_param)
            if start_date:
                queryset = queryset.filter(timestamp__date__gte=start_date)

        # 3. Aplicar filtro de fecha de fin (menor o igual)
        if end_date_param:
            end_date = parse_date(end_date_param)
            if end_date:
                queryset = queryset.filter(timestamp__date__lte=end_date)
                
        return queryset

