import ipywidgets as widgets
from IPython.display import display
from ipycanvas import Canvas
import numpy
import matplotlib.pyplot as plot


class Bear:
    def __init__(self, name="", length=0, colour="", power=""):
        self.name = name
        self.length = length
        self.colour = colour
        self.power = power

    def __str__(self):
        return f"A {self.power} {self.colour}-coloured bear named {self.name}, of length {self.length}m"


def create_bear():
    name = widgets.Text(description="Name")
    length = widgets.FloatText(description="Length")
    colour = widgets.ColorPicker(concise=True, description="Fur colour", value="brown")
    powers = ['very strong', 'very fast', 'very clever', 'thunder-summoning']
    power = widgets.RadioButtons(options=powers, description='Power')
    
    tabs = ["Basic", "Colour", "Power"]
    page1 = widgets.VBox([name, length])
    page2 = colour
    page3 = power
    tab = widgets.Tab()
    tab.children = [page1, page2, page3]
    for i in range(3):
        tab.set_title(i, tabs[i])
    button = widgets.Button(description='Save')
    panel = widgets.VBox([tab, button])

    out = widgets.Output()
    with out:
        display(panel)
    display(out)

    def on_button_click(_):
        out.clear_output()
        new_bear = Bear(name.value, length.value, colour.value, power.value)
        print(f"{new_bear} is created")

    button.on_click(on_button_click)


def greeting_roar():
    print("Roar! You've found me!")


drawing = False


def try_circle():
    canvas = Canvas(width=540, height=180)
    canvas_out = widgets.Output()
    plot_out = widgets.Output()
    box = widgets.HBox([canvas_out, plot_out])
    points = []

    def on_mouse_down(x, y):
        canvas.fill_style = "white"
        canvas.fill_rect(0, 0, 540, 180)
        canvas.fill_style = "#00c8ff"
        canvas.fill_arc(x, y, 5, 0, numpy.pi * 2, False)
        points.clear()
        global drawing
        drawing = True

    def on_mouse_move(x, y):
        global drawing
        if drawing:
            canvas.fill_style = "#00c8ff"
            canvas.fill_arc(x, y, 5, 0, numpy.pi * 2, False)
            points.append((x, y))
    
    def on_mouse_up(x, y):
        global drawing
        if drawing:
            point_xy = list(zip(*points))
            point_x = numpy.array(list(point_xy[0])) / 540 * 2 * numpy.pi
            point_y = numpy.array(list(point_xy[1]))
            point_y = (point_y - numpy.amin(point_y)) / (numpy.amax(point_y) - numpy.amin(point_y)) + 5
            drawing = False
            plot_out.clear_output()
            with plot_out:
                plot.polar(point_x, point_y)
                plot.show()

    canvas.on_mouse_down(on_mouse_down)
    canvas.on_mouse_move(on_mouse_move)
    canvas.on_mouse_up(on_mouse_up)
    canvas.on_mouse_out(on_mouse_up)
    with canvas_out:
        display(canvas)
    display(box)
