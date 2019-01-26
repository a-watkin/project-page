import sqlite3


def create_database(db_name):

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS user(
            username TEXT PRIMARY KEY UNIQUE NOT NULL,
            hash TEXT NULL
        );
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS post(
            post_id INT PRIMARY KEY UNIQUE NOT NULL,
            username TEXT NOT NULL,
            title TEXT,
            content TEXT,
            datetime_posted TEXT,
            datetime_published TEXT,
            FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE
        );
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS deleted_post(
            post_id INT PRIMARY KEY UNIQUE NOT NULL,
            username TEXT NOT NULL,
            title TEXT,
            content TEXT,
            datetime_posted TEXT,
            datetime_published TEXT,
            FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE
        );
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS tag(
            tag_name TEXT NOT NULL UNIQUE, 
            username TEXT NOT NULL,
            posts INT,
            photos INT,
            projects INT,
            PRIMARY KEY (tag_name, username)
            FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE
        );
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS post_tag(
            post_id INT references post(post_id) ON UPDATE CASCADE,
            tag_name TEXT references tag(tag_name) ON UPDATE CASCADE,
            PRIMARY KEY (post_id, tag_name)
        );
        '''
    )

    # PROJECTS
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS project(
            project_id INT PRIMARY KEY NOT NULL UNIQUE,
            username TEXT,
            title TEXT,
            description TEXT,
            git_link TEXT,
            live_link TEXT,
            datetime_started TEXT,
            datetime_finished TEXT,
            datetime_updated TEXT,
            datetime_published TEXT,
            FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE
        );
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS deleted_project(
            project_id INT PRIMARY KEY NOT NULL UNIQUE,
            username TEXT,
            title TEXT,
            description TEXT,
            git_link TEXT,
            live_link TEXT,
            datetime_started TEXT,
            datetime_finished TEXT,
            datetime_updated TEXT,
            datetime_published TEXT,
            FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE
        );
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS project_tag(
            project_id INT references project(project_id) ON UPDATE CASCADE,
            tag_name TEXT references tag(tag_name) ON UPDATE CASCADE,
            PRIMARY KEY (project_id, tag_name)
        );
        '''
    )


if __name__ == "__main__":
    # pass
    create_database('projects.db')
