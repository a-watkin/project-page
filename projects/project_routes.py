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
    from projects.project_tag import ProjectTag


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
@login_required
def new_project():
    if request.method == 'GET':

        return render_template('projects/add_project.html')

    if request.method == 'POST':

        # make new project object
        project_data = request.form.to_dict()
        p = Project(project_data)

        if 'publish' in request.form:
            publish = datetime.datetime.now()
            p.datetime_published = publish

        # this will be handled by tag call
        tags = request.form['tags']
        # split only if key exists
        if tags:
            tags = tags.split(',')
            pt = ProjectTag()
            for tag in tags:
                tag = tag.strip()
                pt.add_tag_to_project(p.project_id, tag)

        # this will be handled by another class
        screenshots = request.form['screenshots']
        # split only if key exists
        if screenshots:
            screenshots = screenshots.split(',')

        p.create_project()

        return redirect(url_for('projects.get_projects'))


@project_blueprint.route('/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    if request.method == 'GET':
        p = Project()
        project = p.get_project(project_id)
        return render_template('projects/edit_project.html', project=project)
    if request.method == 'POST':
        project_data = request.form.to_dict()
        # add the porject_id to the dict
        project_data['project_id'] = project_id
        # make a new Project object with the dict data
        p = Project(project_data)

        if 'publish' in request.form:
            publish = datetime.datetime.now()
            p.datetime_published = publish

        # update the data in the db
        p.update_project()

        if request.form['tags']:
            tags = request.form['tags']
            tags_data = tags.split(',')
            pt = ProjectTag()
            pt.add_tags_to_project(p.project_id, tags_data)

        if p.get_project(p.project_id):
            return redirect(url_for('projects.edit_project', project_id=p.project_id))
        else:
            return 'Oh no something went wrong :(', 404

        return redirect(url_for('projects.get_project', project_id=project_id))

    return 'hello from edit project {}'.format(project_id)


@project_blueprint.route('/delete/<int:project_id>', methods=['GET', 'POST'])
@login_required
def delete_project(project_id):
    p = Project()
    p.remove_project(project_id)
    print(p)
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
    print('GETTING HERE?\n')
    p = Project()
    p.purge_deleted_projects()
    return redirect(url_for('projects.get_projects'))


@project_blueprint.route('/restore/<int:project_id>', methods=['GET'])
@login_required
def restore_deleted_projects(project_id):
    p = Project()
    p.restore_project(project_id)
    return redirect(url_for('projects.get_projects'))


@project_blueprint.route('/<string:tag_name>', methods=['GET'])
def get_project_by_tag(tag_name):
    t = ProjectTag()
    projects = t.get_entity_by_tag('project', tag_name)

    print(projects)

    return render_template('projects/projects.html', projects=projects), 200
