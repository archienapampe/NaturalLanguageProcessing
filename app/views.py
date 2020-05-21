from app import app
from app import controllers


@app.route('/')
def test():
    return controllers.TestToRun().call()