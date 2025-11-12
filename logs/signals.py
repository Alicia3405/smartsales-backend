from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import LogEntry

# Deshabilitamos la señal 'user_logged_in' porque no cumple
# el requisito de registrar N veces el login.
# Moveremos esta lógica a la vista de Login (users/views.py).

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    pass # No hacer nada aquí