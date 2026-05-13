@echo off
cls
echo ===============================================
echo   🚀 Iniciando servidor Django: Norean App Beta
echo ===============================================

REM === Ir a la carpeta del entorno virtual ===
cd /d "C:\Users\HP-245-G9\OneDrive - unicesar.edu.co\Documentos\INGENIERIA DE SOFTWARE I\EL SOFTWARE TIENDA COFLA\software"

REM === Activar el entorno virtual ===
call Scripts\activate

REM === Ir a la carpeta del proyecto Django ===
cd "C:\Users\HP-245-G9\OneDrive - unicesar.edu.co\Documentos\INGENIERIA DE SOFTWARE I\EL SOFTWARE TIENDA COFLA\proyects\app_management_inventory"

REM === Mostrar qué Python se está usando ===
echo.
echo 🐍 Entorno virtual activo:
where python
echo.

REM === Abrir automáticamente el navegador ===
start http://127.0.0.1:8000


REM === Ejecutar el servidor Django ===
python manage.py runserver 0.0.0.0:8000


REM === Mantener la ventana abierta después de cerrar el servidor ===
echo.
echo ===============================================
echo   💡 Servidor detenido. Cierra esta ventana.
echo ===============================================
pause
