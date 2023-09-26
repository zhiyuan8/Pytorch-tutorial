from app import app
from flask import (render_template,
                   send_from_directory)
import os

@app.route('/')
def index():
    hostname = os.uname()[1]
    return render_template('index.html', hostname=hostname)


# add the favicon.ico to the app
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Note that the code below is only used for the 
# development.
if __name__ == '__main__':
    # run flask app
    app.run(host='0.0.0.0', port=8040, debug=True)