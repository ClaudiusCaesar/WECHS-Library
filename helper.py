import tkinter as tk

class Application(tk.Frame):
  def __init__(self, master = None):
    tk.Frame.__init__(self, master)
    self.current_widget_list = []
    self.currentframe = tk.Frame()
  def makehelp(self, text):
    self.destroywidgets()
    self.currentframe = tk.Frame()
    self.currentframe.grid(row = 0, column = 0)
    self.current_widget_list.append(tk.Button(self.currentframe, text = 'Back', command = self.helpbuttons))
    self.current_widget_list[-1].grid(row = 1, column = 0)
    self.current_widget_list.append(tk.Label(self.currentframe, text = text, justify = 'left', anchor = 'w'))
    self.current_widget_list[-1].grid(row = 0, column = 0)
  def destroywidgets(self):
    for widget in self.current_widget_list:
      widget.grid_forget()
      widget.destroy()
    self.currentframe.grid_forget
    self.currentframe.destroy()
    self.current_widget_list = []
  def helpbuttons(self):
    self.destroywidgets()
    self.current_widget_list.append(tk.Label(text = "For help with any of these\nactions, press one of these buttons.", anchor = 'w', justify = "left"))
    self.current_widget_list[-1].grid(row = 0, column = 0)
    self.current_widget_list.append(tk.Button(text = "Adding A Person", command = lambda: self.makehelp("To add a person, click the menu button to open the dropdown, and click the 'New Person' option.\nThis will open a form on the left side of the application.\nSimply enter the name of the person being added, and choose a type for that person.\nThen press the Add button.\nThis will show the list of people on the right, now with the new person on the bottom of the list.")))
    self.current_widget_list[-1].grid(row = 1, column = 0)
    self.current_widget_list.append(tk.Button(text = "Adding A Book", command = lambda: self.makehelp("To add a book, click the menu button to open the dropdown, and click the 'New Book' option.\nThis will open a form on the left side of the application.\nSimply enter the information of the book into the text boxes.\nIn the Location box enter the preferred place of refernce, such as a dewey decimal number, or shortened author name.\nThen press the add button\nThis will open a list of books on the right, with the new book now at the bottom.")))
    self.current_widget_list[-1].grid(row = 2, column = 0)
    self.current_widget_list.append(tk.Button(text = "Editing", command = lambda: self.makehelp("To edit a book or person, click on the menu button, and press the 'Show Book' or 'Show People' buttons, respectively.\nThen press the 'Edit' button, which will open a form on the left side of the screen.\nChange the text in the textboxes, and/or choose a type, and press the 'Change' button to change data for the item.")))
    self.current_widget_list[-1].grid(row = 3, column = 0)
    self.current_widget_list.append(tk.Button(text = "Deleting", command = lambda: self.makehelp("To delete a book or person, click on the menu button, and press the 'Show Book' or 'Show People' buttons, respectively.\nThen press the delete button on the item you would like to delete.")))
    self.current_widget_list[-1].grid(row = 4, column = 0)
    self.current_widget_list.append(tk.Button(text = "Viewing", command = lambda: self.makehelp("To view the information of a book or person, press the menu button, and click the 'Show Book' or 'Show People' buttons, respectively.\nNow press the view button next to the item you would like to view.")))
    self.current_widget_list[-1].grid(row = 5, column = 0)
    self.current_widget_list.append(tk.Button(text = "Checking Out", command = lambda: self.makehelp("To check out a book, open the book list from the menu, and press view on the book you would like to check out.\nIf you cannot find it directly, enter its name or id in the search box and press enter.\nAfter pressing view, if the book is checked into the library, you will see a button saying 'Check Out'.\nPress that button, and in the text box that appears below enter the name or id of the person you would like ot check the book out to.\nIf you entered the name/id of the person incorrectly, or a person with the information you entered does not exist, a piece of text will appear below the text box, saying that this is the case.")))
    self.current_widget_list[-1].grid(row = 6, column = 0)
    self.current_widget_list.append(tk.Button(text = "Checking In", command = lambda: self.makehelp("To check in a book, open the book list from the menu, and press view on the book you would like to check out.\nIf you cannot find the book directly, enter its name or id in the search box and press enter.\nAfter pressing view, if the book is currently checked out, you will see a button saying 'Check In'.\nPress that button, and the book will now be checked in.")))
    self.current_widget_list[-1].grid(row = 7, column = 0)
    self.current_widget_list.append(tk.Button(text = "Creating A Printout", command = lambda: self.makehelp("To create a printout, press the menu button, and in the list that appears, press the 'Make File' button.\nThe application window will now show a copy of the report that will be printed.\nPress the print button, and the report will be printed.*\n*The file will be printed on the default printer of the machine you have run the program on, so make sure the default printer is the one you prefer.")))
    self.current_widget_list[-1].grid(row = 8, column = 0)
help_app = Application()
help_app.master.title("Help Window")
help_app.helpbuttons()
help_app.mainloop()
