import logging
from app.services.notification_service import NotificationService
from app.utils.config import settings

# Configurar logging básico para ver salida en consola
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_notifications():
    print("\n=== Prueba de Notificaciones ===\n")
    service = NotificationService()
    
    # 1. Prueba de WhatsApp
    print("--- 1. Generación de Enlace WhatsApp ---")
    telefono = input("Ingrese número de celular (con código de país, ej: 573001234567): ")
    if telefono:
        mensaje = "Hola, esta es una prueba del Sistema de Convocatorias 🚀"
        link = service.send_whatsapp_test(telefono, mensaje)
        print(f"\n✅ Copia y pega este enlace en tu navegador para probar:")
        print(f"{link}\n")
    
    # 2. Prueba de Correo
    print("--- 2. Envío de Correo Electrónico ---")
    print("Nota: Para que funcione, debes tener configurado SMTP en el archivo .env o config.py")
    print(f"Configuración actual: Server={settings.SMTP_SERVER}, User={settings.SMTP_USERNAME or 'No configurado'}")
    
    email = input("Ingrese correo de destino para prueba (deje vacío para omitir): ")
    if email:
        print("Enviando correo...")
        success = service.send_email(
            to_email=email,
            subject="Prueba de Sistema de Convocatorias",
            body="<h1>¡Hola!</h1><p>Esta es una prueba de notificación del <b>Sistema de Convocatorias</b>.</p>",
            is_html=True
        )
        
        if success:
            print("✅ Correo enviado exitosamente.")
        else:
            print("❌ Falló el envío del correo. Revise los logs y credenciales.")

if __name__ == "__main__":
    test_notifications()
