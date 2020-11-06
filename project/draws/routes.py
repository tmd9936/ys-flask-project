from . import *

@draw_blueprint.route("/")
def draw_render():
    return render_template('draw/draw.html', title="그림판")