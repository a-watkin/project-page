import os
import sys

from flask import Blueprint, jsonify, request, render_template, redirect, url_for


from .projects import Project

# try:
#     from .blog.post import Post
#     from .tag.tag import Tag
#     from .common.utils import login_required
# except Exception as e:
#     print('post routes import error', print(sys.path))
#     print('\n', os.getcwd(), '\n')
#     from projects import Project

project_blueprint = Blueprint('projects', __name__)


@project_blueprint.route('/', methods=['GET'])
def test():
    p = Project()
    project_data = p.get_projects()
    return render_template('projects/projects.html', projects=project_data)


@project_blueprint.route('/new', methods=['GET', 'POST'])
def new_project():
    if request.method == 'GET':

        return render_template('projects/add_project.html')

    if request.method == 'POST':
        # this will be handled by tag call
        tags = request.form['tags']
        # split only if key exists
        if tags:
            tags = tags.split(',')

        # this will be handled by another class
        screenshots = request.form['screenshots']
        # split only if key exists
        if screenshots:
            screenshots = screenshots.split(',')

        # make new project object
        project_data = request.form.to_dict()
        p = Project(project_data)
        print(p)
        p.create_project()
