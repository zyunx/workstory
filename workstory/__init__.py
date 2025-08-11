import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import task
    app.register_blueprint(task.bp)

    from . import today
    app.register_blueprint(today.bp)

    from . import work
    app.register_blueprint(work.bp)

    @app.route('/hello')
    def hello():
        db.get_db()
        db.close_db()
        return 'Hello, world!'

    return app
    