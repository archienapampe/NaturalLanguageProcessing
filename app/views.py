from app import app
from app import controllers


@app.route('/')
def start_process():
	return controllers.StartProcess().call()