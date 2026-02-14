# Portfolio Flask - Starter

Este es un proyecto pequeño en Flask que obtiene tus repositorios públicos de GitHub y los muestra en una página simple.

Características
- Obtiene repos con la API pública de GitHub
- Soporta token opcional para evitar límites de la API
- Plantilla HTML minimalista que puedes personalizar (añadir screenshots, demos, filtros)

Requisitos
- Python 3.8+

Cómo ejecutar (Windows PowerShell)

```powershell
# crear y activar entorno virtual
python -m venv venv
venv\Scripts\Activate
# instalar dependencias
pip install -r requirements.txt
# copiar y editar variables
copy .env.example .env
# editar .env y poner tu GITHUB_USER (OBLIGATORIO para que tu portfolio muestre tus repos automáticamente)
# opcionalmente añade GITHUB_TOKEN para aumentar el límite de la API
# ejecutar
python app.py
```

Abre: http://127.0.0.1:5000/ — la app usará el valor de `GITHUB_USER` en `.env` y mostrará directamente tus proyectos destacados.

Siguientes pasos recomendados
- Personalizar la plantilla `templates/index.html` con screenshots, etiquetas y enlaces a demos.
- Añadir una sección "Sobre mí" y formulario de contacto o enlace a LinkedIn.
- Crear un README destacado en cada repo de GitHub con instrucciones y demo.
- Deploy: puedes usar Render, Railway o Heroku (añade Procfile y variables de entorno). Si quieres, puedo añadir el archivo de deploy y CI.

Django
---
Si prefieres Django puedo generar un proyecto base que haga lo mismo (app llamada `projects`) con una vista que consuma la API de GitHub, templates, y configuración mínima para desplegar. ¿Quieres que la genere ahora?

Si quieres que conecte automáticamente repos seleccionados (por etiquetas o nombres) y muestre contenidos como screenshots y README renderizado, dime tus preferencias y lo implemento.
