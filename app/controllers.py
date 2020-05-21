from flask import render_template, make_response


class BaseController:
    def __init__(self):
        pass
    
    def call(self, *args, **kwargs):
        try:
            return self._call(*args, **kwargs)
        except Exception as e:
            return make_response(str(e), 500)
        
    def _call(self, *args, **kwargs):
        raise NotImplementedError('_call')
    

class StartProcess(BaseController):
    def _call(self):
        return render_template('index.html')