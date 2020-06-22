from flask import request

from app import app, controllers


@app.route('/')
def raw_data_input():
	return controllers.RawDataInput().call()


@app.route('/result', methods=['POST'])
def start_process():
    if request.method == 'POST':
        rawdata = request.form['rawdata']
        return controllers.StartProcess().call(rawdata)