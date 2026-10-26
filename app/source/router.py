from flask import render_template, request, redirect, url_for, flash

from app.source.ui.routes.index    import index_route
from app.source.ui.routes.menu     import menu_route
from app.source.ui.routes.add_food import add_food_route
