#pyhton3 manage.py
def deploy():
	from app import create_app,db
	from models import User
	app = create_app()
	app.app_context().push()
	db.create_all()
deploy()
	