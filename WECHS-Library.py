import tkinter as tk #GUI Package
import math #used for the abs() function, and others

import time #Used for dates and fines
import datetime
from datetime import date #Held over from earlier versions, and unchanged for simplicity

import pickle #Package for saving data
import os #Allows interfacing with the computer, mainly for printing
PickledPeople = 'PickledPeople.pk1' #References used for the pickling process
PickledBooks = 'PickledBooks.pk1'
PickledId = 'singlevalue.pk1'
book_list = [] # Holds the main data objects
person_list = []
today = datetime.datetime.today() #Used for updating histories when checking out
todaystring = today.strftime('%m/%d/%Y')
idvalue = [0, 0] #Saves id's when making new ones
fwidgetlist = [] #Used for the makefile widgets
def fine_calculation(): #Calculates Fines
  for aperson in person_list:
    aperson.fines = 0 + aperson.heldfines
    for books in aperson.booksout:
      for abook in book_list:
        if abook.id == books[0].id:
          day = datetime.datetime.strptime(abook.datehis[-1], "%m/%d/%Y")
          daysout = (today-day).days
          if daysout > 0:
            if aperson.type == "Student":
              if daysout > 14:
                aperson.fines = float(aperson.fines) + math.ceil(((daysout - 14)*.20)*100)/100 + aperson.heldfines
            elif aperson.type == "Teacher":
              if daysout > 30:
                aperson.fines= float(aperson.fines) + math.ceil(((daysout - 30)*.20)*100)/100 + aperson.heldfines
      if aperson.fines != 0:
        if (float(aperson.fines)*100)%10 == 0:
          aperson.fines =str(aperson.fines) + '0'
    aperson.fines = '$'+str(aperson.fines)
    pickle_all()
def pickledump(list1, file): #Updates a pickle file with a list
  with open(file, 'wb') as op:
    pickle.dump(list1, op, pickle.HIGHEST_PROTOCOL)
def strip(string): #Strips of string of spaces and makes it lower case for searching
  string = string.lower()
  return string.replace(" ", "")
def pickle_all(): #Pickles all
  pickledump(person_list, PickledPeople)
  pickledump(book_list, PickledBooks)
  pickledump(idvalue, PickledId)
def newdatap(x, z, a): #Adds to their specific lists, and was easier to code with two functions
    person_list.append(person(x, idvalue[0], z, a))
    pickle_all()
    app.gridpersonlist()
def newdatab(x, z, a, b):
    book_list.append(book(x, idvalue[1], z, a, b))
    pickle_all()
    app.gridbooklist()
def makefinefile(thefile): #Creates the fine data for the report
  lengthtest = person_list[0].name
  times = True
  finelist = []
  for aperson in person_list:
    if len(aperson.name) > len(lengthtest):
      lengthtest = aperson.name
  length = len(lengthtest)
  for aperson in person_list:
    if times == True:
      top1 = "Name"
      top2 = "Fines"
      top3 = top1.center(length, " ") + "  " + top2.center(6, " ") + "\n"
      finelist.append(["Names", 'Fines'])
      thefile.write(top3)
      times = False
    if aperson.fines != "$0":
      towrite = aperson.name.center(length, " ") + "  " + aperson.fines.center(6, " ") + '\n'
      finelist.append([aperson.name, aperson.fines])
      thefile.write(towrite)
  for num in range(3):
    thefile.write("\n")
  return(finelist)
def makedatesfile(thefile): #Creates the due date data for the report
  lengthtest = ""
  lengthtest2 = ""
  times = True
  datelist = []
  lastperson = "placeholder"
  towrite = "placeholderagain"
  for aperson in person_list:
    if len(aperson.name) > len(lengthtest):
      lengthtest = aperson.name
  for abook in book_list:
    if len(abook.name) > len(lengthtest2):
      lengthtest2 = abook.name
  length = len(lengthtest)
  length2 = len(lengthtest2)
  for aperson in person_list:
    for abooklist in aperson.booksout:
      if times == True:
        top1 = "Name"
        top2 = "Book"
        top3 = "Due Back"
        top4 = "Days Out"
        top5 = top1.center(length) + "  " + top2.center(length2) + "  " + top3.center(12) + "  " + top4.center(9)+ "\n"
        top6 = []
        top6.append(top1)
        top6.append(top2)
        top6.append(top3)
        top6.append(top4)
        datelist.append(top6)
        thefile.write(top5)
        times = False
      towrite = aperson.name.center(length, " ")
      daysout = datetime.datetime.strptime(abooklist[1], "%m/%d/%Y") - today
      daysout = daysout.days + 1
      if daysout >= 0:
          daysout1 = str(daysout) + " Days Until Due"
      elif daysout < 0:
        if daysout == -1:
          daysout1 = str(abs(daysout)) + " Day Late"
        else:
          daysout1 = str(abs(daysout)) + " Days Late"
      towrite1 = []
      towrite1.append(towrite)
      towrite = towrite + "  " + (abooklist[0].name).center(length2) + "  " + (abooklist[1].center(10)) + "  " + str(daysout1) + '\n'
      towrite1.append(abooklist[0].name)
      towrite1.append(abooklist[1])
      towrite1.append(str(daysout1))
      datelist.append(towrite1)
      thefile.write(towrite)
  return(datelist)
def makefile(): #Actually makes the report.txt
  global fwidgetlist
  for widget in fwidgetlist:
    widget.grid_forget()
    widget.destroy()
  fwidgetlist = []
  os.remove("Report.txt")
  thefile = open("Report.txt", "w+")
  finelist = makefinefile(thefile)
  datelist = makedatesfile(thefile)
  thefile.close()
  rowval = -1
  app.forgetall()
  app.printframe.grid(row = 1, column = 0)
  for textlist in finelist:
    rowval+=1
    columnval = 0
    for widget in textlist:
      fwidgetlist.append(tk.Label(app.printframe, text = str(widget), anchor = 'w'))
      fwidgetlist[-1].grid(row = rowval, column = columnval, sticky = "W")
      columnval+=1
  rowval+=3
  for textlist in datelist:
    columnval = 0
    rowval+=1
    for widget in textlist:
      fwidgetlist.append(tk.Label(app.printframe, text = str(widget), anchor = 'w'))
      fwidgetlist[-1].grid(row = rowval, column = columnval, sticky = "W")
      columnval+=1
  rowval+=1
  fwidgetlist.append(tk.Button(app.printframe, text = "Close", command = app.forgetall))
  fwidgetlist[-1].grid(row = rowval, column = 1)
  fwidgetlist.append(tk.Button(app.printframe, text = "Print", command = lambda: os.startfile("Report.txt", "print")))
  fwidgetlist[-1].grid(row = rowval, column = 0)
  app.NextDay.grid_forget()
  app.searchtext.grid_forget()
def deleteperson(num):
  del person_list[person_list.index(num)]
  pickle_all()
  app.Create_PersonList(person_list)
def deletebook(num):
  del book_list[book_list.index(num)]
  pickle_all()
  app.Create_BookList(book_list)
def NewDay(test, object1 = "nevermind"): #Changes today variable to the next day
  global today
  today += datetime.timedelta(days=1)
  global todaystring
  todaystring = today.strftime('%m/%d/%Y')
  fine_calculation()
  app.todaytkstring.set(todaystring)
  if test == 1:
    app.Create_BookList(book_list)
  elif test == 0:
    app.Create_PersonList(person_list)
  elif test == 2:
    for aperson in person_list:
      if aperson.id == object1.id:
        aperson.viewperson()
  elif test == 3:
    for abook in book_list:
      if abook.id == object1.id:
        abook.viewbook()
class Application(tk.Frame): #Used as an easy place to hold functions
  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.grid()
    self.bwidgetlist = [] #All widget lists are used to create and destroy widgets
    self.pwidgetlist = [] #These two are for people and books, p and b
    self.mb = tk.Menubutton(self, text = 'Menu')
    self.mb.grid(row = 0, column = 0, sticky = 'NW')
    self.mb.menu = tk.Menu(self.mb)
    self.mb['menu'] = self.mb.menu
    self.mb.menu.add_command(label = 'New Person', command = self.PersonFC)
    self.mb.menu.add_command(label = 'New Book', command = self.BookFC)
    self.mb.menu.add_command(label = 'Show Books', command = self.gridbooklist)
    self.mb.menu.add_command(label = 'Show People', command = self.gridpersonlist)
    self.mb.menu.add_command(label = "Print Report", command = makefile)
    self.mb.menu.add_command(label = "Help", command = lambda: os.system("helper.py"))
    self.formframea = tk.Frame(self) # Two frames because re-gridding a frame causes
    self.formframeb = tk.Frame(self) # all widgets to re-appear, rather than a selection
    self.booksframe = tk.Frame(self)
    self.peopleframe = tk.Frame(self)
    self.viewframe = tk.Frame(self)
    self.extraviewframe = tk.Frame(self.viewframe)
    self.extralist = []
    self.labellist = []
    self.searchtext = tk.Label(self, text = "Search:")
    self.searchbox = tk.Entry(self)
    self.Add = tk.Button()
    self.NextDay = tk.Button() #Created so I can safely destroy at the beginning of each Create function
    self.todaytkstring = tk.StringVar()
    self.todaytkstring.set(todaystring)
    self.DateLabel = tk.Label(self, textvariable = self.todaytkstring)
    self.DateLabel.grid(row = 0, column = 5)
    self.printframe = tk.Frame()
    self.printlist = []
  def showprint(): #Gets the data from the make functions, and puts it in the application
    self.forgetall()
    for widget in self.printlist:
      widget.grid_forget()
      widget.destroy()
    self.printframe.grid(row = 1, column = 1)
    self.fineslist = makefinefile()
  def forgetall(self): #Clears the window
    self.printframe.grid_forget()
    self.NextDay.grid_forget
    self.searchbox.grid_forget()
    self.searchtext.grid_forget
    self.clearviewframe()
    self.formframea.grid_forget()
    self.formframeb.grid_forget()
    self.booksframe.grid_forget()
    self.peopleframe.grid_forget()
    self.printframe.grid_forget()
  def PersonFC(self): #Clears the screen for the person form
      self.formframeb.grid_forget()
      self.printframe.grid_forget()
      self.clearviewframe()
      self.NewPersonForm()
      self.Create_PersonList(person_list)
      self.booksframe.grid_forget()
      self.Add.bind("<Button-1>", self.NewPerson)
  def BookFC(self): #Clears the screen for the book form
      self.formframea.grid_forget()
      self.printframe.grid_forget()
      self.clearviewframe()
      self.NewBookForm()
      self.Create_BookList(book_list)
      self.peopleframe.grid_forget()
      self.Add.bind("<Button-1>", self.NewBook)
  def NewPersonForm(self): #Actually makes the forms
      self.Add.grid_forget()
      self.formframea.grid(row= 1, column = 0, sticky = "N")
      self.Name = tk.StringVar()
      self.Type = tk.StringVar()


      self.NameLabel = tk.Label(self.formframea, text = "Name:").grid(row = 1, column = 1)
      self.TypeLabel = tk.Label(self.formframea, text = "Type:").grid(row = 2, column = 1)

      self.NameEntry = tk.Entry(self.formframea, textvariable = self.Name)
      self.NameEntry.grid(row = 1, column = 2, columnspan = 2) #type entry checking found in realpedit
      self.TypeEntry1 = tk.Radiobutton(self.formframea, variable = self.Type, value = "Teacher", text = "Teacher")
      self.TypeEntry1.grid(row = 2, column = 2)
      self.TypeEntry1.select()
      self.TypeEntry2 = tk.Radiobutton(self.formframea, variable = self.Type, value = "Student", text = "Student")
      self.TypeEntry2.grid(row = 2, column = 3)

      self.Add = tk.Button(self.formframea, text = "Add")
      self.Add.grid(row = 3, column = 2)
      self.Close = tk.Button(self.formframea, text = "Close", command = self.formframea.grid_forget).grid(row = 3, column = 3)
  def NewBookForm(self):
      self.Add.grid_forget()
      self.formframeb.grid(row= 1, column = 0, sticky = "N")
      self.Name = tk.StringVar()
      self.Dewey = tk.StringVar()
      self.Author = tk.StringVar()
      self.Genre = tk.StringVar()

      self.NameLabel = tk.Label(self.formframeb, text = "Name:").grid(row = 1, column = 1)
      self.DeweyLabel = tk.Label(self.formframeb, text = "Location:").grid(row = 2, column = 1)
      self.AuthorLabel = tk.Label(self.formframeb, text = "Author:").grid(row = 3, column = 1)
      self.GenreLabel = tk.Label(self.formframeb, text = "Genre:").grid(row = 4, column = 1)

      self.NameEntry = tk.Entry(self.formframeb, textvariable = self.Name)
      self.NameEntry.grid(row = 1, column = 2, columnspan = 2)
      self.DeweyEntry = tk.Entry(self.formframeb, textvariable = self.Dewey)
      self.DeweyEntry.grid(row = 2, column = 2, columnspan = 2)
      self.AuthorEntry = tk.Entry(self.formframeb, textvariable = self.Author)
      self.AuthorEntry.grid(row = 3, column = 2, columnspan = 2)
      self.GenreEntry = tk.Entry(self.formframeb, textvariable = self.Genre)
      self.GenreEntry.grid(row = 4, column = 2, columnspan = 2)

      self.Add = tk.Button(self.formframeb, text = "Add")
      self.Add.grid(row = 6, column = 2)
      self.Close = tk.Button(self.formframeb, text = "Close", command = self.formframeb.grid_forget).grid(row = 6, column = 3)
  def Create_BookList(self, alist):
      self.printframe.grid_forget()
      self.NextDay.grid_forget()
      self.NextDay.destroy()
      self.NextDay = tk.Button(self, text = "Next Day", command = lambda test = 1: NewDay(test))
      self.NextDay.grid(column = 5, row = 5, sticky = "SE")
      self.booksframe.grid(row = 1, column = 2, sticky = 'NW', columnspan = 2)
      self.searchbox.bind('<Return>', self.searchbook)
      self.bTopIDLabel = tk.Label(self.booksframe, text = "Id").grid(row = 0, column = 3)
      self.bTopNameLabel = tk.Label(self.booksframe, text = "Name").grid(row = 0, column = 4)
      self.TopAuthorLabel = tk.Label(self.booksframe, text = "Author").grid(row = 0, column = 5)
      self.TopDeweyLabel = tk.Label(self.booksframe, text = "Location").grid(row = 0, column = 6)
      self.TopGenreLabel = tk.Label(self.booksframe, text = "Genre").grid(row = 0, column = 7)
      self.TopAmountLabel = tk.Label(self.booksframe, text = "Amount").grid(row = 0, column = 8)

      self.rownum = 0
      for widgetlist in self.bwidgetlist:
        for widget in widgetlist:
          widget.grid_forget()
          widget.destroy()
      self.bwidgetlist = []
      for books in alist:
        self.amount = 0
        for abook in book_list:
          if abook.name == books.name:
            self.amount +=1
        self.bwidgetlist.append([])
        self.rownum+=1
        self.columnnum = 1
        self.tklist = [books.id, books.name, books.author, books.dewey, books.genre, self.amount]
        self.bwidgetlist[-1].append(tk.Button(self.booksframe, text = "Edit", command = books.editbook))
        self.bwidgetlist[-1][-1].grid(row = self.rownum, column = 0)
        self.bwidgetlist[-1].append(tk.Button(self.booksframe, text = "View", command = books.viewbook))
        self.bwidgetlist[-1][-1].grid(row = self.rownum, column = 1)
        self.columnnum+=1
        self.bwidgetlist[-1].append(tk.Button(self.booksframe, text="Delete", command = books.deletewb))
        self.bwidgetlist[-1][-1].grid(row = self.rownum, column = 2)
        for textv in self.tklist:
          self.columnnum+=1
          self.bwidgetlist[-1].append(tk.Label(self.booksframe, text = str(textv)))
          self.bwidgetlist[-1][-1].grid(row = self.rownum, column = self.columnnum, sticky = "W")

  def Create_PersonList(self, alist):
    self.printframe.grid_forget()
    self.NextDay.grid_forget()
    self.NextDay.destroy()
    self.NextDay = tk.Button(self, text = "Next Day", command = lambda test = 0: NewDay(test))
    self.NextDay.grid(column = 5, row = 4, sticky = "SE")
    self.peopleframe.grid(row = 1, column = 2, sticky = 'NW', columnspan = 2)
    self.searchbox.grid(row = 0, column = 3, sticky = "W")
    self.searchtext.grid(row = 0, column = 2, sticky = "E")
    self.pTopIdLabel = tk.Label(self.peopleframe, text = "Id").grid(row = 0, column = 3)
    self.pTopNameLabel = tk.Label(self.peopleframe, text = "Name").grid(row = 0, column = 5)
    self.TopTypeLabel = tk.Label(self.peopleframe, text = "Type").grid(row = 0, column = 4)
    self.TopBooksOutLabel = tk.Label(self.peopleframe, text = "Books Out").grid(row = 0, column = 6)
    self.TopFinesLabel = tk.Label(self.peopleframe, text = "Fines").grid(row = 0, column = 7)

    self.rownum = 0
    for widgetlist in self.pwidgetlist:
      for widget in widgetlist:
        widget.grid_forget()
        widget.destroy()
    self.pwidgetlist = []
    for aperson in alist:
      self.pwidgetlist.append([])
      self.rownum+=1
      self.columnnum = 2
      booklist = ""
      for books in aperson.booksout:
        self.test = False
        for booktest in book_list:
          if books[0].id == booktest.id:
            booklist += books[0].name
            self.test = True
            if books != aperson.booksout[-1]:
              booklist+= ",\n"
            break
        if self.test == False:
          aperson.booksout.remove(books)
      self.tklist = [aperson.id, aperson.type, aperson.name, booklist, aperson.fines]
      self.pwidgetlist[-1].append(tk.Button(self.peopleframe, text = "Edit", command = aperson.editperson))
      self.pwidgetlist[-1][-1].grid(row = self.rownum, column = 0)
      self.pwidgetlist[-1].append(tk.Button(self.peopleframe, text = "View", command = aperson.viewperson))
      self.pwidgetlist[-1][-1].grid(row = self.rownum, column = 1)
      self.pwidgetlist[-1].append(tk.Button(self.peopleframe, text="Delete", command = aperson.deletewp))
      self.pwidgetlist[-1][-1].grid(row = self.rownum, column = 2)
      for textv in self.tklist:
        self.columnnum+=1
        self.pwidgetlist[-1].append(tk.Label(self.peopleframe, text = str(textv)))
        self.pwidgetlist[-1][-1].grid(row = self.rownum, column = self.columnnum, sticky = "W")
  def gridbooklist(self): #Creates the list without disrupting the forms
      self.printframe.grid_forget()
      self.peopleframe.grid_forget()
      self.booksframe.grid_forget()
      self.clearviewframe()
      self.searchbox.bind('<Return>', self.searchbook)
      self.searchbox.grid(row = 0, column = 3, sticky = "W")
      self.searchtext.grid(row = 0, column = 2, sticky = "E")
      self.Create_BookList(book_list)
  def gridpersonlist(self):
      self.printframe.grid_forget()
      self.booksframe.grid_forget()
      self.peopleframe.grid_forget()
      self.clearviewframe()
      self.searchbox.bind('<Return>', self.searchperson)
      self.searchbox.grid(row = 0, column = 3, sticky = "W")
      self.searchtext.grid(row = 0, column = 2, sticky = "E")
      self.Create_PersonList(person_list)
  def NewPerson(self, useless): #Takes data from the form to make a new data entry
    self.x = self.Name.get()
    self.z = self.Type.get()
    self.a = "10"
    if self.z == "Student":
      self.a = '2'
    elif self.z == "Teacher":
      self.a == '10'
    newdatap(self.x, self.z, self.a)
  def NewBook(self, useless):
      self.x = self.NameEntry.get()
      self.z = self.DeweyEntry.get()
      self.a = self.AuthorEntry.get()
      self.b = self.GenreEntry.get()

      newdatab(self.x, self.z, self.a, self.b)
  def minimumcell(self, frame): #Used for aethetics
    row_count, column_count = frame.grid_size()
    for col in range(column_count):
      frame.grid_columnconfigure(col, minsize= 20)
    for row in range(row_count):
      frame.grid_rowconfigure(col, minsize = 40)
  def clearviewframe(self): #Clears the viewframe for updating
    for num in range(len(self.labellist)):
      self.labellist[num].grid_forget()
      self.labellist[num].destroy()
    for num in range(len(self.extralist)):
      self.extralist[num].grid_forget()
      self.extralist[num].destroy()
    self.extralist.clear()
    self.viewframe.grid_forget()
    self.extraviewframe.grid_forget()
    self.labellist.clear()
  def searchperson(self, searchvalue):
    self.sentlist = []
    searchvalue = self.searchbox.get()
    if searchvalue == "":
      self.Create_PersonList(person_list)
      return
    searchvalue = searchvalue.lower()
    searchvalue = searchvalue.replace(" ", "")
    for aperson in person_list:
      self.attributelist = [aperson.id, strip(aperson.name), strip(aperson.type), aperson.fines]
      for attribute in self.attributelist:
        if searchvalue in attribute:
         if aperson not in self.sentlist:
            self.sentlist.append(aperson)
      for abooklist in aperson.booksout:
        if searchvalue == abooklist[0].name:
          if aperson not in self.sentlist:
            self.sentlist.append(aperson)
    self.Create_PersonList(self.sentlist)
  def searchbook(self, searchvalue):
    self.sentlist = []
    searchvalue = self.searchbox.get()
    searchvalue = strip(searchvalue)
    if searchvalue == "":
      self.Create_BookList(book_list)
      return
    for abook in book_list:
      self.attributelist = [abook.id, strip(abook.name), strip(abook.dewey), strip(abook.author), strip(abook.genre)]
      for attribute in self.attributelist:
        if searchvalue in attribute:
          if abook not in self.sentlist:
            self.sentlist.append(abook)
    self.Create_BookList(self.sentlist)
app = Application()

class data: #Parent of Person and Book classes, with shared functions
  def __init__(self, x, y):
    self.name = x
    self.id = str(y + 1)
    self.datehis = []
    self.datahis = []
    self.actionhis = []
    self.listlistlist = [self.datehis, self.datahis, self.actionhis]
    self.currentlistvars = []
    self.currentlist1 = []
  def hisupdate(self, d2, a): #adds to history, for later
    self.datehis.append(today.strftime("%m/%d/%Y"))
    self.datahis.append(d2)
    self.actionhis.append(a)
  def maketable(self):
    self.x = -1
    for l in self.listlistlist:
      self.x+=1
      self.y = 0
      for info in l:
          self.currentlistvars.append(tk.StringVar())
          self.currentlistvars[-1].set(info)
          self.currentlist1.append(tk.Label(app, textvariable = self.currentlistvars[-1]).grid(row = self.y, column = self.x))
          self.y+=1
          self.currentlistvars = []
  def createhis(self):
    app.extraviewframe.grid(row = self.rowval+5, column = 2, columnspan = 5)
    for num in range(len(app.extralist)):
      app.extralist[num-1].grid_forget()
    self.columnnum = -1
    app.extralist.append(tk.Label(app.extraviewframe, text = "History"))
    app.extralist[-1].grid(row = 0, column = 0)
    for listtype in self.listlistlist:
      self.columnnum += 1
      self.rownum = 0
      for action in listtype:
        self.rownum+=1
        app.extralist.append(tk.Label(app.extraviewframe, text = action))
        app.extralist[-1].grid(row = self.rownum, column = self.columnnum)
class person(data): #One of the two main data types
  def __init__(self, x, y, a, c):
    super().__init__(x, y)
    self.type = a
    self.maxbooks = c
    self.booksout = []
    self.fines = '$0'
    self.heldfines = 0
    idvalue[0]+=1
  def check(self, the_book): #Checks out or in books based on if the book is in the person's booksoutlist
    self.test = False
    for abooklist in self.booksout:
      if the_book.id == abooklist[0].id:
        self.daysout = 1
        self.day = datetime.datetime.strptime(abooklist[1], "%m/%d/%Y")
        self.daysout = (self.day-today).days
        self.fines = self.fines.replace("$", "")
        if self.daysout > 0:
          if self.type == "Student":
            if self.daysout > 14:
              self.heldfines = self.heldfines + math.ceil(((self.daysout-14)*.20)*100)/100
          elif self.type == "Teacher":
            if self.daysout > 30:
              self.heldfines = self.heldfines + math.ceil(((self.daysout-30)*.20)*100)/100
        self.fines = 0
        fine_calculation()
        self.hisupdate(the_book.name, "Checked In")
        the_book.hisupdate(self.name, "Checked In")
        self.booksout.remove(abooklist)
        self.test = True
    if self.test == False:
      if len(self.booksout) < int(self.maxbooks):
        self.booksout.append([the_book])
        self.datedue = "Forever"
        if self.type == "Student":
          self.datedue = today + datetime.timedelta(days = 14)
          self.datedue = self.datedue.strftime("%m/%d/%Y")

        elif self.type == "Teacher":
          self.datedue = today + datetime.timedelta(days = 30)
          self.datedue = self.datedue.strftime("%m/%d/%Y")
        self.booksout[-1].append(self.datedue)
        self.hisupdate(the_book.name, "Checked Out")
        the_book.hisupdate(self.name, "Checked Out")
    for abook in book_list:
      if abook.id == the_book.id:
        book_list[book_list.index(abook)].heldby = "none"
    the_book.viewbook()
    pickle_all()
  def deletewp(self): #Deletes widgets in pwidgetlist
    for widgetlist in app.pwidgetlist:
      for checkwidg in widgetlist:
        widgtext = checkwidg.cget("text")
        if widgtext == self.id:
          for widgetfound in widgetlist:
            widgetfound.grid_forget()
    deleteperson(self)
  def viewperson(self): #Creates the view window for a person
    app.forgetall()
    app.searchtext.grid_forget()
    app.NextDay.grid_forget()
    app.NextDay.destroy()
    app.NextDay = tk.Button(app, text = "Next Day", command = lambda test = 2: NewDay(test, self))
    app.NextDay.grid(column = 5, row = 4, sticky = "SE")
    app.viewframe.grid(row = 1, column = 1)
    app.labellist = []

    app.labellist.append(tk.Label(app.viewframe, text = "Id:"))
    app.labellist[-1].grid(row = 1, column = 0, sticky = 'W')

    app.labellist.append(tk.Label(app.viewframe, text = self.id))
    app.labellist[-1].grid(row = 1, column = 1, sticky = 'W')

    app.labellist.append(tk.Label(app.viewframe, text = self.name))
    app.labellist[-1].grid(row = 0, column = 0, columnspan = 1, sticky = 'W')

    self.rowval = 1
    app.viewframe.grid_columnconfigure(3, minsize = 0)

    app.labellist.append(tk.Label(app.viewframe, text = "Books Out"))
    app.labellist[-1].grid(row = 0, column = 3)
    app.labellist.append(tk.Label(app.viewframe, text = "Due Back"))
    app.labellist[-1].grid(row = 0, column = 4)
    app.labellist.append(tk.Label(app.viewframe, text = "Fines"))
    app.labellist[-1].grid(row = 0, column = 2)
    app.labellist.append(tk.Label(app.viewframe, text = self.fines))
    app.labellist[-1].grid(row = 1, column = 2)
    if self.fines != '$0':
      self.test = False
      for books in self.booksout:
        self.testdate = datetime.datetime.strptime(books[1], "%m/%d/%Y")
        if (self.testdate - today).days < 0:
          self.test = True
      if self.test != True:
        if float(self.fines.replace("$", "")) != 0:
          app.labellist.append(tk.Button(app.viewframe, text = "Pay Fines", command = self.payfines))
          app.labellist[-1].grid(row = 2, column = 2)
    for books in self.booksout:
      app.labellist.append(tk.Label(app.viewframe, text = books[0].name))
      app.labellist[-1].grid(row = self.rowval, column = 3)
      app.labellist.append(tk.Label(app.viewframe, text = books[1]))
      app.labellist[-1].grid(row = self.rowval, column = 4)
      self.rowval+=1
    self.rowval+=1
    app.minimumcell(app.viewframe)
    self.createhis()
  def editperson(self): #Brings up the form for editing a person
    app.formframeb.grid_forget()
    app.NewPersonForm()
    app.Add["text"] = "Change"
    app.Add.bind("<Button-1>", self.realpedit)
    if self.type == "Student":
      app.TypeEntry2.select()
    else:
      app.TypeEntry1.select()
    app.NameEntry.insert(0, self.name)
  def realpedit(self, useless): #Edits a person
      self.name = app.NameEntry.get()
      self.type = app.Type.get()
      pickle_all()
      app.Create_PersonList(person_list)
      app.searchperson("placeholder")
  def payfines(self): #Pays fines off
    self.fines = "$0"
    self.heldfines = 0
    pickle_all()
    self.viewperson()
class book(data): #The other main data type
  def __init__(self, x, z, a, b, c):
    super().__init__(x, z)
    self.dewey = a
    self.author = b
    self.genre = c
    self.rowval = 0
    idvalue[1]+=1
    self.fines = 0
    self.heldby = "none"
  def deletewb(self): #Deletes widgets out of bwidgetlist
    for widgetlist in app.bwidgetlist:
      for checkwidg in widgetlist:
        widgtext = checkwidg.cget("text")
        if widgtext == self.id:
          for widgetfound in widgetlist:
            widgetfound.grid_forget()
    deletebook(self)

  def viewbook(self): #Opens the view window for a book
    app.forgetall()
    app.searchtext.grid_forget()
    app.NextDay.grid_forget()
    app.NextDay.destroy()
    app.NextDay = tk.Button(app, text = "Next Day", command = lambda test = 3: NewDay(test, self))
    app.NextDay.grid(column = 5, row = 4, sticky = "SE")
    app.viewframe.grid(row = 1, column = 1)
    app.labellist = []

    app.labellist.append(tk.Label(app.viewframe, text = self.name))
    app.labellist[-1].grid(row = 1, column = 0, sticky = 'W')

    self.author1 = "By " + self.author
    app.labellist.append(tk.Label(app.viewframe, text = self.author1))
    app.labellist[-1].grid(row = 2, column = 0, sticky = 'W')

    app.labellist.append(tk.Label(app.viewframe, text = "Id"))
    app.labellist[-1].grid(row = 0, column = 3)

    app.labellist.append(tk.Label(app.viewframe, text = "Status"))
    app.labellist[-1].grid(row = 0, column = 4, columnspan = 2, sticky = 'W')

    self.rowval = 1
    app.viewframe.grid_columnconfigure(3, minsize = 0)

    for books in book_list:
      if books.name == self.name:
        app.labellist.append(tk.Label(app.viewframe, text = books.id))
        app.labellist[-1].grid(row = self.rowval, column = 3)
        self.inlistcheck = False
        for aperson in person_list:
          if self.inlistcheck == True:
            break
          for abooklist in aperson.booksout:
            if abooklist[0].id == books.id:
              app.labellist.append(tk.Button(app.viewframe, text = "Check In", command = books.checkin))
              app.labellist[-1].grid(row = self.rowval, column = 2)
              self.checkbookname = "Checked Out By " + aperson.name
              app.labellist.append(tk.Label(app.viewframe, text = self.checkbookname))
              app.labellist[-1].grid(row = self.rowval, column = 4, sticky = 'W')
              self.inlistcheck = True
              break
        if self.inlistcheck == False:
          app.labellist.append(tk.Button(app.viewframe, text = "Check Out", command = books.checkout))
          app.labellist[-1].grid(row = self.rowval, column = 2)
          app.labellist.append(tk.Label(app.viewframe, text = "Checked In"))
          app.labellist[-1].grid(row = self.rowval, column = 4, sticky = 'W')
          if books.heldby == "none":
            app.labellist.append(tk.Button(app.viewframe, text = 'Hold', command = books.holdbook))
            app.labellist[-1].grid(row = self.rowval, column = 1)
          else:
            self.rowval+=1
            app.labellist.append(tk.Label(app.viewframe, text = "On Hold By"))
            app.labellist[-1].grid(row = self.rowval, column = 3)
            app.labellist.append(tk.Label(app.viewframe, text = books.heldby))
            app.labellist[-1].grid(row = self.rowval, column = 4)
            self.rowval-=1

        app.labellist.append(tk.Button(app.viewframe, text = "History", command = books.createhis))
        app.labellist[-1].grid(row = self.rowval, column = 6)
        self.rowval+=2
    self.genre1 = "Genre: " + self.genre
    app.labellist.append(tk.Label(app.viewframe, text = self.genre1))
    app.labellist[-1].grid(row = 3, column = 0, sticky = 'W')
    self.rowval+=1
    app.minimumcell(app.viewframe)
  def checkin(self):
    for aperson in person_list:
      for booklist in aperson.booksout:
        if booklist[0].id == self.id:
          aperson.check(self)
  def checkout(self): #Sets up the text box for checking out
    self.extrarow = 1
    for books in book_list:
      if books.name == self.name:
        self.extrarow+=2
    app.extraviewframe.grid(row = self.extrarow, column = 2, columnspan = 5)
    for num in range(len(app.extralist)):
      app.extralist[num-1].grid_forget()
      app.extralist[num-1].destroy()
    app.extralist = []
    self.rowval+=1
    app.extralist.append(tk.Label(app.extraviewframe, text = "Enter a full name, or id"))
    app.extralist[-1].grid(row = 0, column = 0, columnspan = 3)
    app.extralist.append(tk.Entry(app.extraviewframe))
    app.extralist[-1].bind('<Return>', self.checkout2)
    app.extralist[-1].grid(row = 1, column = 0, columnspan = 3, sticky = "W")
  def checkout2(self, search): #Checks a book out to a person
    search = app.extralist[-1].get()
    self.test = False
    for person in person_list:
      if strip(search) == strip(person.name):
        if len(person.booksout) < int(person.maxbooks):
          person.check(self)
          app.clearviewframe()
          self.labellist = []
          self.viewbook()
        else:
          app.extralist.append(tk.Label(app.extraviewframe, text = "Enter a full name, or id"))
          app.extralist[-1].grid(row = 0, column = 0, columnspan = 3, sticky = 'W')
          app.extralist.append(tk.Label(app.extraviewframe, text = "This patron has too many books checked out"))
          app.extralist[-1].grid(row = 2, column = 0)
          app.extralist.append(tk.Entry(app.extraviewframe))
          app.extralist[-1].bind('<Return>', self.checkout2)
          app.extralist[-1].grid(row = 1, column = 0, columnspan = 3, sticky = "W")
          self.test = True
      if strip(search) == strip(person.id):
        if len(person.booksout) < int(person.maxbooks):
          person.check(self)
          app.clearviewframe()
          self.labellist = []
          self.viewbook()
        else:
          app.extralist.append(tk.Label(app.extraviewframe, text = "Enter a full name, or id"))
          app.extralist[-1].grid(row = 0, column = 0, columnspan = 3, sticky = 'W')
          app.extralist.append(tk.Label(app.extraviewframe, text = "This patron has too many books checked out"))
          app.extralist[-1].grid(row = 2, column = 0)
          app.extralist.append(tk.Entry(app.extraviewframe))
          app.extralist[-1].bind('<Return>', self.checkout2)
          app.extralist[-1].grid(row = 1, column = 0, columnspan = 3, sticky = "W")
          self.test = True
      elif self.test == False:
        for num in range(len(app.extralist)):
          app.extralist[num-1].grid_forget()
          app.extralist[num-1].destroy()
        app.extralist = []
        app.extralist.append(tk.Label(app.extraviewframe, text = "Enter a full name, or id"))
        app.extralist[-1].grid(row = 0, column = 0, columnspan = 3, sticky = 'W')
        app.extralist.append(tk.Label(app.extraviewframe, text = "Incorrect name/id"))
        app.extralist[-1].grid(row = 2, column = 0, columnspan = 3, sticky = 'W')
        app.extralist.append(tk.Entry(app.extraviewframe))
        app.extralist[-1].bind('<Return>', self.checkout2)
        app.extralist[-1].grid(row = 1, column = 0, columnspan = 3, sticky = "W")
  def editbook(self): #Brings up the form for editing
    app.formframea.grid_forget()
    app.NewBookForm()
    app.Add["text"] = "Change"
    app.Add.bind("<Button>", self.realbedit)
    app.NameEntry.insert(0, self.name)
    app.DeweyEntry.insert(0, self.dewey)
    app.AuthorEntry.insert(0, self.author)
    app.GenreEntry.insert(0, self.genre)
  def realbedit(self, useless): #Edits the book
      self.name = app.NameEntry.get()
      self.dewey = app.DeweyEntry.get()
      self.author = app.AuthorEntry.get()
      self.genre = app.GenreEntry.get()
      pickle_all()
      app.Create_BookList(book_list)
      app.searchbook("placeholder")
  def holdbook(self): #Sets the textbox from checkout() to work for holding
    self.checkout()
    app.extralist[-1].bind('<Return>', self.hold2)
  def hold2(self, useless): #Puts a book on hold
    for aperson in person_list:
      if strip(aperson.name) == strip(app.extralist[-1].get()):
        self.heldby = aperson
        self.hisupdate(aperson.name, "Put On Hold")
      elif aperson.id == strip(app.extralist[-1].get()):
        self.heldby = aperson
        self.hisupdate(aperson.name, "Put On Hold")
        apperson.hisupdate(self.name, "Put On Hold")
    self.heldby = app.extralist[-1].get()
    self.viewbook()
with open(PickledPeople, 'r+b') as file1: #Pulls data from a pickle file into the program
    person_list = pickle.load(file1)
    file1.close()
with open(PickledBooks, 'r+b') as file2:
    book_list = pickle.load(file2)
    file2.close()
with open(PickledId, 'r+b') as file3:
    idvalue = pickle.load(file3)
    file3.close()
fine_calculation()
app.master.title('WECHS Library Mangement')
app.mainloop() #Starts the application loop
