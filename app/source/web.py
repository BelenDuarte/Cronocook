from flask import Flask

server = Flask(
	__name__,
	template_folder='ui/templates',
	static_folder='../static'
)

server.secret_key = "a_secure_random_key"
