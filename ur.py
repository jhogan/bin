import urwid.curses_display
import urwid

ui = urwid.curses_display.Screen()

def run():
        cols, rows = ui.get_cols_rows()
        txtFName = urwid.Edit("First: ")
        txtLName = urwid.Edit("Last: ")
        fill = urwid.Filler(txtName)
        reply = None
        while True:
                canvas = fill.render( (cols, rows), focus=True )
                ui.draw_screen( (cols, rows), canvas )

                keys = ui.get_input()
                for k in keys:
                        if k == "window resize":
                                cols, rows = ui.get_cols_rows()
                                continue
                        if reply is not None:
                                return
                        if k == "enter":
                                return True
                        if fill.selectable():
                                fill.keypress( (cols, rows), k )

ui.run_wrapper( run )

