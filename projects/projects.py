import os
import sys
import datetime

try:
    """
    Running as flask app.
    """
    from common.utils import get_id
    from common.db_interface import Database
    from tag.tag import Tag
except Exception as e:
    """
    Running as module.
    """
    print('\nproject running as a module, for testing\n')
    print('project.py import problem ', e)
    # adding the root directory of the projects
    print(os.getcwd(), '\n')
    sys.path.append(os.getcwd())
    print('added to path ', sys.path)
    from common.utils import get_id
    from common.db_interface import Database


class Project(object):
    def __init__(self, *args, **kwargs):
        # print(args, '\nkwargs\n', kwargs)

        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            # print('key', key)
            setattr(self, key, kwargs[key])
        # access to the db
        self.db = Database()

        # really not ideal but i need some deault values beyond just None for a lot of these

        # i could make this a loop with setdefault, but I would still need a list of keys i expect in the object and i don't mind it being explicit, it doesn't quite work for the first two either
        if 'project_id' not in self.__dict__:
            # print('No project_id, so adding it')
            self.project_id = get_id()

        if 'username' not in self.__dict__:
            # print('No username, so adding it')
            self.username = 'a'

        if 'title' not in self.__dict__:
            # print('No title, so adding it')
            self.title = None

        if 'description' not in self.__dict__:
            # print('No content, so adding it')
            self.description = None

        if 'git_link' not in self.__dict__:
            # print('No content, so adding it')
            self.git_link = None
        # there may not be a git version of some projects

        elif self.__dict__['git_link'] is not None and len(self.__dict__['git_link']) == 0:
            self.git_link = None

        if 'live_link' not in self.__dict__:
            # print('No content, so adding it')
            self.live_link = None
        # there may not be a live version of some projects
        elif self.__dict__['live_link'] is not None and len(self.__dict__['live_link']) == 0:
            self.live_link = None

        if 'datetime_started' not in self.__dict__:
            # print('No datetime_posted, so adding it')
            self.datetime_started = None

        if 'datetime_finished' not in self.__dict__:
            # print('No datetime_published, so adding it')
            self.datetime_finished = None

        if 'datetime_updated' not in self.__dict__:
            # print('No datetime_published, so adding it')
            self.datetime_updated = None

        if 'datetime_published' not in self.__dict__:
            # print('No datetime_published, so adding it')
            self.datetime_published = None

    def __repr__(self):
        pass

    def __str__(self):
        return '''
        A project: \n
        project_id: {}\n
        username: {}\n
        title: {}\n
        description: {}\n
        git_link: {}\n
        live_link: {}\n
        datetime_started: {}\n
        datetime_finished: {}\n
        datetime_updated: {}\n
        datetime_published: {}\n
        '''.format(
            self.project_id,
            self.username,
            self.title,
            self.description,
            self.git_link,
            self.live_link,
            self.datetime_started,
            self.datetime_finished,
            self.datetime_updated,
            self.datetime_published
        )

    def create_project(self):
        query_string = '''
                INSERT INTO project (project_id, username, title, description, git_link, live_link, datetime_started, datetime_finished, datetime_updated, datetime_published)
                VALUES (?,?,?,?,?,?,?,?,?,?)
                '''

        data = (
            self.project_id,
            self.username,
            self.title,
            self.description,
            self.git_link,
            self.live_link,
            self.datetime_started,
            self.datetime_finished,
            self.datetime_updated,
            self.datetime_published
        )

        self.db.make_sanitized_query(query_string, data)

    def get_projects(self):
        return self.db.get_query_as_list(
            '''
            SELECT * FROM project ORDER BY datetime_started DESC
            '''
        )

    def get_project(self, project_id):
        return self.db.get_query_as_list(
            '''
            SELECT * FROM project WHERE project_id = {}
            '''.format(project_id)
        )

    def save_deleted_project(self):
        query_string = '''
                INSERT INTO deleted_project (project_id, username, title, description, git_link, live_link, datetime_started, datetime_finished, datetime_updated, datetime_published)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            '''

        data = (
            self.project_id,
            self.username,
            self.title,
            self.description,
            self.git_link,
            self.live_link,
            self.datetime_started,
            self.datetime_finished,
            self.datetime_updated,
            self.datetime_published
        )

        self.db.make_sanitized_query(query_string, data)

    def remove_project(self, project_id):
        project_data = self.get_project(project_id)

        if project_data:
            p = Project(project_data[0])
            p.save_deleted_project()

            self.db.make_query(
                '''
                DELETE FROM project WHERE project_id = {};
                '''.format(project_id)
            )

            if self.get_project(project_id):
                return True

        return False

    def restore_project(self, project_id):
        # gets the project data
        project = self.get_deleted_project(project_id)
        # make a new project object
        if project:
            project = project[0]
            # New instance of project using the data from the deleted_project
            project_to_restore = Project(project)
            # write the project to the project table
            project_to_restore.create_project()
            # remove the project from deleted project table
            project_to_restore.remove_deleted_project(project_id)

    def get_deleted_projects(self):
        data = self.db.get_query_as_list(
            '''
            SELECT * FROM deleted_project ORDER BY datetime_published DESC
            '''
        )

        # data = self.db.get_rows('post')
        return data

    def get_deleted_project(self, project_id):
        data = self.db.get_query_as_list(
            '''
            SELECT * FROM deleted_project WHERE project_id = {}
            '''.format(project_id)
        )

        # data = self.db.get_rows('project')
        return data

    def remove_deleted_project(self, project_id):
        """
        Remove a post from deleted_post table and check that it is gone.
        """
        self.db.make_query(
            '''
            DELETE FROM deleted_project WHERE project_id = "{}";
            '''.format(project_id)
        )

        if self.get_deleted_project(project_id):
            return False

        return True

    def purge_deleted_projects(self):
        self.db.make_query(
            '''
            DELETE FROM deleted_project
            '''
        )

        if self.get_deleted_projects():
            return False
        return True

    def get_and_set_project(self, project_id):
        data = self.get_project(project_id)
        print(data[0])
        if data:
            # p = Project(data[0])
            # print(p)

            return Project(data[0])

    def update_project(self, project_id):
        """
        project_id shouldn't change.
        """
        if self.get_project(project_id):
            query_string = '''
                UPDATE project
                SET title = ?, description = ?, git_link = ?, live_link = ?, datetime_started =?, datetime_finished = ?, datetime_updated = ?, datetime_published = ?
                WHERE project_id = ?
                '''

            data = (
                self.title,
                self.description,
                self.git_link,
                self.live_link,
                self.datetime_started,
                self.datetime_finished,
                self.datetime_updated,
                self.datetime_published,
                self.project_id
            )

            self.db.make_sanitized_query(query_string, data)

            return True
        else:
            return False


if __name__ == "__main__":
    p = Project()

    # print(p)
    print(p.get_and_set_project(7651738052))
    # p.create_project()

    # print(p.get_projects())

    # print(p.get_project(2031595445))
