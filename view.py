import tkinter as tk
from tkinter import ttk
from controller import Controller
import sqlalchemy.exc


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # create widgets
        # label
        self.label = ttk.Label(self, text='Email:')
        self.label.grid(row=1, column=0)
        self.label = ttk.Label(self, text='Password:')
        self.label.grid(row=2, column=0)

        # email entry
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(self, textvariable=self.email_var, width=30)
        self.email_entry.grid(row=1, column=1, sticky=tk.NSEW)

        # password entry
        self.pass_var = tk.StringVar()
        self.pass_entry = ttk.Entry(self, textvariable=self.pass_var, width=30)
        self.pass_entry.grid(row=2, column=1, sticky=tk.NSEW)

        # save button
        self.save_button = ttk.Button(self, text='Save', command=self.save_button_clicked)
        self.save_button.grid(row=3, column=1, padx=10)

        # message
        self.message_label = ttk.Label(self, text='', foreground='red')
        self.message_label.grid(row=4, column=0, columnspan=2, sticky=tk.W)

        # set the controller
        self.controller = None

    def set_controller(self, controller):
        # Set the controller
        self.controller = controller

    def save_button_clicked(self):
        # Handle button click event
        try:
            self.controller.save(self.email_var.get(), self.pass_var.get())
            self.show_success("Email saved")
        except sqlalchemy.exc.IntegrityError:
            raise self.show_error("Email already inputted")
        except ValueError:
            raise self.show_error("Invalid email/Empty password")

    def show_error(self, message):
        # Show an error message
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)
        self.email_entry['foreground'] = 'black'

    def show_success(self, message):
        # Show a success message
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000, self.hide_message)

        # reset the form
        self.email_entry['foreground'] = 'black'
        self.email_var.set('')
        self.pass_var.set('')

    def hide_message(self):
        # Hide the message
        self.message_label['text'] = ''


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Emails')

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller()

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()
