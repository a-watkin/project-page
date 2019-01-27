

import os
import sys

try:
    from .password_util import PasswordUtil
except Exception as e:
    print('import problem, ', e)
    sys.path.append(os.getcwd())
    from common.db_interface import Database
    from common.password_util import PasswordUtil


class User(object):
    def __init__(self, username, password=None, user_id=None):
        self.username = username
        self.user_id = '9604217@N03'
        self.password = password
        # init database
        self.db = Database()

    # check if username exists

    def __str__(self):
        return """
        A user: \n
        username: {}\n
        user_id: {}\n
        password: {}\n
        using db: {}\n
        """.format(
            self.username,
            self.user_id,
            self.password,
            self.db.db_name
        )

    def check_for_username(self):
        """
        Checks if the username is in the database.
        """
        db_resp = self.db.get_row('user', 'username', self.username)
        if db_resp is None:
            return False
        return True

    def get_hashed_password(self, username):
        """
        Returns the hashed password from the database for the given username.
        """
        db_resp = self.db.get_row('user', 'username', self.username)

        print(db_resp)
        if db_resp:
            return db_resp[0]['hash_value']
        # changed here because the db no longer returns a tuple
        # return db_resp[2]

    def insert_hased_password(self, password):
        """
        Inserts hashed password into the database.

        Replaces password if already there.
        """
        # get hashed version
        hased_password = PasswordUtil.hash_password(password)
        self.db.make_query(
            '''
            UPDATE user 
            SET hash_value = "{}"
            WHERE username = "{}"
            '''.format(hased_password, self.username)
        )
        # print(hased_password)

    def check_password(self):
        hashed_password = self.get_hashed_password(self.username)
        return PasswordUtil.check_hashed_password(self.password, hashed_password)

    def insert_user(self):
        """
        Can only run once per user as is.
        """
        self.db.make_query(
            '''
            INSERT INTO user (username, user_id)
            VALUES ("{}", "{}")
            '''.format(self.username, self.user_id)
        )

        self.insert_hased_password(self.password)


def main():
    u = User('a', 'a')
    print(u)
    # hased password has been inserted
    # print(u.get_hashed_password('a'))

    # print(u.check_password())

    u.insert_user()
    # u.insert_hased_password(u.password)


if __name__ == '__main__':
    main()
