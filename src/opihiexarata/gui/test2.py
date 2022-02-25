if __name__ == "__main__":
    import PySimpleGUIQt as sg

    sg.theme("DarkAmber")  # Add a little color to your windows
    # All the stuff inside your window. This is the PSG magic code compactor...
    layout = [
        [sg.Text("Some text on Row 1")],
        [sg.Text("Enter something on Row 2"), sg.InputText(key="-input-")],
        [sg.Button("Dome"), sg.Text("On", key="-dome-"), sg.Button("More")],
        [sg.Graph((200, 200), (0, 0), (200, 200), enable_events=True, key="-grid-")],
        [sg.OK(), sg.Cancel()],
    ]

    # Create the Window
    window = sg.Window("Window Title", layout, finalize=True)

    graph = window["-grid-"]
    # graph.bind('<Button-3>', '+RIGHT+')

    dome_state = True
    true_timeout = None
    # Event Loop to process "events"
    while True:
        event, values = window.read(timeout=1000)
        print(event, "=", values)
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        if event in "Dome":
            dome_state = not dome_state
            if dome_state:
                window["-dome-"].update(background_color="blue")
            else:
                window["-dome-"].update(background_color="red")
        if event in "More":
            sg.popup("Annoy")
        if event in "-grid-":
            print(3)
        print("running")

    window.close()

    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    class Annotate(object):
        def __init__(self):
            self.ax = plt.gca()
            self.rect = Rectangle((0, 0), 1, 1)
            self.x0 = None
            self.y0 = None
            self.x1 = None
            self.y1 = None
            self.ax.add_patch(self.rect)
            self.ax.figure.canvas.mpl_connect("button_press_event", self.on_press)
            self.ax.figure.canvas.mpl_connect("button_release_event", self.on_release)

        def on_press(self, event):
            print("press")
            self.x0 = event.xdata
            self.y0 = event.ydata

        def on_release(self, event):
            print("release")
            self.x1 = event.xdata
            self.y1 = event.ydata
            self.rect.set_width(self.x1 - self.x0)
            self.rect.set_height(self.y1 - self.y0)
            self.rect.set_xy((self.x0, self.y0))
            self.ax.figure.canvas.draw()

    a = Annotate()
    plt.show()
    print(a.x0, a.x1)
