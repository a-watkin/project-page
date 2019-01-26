import os
import sys
import datetime

from flask import Blueprint, jsonify, request, render_template, redirect, url_for
# for markdown
import mistune


try:
    from .srojects.Project import Project
    from .project.project_tag import ProjectTag
    from .common.utils import login_required
except Exception as e:
    print('post routes import error', print(sys.path))
    print('\n', os.getcwd(), '\n')
    from projects.projects import Project
    from common.utils import login_required
    from projects.project_tag import ProjectTag

project_tag_blueprint = Blueprint('project_tag', __name__)
user_blueprint = Blueprint('user', __name__)


@project_tag_blueprint.route('/', methods=['GET'])
def get_all_tags():

    pt = ProjectTag()
    pt.remove_orphaned_tags()
    tags = pt.get_all_tags()

    print(tags)

    return render_template('projects/tags.html', tags=tags), 200
