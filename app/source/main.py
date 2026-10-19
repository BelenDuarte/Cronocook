from litestar.plugins.htmx import HTMXPlugin
from litestar import Litestar, get

from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig

from pathlib import Path

@get("/form")
async def get_form() -> dict:
	return {"message": "Hello, Litestar with HTMX!"}

server = Litestar(
	route_handlers=[get_form],
	debug=True,
	plugins=[HTMXPlugin()],
	template_config=TemplateConfig(
		directory=Path("litestar_htmx/templates"),
		engine=JinjaTemplateEngine,
	),
)
