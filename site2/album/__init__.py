from flask import Flask,request,render_template,flash,redirect,url_for

def create_app():
    app=Flask('album')
    
    app.config.from_pyfile('settings.py')

    from . import auth
    app.register_blueprint(auth.bp)
    from . import album
    app.register_blueprint(album.bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    return app



