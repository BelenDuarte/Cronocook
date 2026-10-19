from litestar.plugins.htmx import HTMXPlugin
from litestar import Litestar, get
from litestar.response import Template
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Ruta principal que renderiza home.html
@get("/")
async def home() -> Template:
    return Template(template_name="home.html", context={"title": "Litestar + HTMX"})

# Ruta de prueba para HTMX que devuelve un fragmento HTML
@get("/api/saludo")
async def saludo() -> str:
    return '<div class="p-4 bg-emerald-50 text-emerald-700 rounded-xl mt-4 border border-emerald-200 font-medium">¡Conexión exitosa con HTMX! 🚀</div>'

server = Litestar(
    route_handlers=[home, saludo],
    debug=True,
    plugins=[HTMXPlugin()],
    template_config=TemplateConfig(
        directory=BASE_DIR / "templates",
        engine=JinjaTemplateEngine,
    ),
)
