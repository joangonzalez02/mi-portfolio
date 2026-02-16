# Mi Portfolio

Mi portafolio personal donde muestro mis proyectos seleccionados de GitHub. Puedo elegir qué proyectos mostrar, agregar descripciones personalizadas, imágenes de preview y enlaces a demostraciones en vivo.

## Características

- ✨ Selecciono qué proyectos mostrar mediante `featured.json`
- 🎨 Diseño moderno con glassmorphism y tarjetas interactivas
- 📸 Extrae automáticamente imágenes del README de cada proyecto
- 🔗 Botones para ver demos en vivo y acceder al código
- 📱 Responsive y se ve bien en cualquier dispositivo
- 🏷️ Etiquetas por proyecto para clasificarlos
- 🌙 Modal interactivo con preview del README

## Instalación local

### Requisitos
- Python 3.9+
- Git

### Pasos

1. Clona el repositorio:
```bash
git clone https://github.com/joangonzalez02/mi-portfolio.git
cd mi-portfolio
```

2. Crea y activa un ambiente virtual (PowerShell en Windows):
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Crea un archivo `.env` con tus datos (copia `.env.example` como referencia):
```
GITHUB_USER=tu_usuario_github
SITE_NAME=Tu Nombre Completo
SITE_ACCENT=Mi
```

5. Ejecuta el servidor:
```bash
python app.py
```

6. Abre http://localhost:5000 en tu navegador.

## Configuración

### Variables de entorno (`.env`)

- `GITHUB_USER`: Tu usuario de GitHub (requerido si no usas `featured.json`)
- `SITE_NAME`: Tu nombre completo que aparece en el hero
- `SITE_ACCENT`: La primera palabra del título en la cabecera (en azul). Defecto: "Mi"
- `GITHUB_TOKEN`: (Opcional) Token personal de GitHub para más solicitudes a la API

### Seleccionar proyectos (`featured.json`)

Edita `featured.json` para elegir qué proyectos mostrar:

```json
[
  {
    "owner": "tu_usuario",
    "repo": "nombre-del-repo",
    "title": "Título personalizado",
    "description": "Descripción del proyecto",
    "image": "/static/previews/1.png",
    "homepage": "https://link-a-demo.com",
    "tags": ["Flask", "Python"]
  }
]
```

## Despliegue

### En Render (recomendado)

1. Ve a https://render.com y crea una cuenta
2. Conecta tu cuenta de GitHub
3. Crea un nuevo Web Service:
   - Selecciona este repositorio
   - Build Command: (dejar vacío)
   - Start Command: `gunicorn app:app`
4. En "Environment" añade las variables de producción:
   - `GITHUB_USER=tu_usuario`
   - `SITE_NAME=Tu Nombre`
   - `SITE_ACCENT=Mi` (o lo que prefieras)
5. Render hace deploy automático cada que haces push a `main`

## Estructura del proyecto

```
.
├── app.py              # Aplicación Flask
├── requirements.txt    # Dependencias de Python
├── Procfile           # Configuración para Render/Heroku
├── runtime.txt        # Versión de Python
├── featured.json      # Proyectos a mostrar
├── .env               # Variables de entorno (no incluir en git)
├── templates/         # Templates HTML
│   ├── base.html
│   ├── index.html
│   └── project.html
└── static/            # CSS, JS, imágenes
    ├── css/
    ├── js/
    └── previews/      # Imágenes de preview
```

## Próximos pasos

- [ ] Agregar más proyectos a `featured.json`
- [ ] Personalizar el CSS en `static/css/style.css`
- [ ] Cambiar el color de acento en las variables de entorno
- [ ] Agregar más información en la sección "Sobre mí"

---

Hecho con 💙



