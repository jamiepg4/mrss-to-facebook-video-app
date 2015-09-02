MRSS To Facebook Video App
==========================

Upload videos to any Facebook entity (Page, Event, User, etc.) from a MRSS feed.

[![Build Status](https://travis-ci.org/fusioneng/mrss-to-facebook-video-app.svg)](https://travis-ci.org/fusioneng/mrss-to-facebook-video-app)

## Architecture

This app is primarily one script intended to be executed on the command line.

Optionally use Redis to capture the Facebook ID for a video guid, to prevent duplicate uploads.

## Setup

### Installing Python Dependencies

To run locally, make sure you have the [pip][pip] installed, the package manager for Python.

You will need to have Python 3 installed. This library has been tested with Python 3.4.3. On OSX you can install Python 3 via `brew install python3`. Most recent Linux distributions come with Python 3 pre-installed. You should be able to determine the path to your Python 3 executable via `whereis python3`.

You will need to set up a Python Virtual Environment:

```shell
# Make sure to use the correct path.
virtualenv --python=$(which python3) $HOME/.venv/mrss-to-facebook-video-app
source $HOME/.venv/mrss-to-facebook-video-app/bin/activate
```

Or you could use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/#introduction).

Once you've activated the virtual environment, you can install the Python dependencies.

```shell
# Install the requirements
pip install -r requirements.txt
```

### Setting up Environment Variables

See `.env.sample` for expected environment variables.

### Generating OAuth tokens

OAuth tokens are needed to authorize requests to Facebook. They are stored as environment variables as well.

First we need to generate the credentials:

```bash
$ mtfv oauth facebook_client_secrets.json facebook-creds.json publish_actions
```

This will open a browser window, asking you to approve the request, which you should.

## Running on Heroku

tk
