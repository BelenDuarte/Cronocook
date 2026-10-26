from flask import render_template, request, redirect, url_for, flash

from routes.index    import index_route
from routes.menu     import menu_route
from routes.add_food import add_food_route
