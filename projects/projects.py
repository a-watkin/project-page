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
    print('\npost running as a module, for testing\n')
    print('post.py import problem ', e)
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
        if 'project_id' not in self.__dict__:
            # print('No post_id, so adding it')
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

        if 'live_link' not in self.__dict__:
            # print('No content, so adding it')
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


if __name__ == "__main__":
    p = Project()

    print(p)
    # print(p.get_post(6558864814))