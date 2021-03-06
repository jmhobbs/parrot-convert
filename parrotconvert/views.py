# -*- coding: utf-8 -*-

from flask import request, render_template, send_from_directory, abort

from PIL import Image
import aalib

from util import is_allowed_file, multiple_replace


def register_views(app):

    #####################################################
    # Util and static. Override these in nginx where possible.

    @app.route('/robots.txt')
    @app.route('/humans.txt')
    def root_level_static_files():
        return send_from_directory(app.static_folder, request.path[1:])

    #####################################################
    # App!
    @app.route('/', methods=('GET', 'POST'))
    def index():
        if request.method == 'POST':
            file = request.files.get('file')
            if not file:
                abort(400)
            elif not is_allowed_file(file.filename):
                abort(400)

            screen = aalib.AsciiScreen(width=20, height=20)
            image = Image.open(file).convert('L').resize(screen.virtual_size)
            screen.put_image((0, 0), image)
            rendered = screen.render()

            used = {}

            for i in xrange(0, len(rendered)):
                if rendered[i] != " ":
                    if rendered[i] not in used:
                        used[rendered[i]] = 0
                    else:
                        used[rendered[i]] += 1

            used = sorted(used.items(), key=lambda x: x[1], reverse=True)

            # Sometimes white backgrounds get dominant, ignore them
            if used[0][1] > rendered.count(" "):
                rendered = rendered.replace(used[0][0], " ")
                used = used[1:]

            replace_map = []

            row_number = 0
            for row in used:
                if row_number == 0:
                    replace_map.append((row[0], ':pt:'))
                elif row_number == 1:
                    replace_map.append((row[0], ':mp:'))
                elif row_number == 2:
                    replace_map.append((row[0], ':rp:'))
                elif row_number % 2 == 0:
                    replace_map.append((row[0], ':sp:'))
                else:
                    replace_map.append((row[0], ':otp:'))
                row_number += 1

            parrot_rendered = map(str.rstrip, map(lambda x: multiple_replace(x, *replace_map), rendered.split("\n")))

            # Remove blank lines
            for line in parrot_rendered:
                if len(line) == 0:
                    parrot_rendered.pop(0)
                else:
                    break
            for line in reversed(parrot_rendered):
                if len(line) == 0:
                    parrot_rendered.pop()
                else:
                    break

            parrot_rendered = "\n".join(parrot_rendered)
            parrot_rendered = parrot_rendered.replace(" ", ":ip:")

            html_parrots = parrot_rendered.replace(":ip:", '<img src="http://dropit.velvetcache.org.s3.amazonaws.com/jmhobbs/NTA50yFcIg/parrotspacer.png" />')
            html_parrots = html_parrots.replace(":pt:", '<img src="http://dropit.velvetcache.org.s3.amazonaws.com/jmhobbs/NTAx6Ctp7A/parrot.gif" />')
            html_parrots = html_parrots.replace(":rp:", '<img src="http://dropit.velvetcache.org.s3.amazonaws.com/jmhobbs/NTA1X9dfUg/rightparrot.gif" />')
            html_parrots = html_parrots.replace(":sp:", '<img src="http://dropit.velvetcache.org.s3.amazonaws.com/jmhobbs/NTA2n8Mr3A/shuffleparrot.gif" />')
            html_parrots = html_parrots.replace(":otp:", '<img src="http://dropit.velvetcache.org.s3.amazonaws.com/jmhobbs/NTA3F9M9JA/oldtimeyparrot.gif" />')
            html_parrots = html_parrots.replace(":mp:", '<img src="http://dropit.velvetcache.org.s3.amazonaws.com/jmhobbs/NTA4zPBpvA/middleparrot.gif" />')
            html_parrots = "<br/>".join(html_parrots.split("\n"))

            return render_template("index.html",
                                   slack_rendered=parrot_rendered,
                                   html_parrots=html_parrots
                                   )
        else:
            return render_template("index.html")

    @app.route("/about")
    def about():
        return render_template("about.html")
