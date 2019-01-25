import os
import sys
import datetime

from flask import Blueprint, jsonify, request, render_template, redirect, url_for


try:
    from .projects import Project
    from .common.utils import login_required
except Exception as e:
    print('project routes import error', print(sys.path))
    print('\n', os.getcwd(), '\n')
    from .projects import Project
    from common.utils import login_required


project_blueprint = Blueprint('projects', __name__)


@project_blueprint.route('/', methods=['GET'])
def get_projects():
    p = Project()
    project_data = p.get_projects()
    return render_template('projects/projects.html', projects=project_data)


@project_blueprint.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    p = Project()
    project_data = p.get_project(project_id)
    return render_template('projects/project.html', projects=project_data)


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

        return redirect(url_for('projects.get_projects'))


@project_blueprint.route('/edit/<int:project_id>', methods=['GET'])
def edit_project(project_id):
    pass


@project_blueprint.route('/delete/<int:project_id>', methods=['GET', 'POST'])
@login_required
def delete_project(project_id):
    p = Project()
    p.remove_project(project_id)
    return redirect(url_for('projects.get_projects'))


@project_blueprint.route('/deleted', methods=['GET', 'POST'])
@login_required
def deleted_projects():
    p = Project()
    deleted_projects = p.get_deleted_projects()
    return render_template('projects/deleted_projects.html', projects=deleted_projects)


@project_blueprint.route('/purge', methods=['GET'])
@login_required
def purge_deleted_projects():
    p = Project()
    p.purge_deleted_projects()
    return redirect(url_for('projects.get_projects'))


@project_blueprint.route('/restore/<int:project_id>', methods=['GET'])
@login_required
def restore_deleted_projects(project_id):
    p = Project()
    p.restore_project(project_id)
    return redirect(url_for('projects.get_projects'))
