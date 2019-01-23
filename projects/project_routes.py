from flask import Blueprint, jsonify, request, render_template, redirect, url_for


project_blueprint = Blueprint('projects', __name__)


@project_blueprint.route('/', methods=['GET'])
def test():
    return 'meh'


@project_blueprint.route('/new', methods=['GET', 'POST'])
def new_project():
    if request.method == 'GET':
        return render_template('projects/add_project.html')
