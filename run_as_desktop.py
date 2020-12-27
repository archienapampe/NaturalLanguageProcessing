from contextlib import redirect_stdout
from io import StringIO

import webview  

from app import app


if __name__ == '__main__':
    stream = StringIO()
    with redirect_stdout(stream):
        window = webview.create_window('NLP desktop application', app)
        webview.start(debug=True)

