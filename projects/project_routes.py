from flask import Blueprint, jsonify, request, render_template, redirect, url_for


project_blueprint = Blueprint('posts', __name__)


@project_blueprint.route('/', methods=['GET'])
def test():
    return 'meh'
