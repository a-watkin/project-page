import subprocess
from flask import Flask

from projects.project_routes import project_blueprint
from user.user_routes import user_blueprint

from flask import Flask, render_template

app = Flask(__name__)
# Markdown(app)

# template_folder='blog/templates',
# static_folder = 'blog/static'

app.register_blueprint(project_blueprint, url_prefix="/projects")
app.register_blueprint(user_blueprint, url_prefix="/user")

app.config.update(
    TESTING=True,
    SECRET_KEY='whyohwhy'
)


@app.route('/', methods=['GET'])
def test():
    return render_template('home.html')


if __name__ == '__main__':
    export_settings = [
        "export FLASK_APP=app.py",
        "export FLASK_ENV=development",
        "export FLASK_DEBUG=1"
    ]

    for command in export_settings:
        print(command.split())
        process = subprocess.Popen(
            command.split(),
            stdout=subprocess.PIPE,
            shell=True
        )

    app.run(
        debug=True,
        port=6060
    )
