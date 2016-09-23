# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from __future__ import print_function  # Use print() instead of print
from flask import url_for

import random
import string

char_set = string.ascii_uppercase + string.digits

def test_page_urls(client):
    # Visit home page
    response = client.get('/')
    assert b'Projects list' in response.data

    # Test login redirect
    response = client.get('/login')
    assert b'You should be redirected automatically to target URL' in response.data

    # Login
    response = client.post(url_for('user.login'), follow_redirects=True,
                           data=dict(username='foo', password='Foo123'))
    assert b'You have signed in successfully' in response.data

    # Get user profile page
    response = client.get(url_for('profile'))
    assert b'Hi foo' in response.data

    # Get page for new()
    response = client.get(url_for('new'))
    assert b'Create new project' in response.data

    # Create a new project
    new_project_name = ''.join(random.sample(char_set, 20))
    response = client.post(url_for('new'), follow_redirects=True,
                           data=dict(project=new_project_name))
    assert new_project_name in response.data

    # Check that project is there
    response = client.get(url_for('projects'))
    assert new_project_name in response.data

    # Visit new project
    response = client.get(url_for('branches',
                                  project=new_project_name))
    assert 'master' in response.data

    # Visit index page in master branch of project
    response = client.get(url_for('view',
                                  project=new_project_name,
                                  branch='master',
                                  filename='index'))
    assert 'Welcome' in response.data

    # View edit page for index in master branch
    response = client.get(url_for('edit',
                                  project=new_project_name,
                                  branch='master',
                                  filename='index'))
    assert 'Math mode' in response.data

    # Save index page in master branch
    response = client.post(url_for('save',
                                   project=new_project_name,
                                   branch='master',
                                   filename='index'),
                           follow_redirects=True,
                           data=dict(code='Title of test page\n=================='))
    assert b'Title of test page' in response.data

    # Logout
    response = client.get(url_for('user.logout'), follow_redirects=True)
    assert b'You have signed out successfully.' in response.data

    # Login as collaborator
    response = client.post(url_for('user.login'), follow_redirects=True,
                           data=dict(username='bar', password='Bar123'))
    assert b'You have signed in successfully' in response.data

    # Visit index page in master branch of project
    response = client.get(url_for('view',
                                  project=new_project_name,
                                  branch='master',
                                  filename='index'))
    assert 'Title of test page' in response.data

    # Attempt to edit unauthorized page
    response = client.get(url_for('edit',
                                  project=new_project_name,
                                  branch='master',
                                  filename='index'), follow_redirects=True)
    assert 'You are not the owner of this branch' in response.data

    # Save index page in master branch
    response = client.post(url_for('clone',
                                   project=new_project_name,
                                   branch='master'),
                           follow_redirects=True,
                           data=dict(name='feature'))
    assert b'Project cloned successfuly!' in response.data

    # Save a change to index page in feature branch
    response = client.post(url_for('save',
                                   project=new_project_name,
                                   branch='feature',
                                   filename='index'),
                           follow_redirects=True,
                           data=dict(code='Title of test page\n==================\n\nSome contents...'))
    assert b'Page submitted to _master' in response.data

    # Log as project creator again
    response = client.get(url_for('user.logout'), follow_redirects=True)
    assert b'You have signed out successfully.' in response.data
    response = client.post(url_for('user.login'), follow_redirects=True,
                           data=dict(username='foo', password='Foo123'))
    assert b'You have signed in successfully' in response.data

    # Visit merge page
    response = client.get(url_for('merge',
                                  project=new_project_name,
                                  branch='master',
                                  other='feature'))
    assert 'Merging from _feature' in response.data

    # Accepting suggestions
    response = client.get(url_for('accept',
                                  project=new_project_name,
                                  branch='master',
                                  filename='index.rst'), follow_redirects=True)
    assert 'You have finished all the reviews' in response.data

    # Finishing merge
    response = client.get(url_for('finish',
                                  project=new_project_name,
                                  branch='master'), follow_redirects=True)
    assert 'You have finished merging _feature' in response.data
    assert 'Some contents' in response.data

