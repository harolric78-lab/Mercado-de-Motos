# Datos de Telegram — pendiente

Carpeta reservada para los datos crudos de Telegram.

Estado actual: **sin datos**. Para recolectarlos se necesita:

1. `api_id`, `api_hash` y número de teléfono (API oficial de Telegram).
2. La lista de canales/grupos públicos o privados a monitorear.
3. El código de inicio de sesión que Telegram envíe al teléfono.

Los archivos que se guarden aquí deben ser **copias crudas sin modificar** del
export o de la recolección (JSON), con el mismo formato que espera el ETL
(`{"mensajes": [...]}`).

Mientras no existan credenciales, el informe de mercado se calcula solo con
Revolico y deja constancia explícita de esta limitación.
