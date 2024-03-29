#!/usr/bin/env python

import os
import sys
import time
import sqlite3
from time import strftime, gmtime


DATABASE = os.path.join(os.getenv('HOME'), 'Dropbox', '.timecard.db')


def table_exists(c):
    '''Check if projects table exists'''

    tables = c.execute("select name from sqlite_master "
                       "where type='table'").fetchall()

    tables = [x[0] for x in tables]

    return 'projects' in tables


def create_table(c):
    '''Create projects table'''
    c.execute("create table projects (project text, action text, date float)")


def last_project(c):
    p = c.execute("select project from projects order by date").fetchall()
    if len(p) == 0:
        return ""
    else:
        return p[-1][0]


def last_action(c):
    p = c.execute("select action from projects order by date").fetchall()
    if len(p) == 0:
        return ""
    else:
        return p[-1][0]


def log_action(c, project, action, action_time):
    c.execute("insert into projects values ('{project}', '{action}', '{time}')".format(project=project, action=action, time=action_time))
    print "Project '{project}' {action} at {date}".format(project=project, action=action, date=strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime(action_time)))


def error(message):
    print message
    sys.exit(2)


def usage():
    print "Usage: tc start/stop project"
    sys.exit(0)

if __name__ == "__main__":

    # Connect to database
    conn = sqlite3.connect(DATABASE)

    # Get cursor
    c = conn.cursor()

    # Check if table exists, create if not
    if not table_exists(c):
        create_table(c)

    # Find action and project from command-line
    if len(sys.argv) >= 2:
        action = sys.argv[1]
    else:
        usage()

    if action in ['start', 'stop']:

        # Find project to start/stop
        if len(sys.argv) == 3:
            project = sys.argv[2]
        else:
            usage()

        if action == 'start':

            # Need to check previous project was stopped
            if last_action(c) == 'stopped' or last_project(c) == "":
                log_action(c, project, 'started', time.time())
                conn.commit()
            else:
                if last_project(c) == project:
                    error("Project '{}' has already been started".format(project))
                else:
                    error("Previous project '{}' has not been stopped".format(last_project(c)))

        else:

            # Need to check project was started
            if last_project(c) == project:
                if last_action(c) == 'started':
                    log_action(c, project, 'stopped', time.time())
                    conn.commit()
                else:
                    error("Project '{}' has already been stopped".format(project))
            else:
                error("Project '{}' has not been started".format(project))

    else:
        usage()

    # Close cursor
    c.close()
