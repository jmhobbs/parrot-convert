# -*- coding: utf-8 -*-

import os
import socket

from flask import Flask
from jinja2 import Markup
import markupsafe

from config import BaseConfig
from views import register_views

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

app.config.from_object(BaseConfig)
app.config.from_envvar('CONFIG', silent=True)

app.debug = app.config.get('DEBUG', False)

register_views(app)


@app.template_filter('render_parrots')
def render_parrots(s):
    if type(s) == Markup or type(s) == markupsafe.Markup:
        s = s.unescape()

    s = s.encode('utf8')

    s = s.replace(" ", '<img src="http://dropit.velvetcache.org.s3.amazonaws.com/jmhobbs/NTA50yFcIg/parrotspacer.png" />')
    s = s.replace(":parrot:", '<img src="http://dropit.velvetcache.org.s3.amazonaws.com/jmhobbs/NTAx6Ctp7A/parrot.gif" />')
    s = s.replace(":rightparrot:", '<img src="http://dropit.velvetcache.org.s3.amazonaws.com/jmhobbs/NTA1X9dfUg/rightparrot.gif" />')
    s = s.replace(":shuffleparrot:", '<img src="http://dropit.velvetcache.org.s3.amazonaws.com/jmhobbs/NTA2n8Mr3A/shuffleparrot.gif" />')
    s = s.replace(":oldtimeyparrot:", '<img src="http://dropit.velvetcache.org.s3.amazonaws.com/jmhobbs/NTA3F9M9JA/oldtimeyparrot.gif" />')
    s = s.replace(":middleparrot:", '<img src="http://dropit.velvetcache.org.s3.amazonaws.com/jmhobbs/NTA4zPBpvA/middleparrot.gif" />')

    return Markup("<br/>".join(s.split("\n")))


@app.context_processor
def inject_globals():
    return dict(
        g_ENVIRONMENT=app.config.get('ENV'),
        g_HOSTNAME=socket.gethostname(),
        g_IS_PRODUCTION=('PRODUCTION' == app.config.get('ENV')),
        g_SERVER_NAME=app.config.get('SERVER_NAME'),
        g_GOOGLE_ANALYTICS_ID=app.config.get('GOOGLE_ANALYTICS_ID')
    )


if __name__ == "__main__":
    app.run(debug=True)
