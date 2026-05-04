# Sistema de Registro de Incidencias

Este proyecto demuestra el Ciclo de Vida del Dato en una aplicación web, transformando datos brutos en información útil para un gerente.

## Objetivos

1. **Control de Entrada (Evitando el Ruido)**: Validación en el servidor para asegurar que la descripción tenga al menos 10 caracteres.
2. **Clasificación (Tipos de Información)**: Categorización de incidencias en A (Crítica) y B (Leve).
3. **Dashboard de Decisiones (Atributo de Oportunidad)**: Reporte en tiempo real con KPIs como incidencias pendientes hoy, tiempo promedio de respuesta y total de críticas.

## Tecnologías

- **Backend**: Python con Flask
- **Base de Datos**: SQLite
- **Frontend**: HTML, CSS (Bootstrap), JS (Chart.js)

## Instalación y Ejecución

1. Asegúrate de tener Python instalado.
2. Instala Flask: `pip install flask`
3. Ejecuta la aplicación: `python app.py`
4. Abre en el navegador: `http://127.0.0.1:5000`

## Funcionalidades

- **Formulario de Incidencia**: Valida entrada y clasifica en categorías.
- **Dashboard**: Muestra estadísticas oportunas y lista de incidencias.
- **Resolución**: Permite marcar incidencias como resueltas, calculando tiempo de respuesta.

## Atributos de Calidad

- **Oportunidad**: Información en tiempo real (pendientes hoy).
- **Exactitud**: Validaciones evitan datos incompletos.
- **Relevancia**: Enfoque en críticas para decisiones gerenciales.
