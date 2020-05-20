from app import app
import controllers


@app.route('/')
def test():
    return controllers.TestToRun().call()