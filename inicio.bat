@echo off

:: Definir la ruta del proyecto
set PROJECT_DIR=%~dp0ProyWeb_diaz_Manriquez_riffo_Seccion_001D-main

:: Ir al directorio del proyecto
cd /d %PROJECT_DIR%

:: Crear entorno virtual
python -m venv venv

:: Activar entorno virtual
call venv\Scripts\activate

:: Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

:: Aplicar migraciones
python manage.py migrate

:: Ejecutar el servidor
python manage.py runserver

:: Pausar para ver mensajes de error o confirmación
pause
