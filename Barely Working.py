import tkinter as tk
import math
import time
import datetime
from datetime import date
import pickle
import os
PickledPeople = 'PickledPeople.pk1'
PickledBooks = 'PickledBooks.pk1'
PickledId = 'singlevalue.pk1'
book_list = [] # Appending lists was the method I used to create objects during runtime
person_list = []
today = datetime.datetime.today()
todaystring = today.strftime('%m/%d/%Y')
idvalue = [0, 0]
fwidgetlist = []
def fine_calculation():
  for aperson in person_list:
    aperson.fines = 0
    for books in aperson.booksout:
      for abook in book_list:
        if abook.id == books[0].id:
          day = datetime.datetime.strptime(abook.datehis[-1], "%m/%d/%Y")
          daysout = abs(day-today).days
          if aperson.type == "Student":
              if daysout > 14:
                  aperson.fines = float(aperson.fines) + math.ceil(((daysout - 14)*.20)*100)/100
          elif aperson.type == "Teacher":
            if daysout > 30:
              aperson.fines= float(aperson.fines) + math.ceil(((daysout - 30)*.20)*100)/100
      if aperson.fines != 0:
        if (float(aperson.fines)*100)%10 == 0:
          aperson.fines =str(aperson.fines) + '0'
    aperson.fines = '$'+str(aperson.fines)
def pickledump(list1, file):
  with open(file, 'wb') as op:
    pickle.dump(list1, op, pickle.HIGHEST_PROTOCOL)

def pickle_all():
  pickledump(person_list, PickledPeople)
  pickledump(book_list, PickledBooks)
  pickledump(idvalue, PickledId)
def newdatap(x, z, a): #Easier to code with two seperate functions
    person_list.append(person(x, idvalue[0], z, a))
    pickle_all()
    app.gridpersonlist()
def newdatab(x, z, a, b):
    book_list.append(book(x, idvalue[1], z, a, b))
    pickle_all()
    app.gridbooklist()
def makefinefile(thefile):
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
      top3 = top1.center(length) + "  " + top2.center(6) + "\n"
      finelist.append(top3)
      thefile.write(top3)
      times = False
    if aperson.fines != "$0":
      towrite = aperson.name.center(length) + "  " + aperson.fines.center(6) + '\n'
      finelist.append(towrite)
      thefile.write(towrite)
  for num in range(3):
    thefile.write("\n")
  return(finelist)
def makedatesfile(thefile):
  lengthtest = person_list[0].name
  lengthtest2 = book_list[0].name
  times = True
  datelist = []
  lastperson = "lol"
  towrite = "lolagain"
  for aperson in person_list:
    if len(aperson.name) > len(lengthtest):
      lengthtest = aperson.name
  for abook in book_list:
    if len(abook.name) > len(lengthtest2):
      lengthtest = abook.name
  length = len(lengthtest)
  length2 = len(lengthtest2)
  for aperson in person_list:
    for abooklist in aperson.booksout:
      if times == True:
        top1 = "Name"
        top2 = "Book"
        top3 = "Day Back"
        top4 = "Days Out"
        top5 = top1.center(length) + "  " + top2.center(length2) + "  " + top3.center(10) + "  " + top4.center(9)+ "\n"
        datelist.append(top5)
        thefile.write(top5)
        times = False
      if lastperson == aperson.id:
        for spaces in range(length):
          towrite.append(" ")
      else:
        towrite = aperson.name.center(length)
      daysout = datetime.datetime.strptime(abooklist[1], "%m/%d/%Y") - today
      daysout = daysout.days + 1
      if daysout >= 0:
          daysout1 = str(daysout) + " Days Until Due"
      elif daysout < 0:
        if daysout == -1:
          daysout = str(abs(daysout)) + " Day Late"
        else:
          daysout = str(abs(daysout)) + " Days Late"
      towrite = towrite + "  " + abooklist[0].name.center(length2) + "  " + abooklist[1].center(10) + "  " + daysout + '\n'
      datelist.append(towrite)
      thefile.write(towrite)
      lastperson = aperson.id
  return(datelist)
def makefile():
  os.remove("Report.txt")
  thefile = open("Report.txt", "w+")
  finelist = makefinefile(thefile)
  datelist = makedatesfile(thefile)
  thefile.close()
  rowval = 0
  app.forgetall()
  app.printframe.grid(row = 1, column = 1)
  for widget in finelist:
    fwidgetlist.append(tk.Label(app.printframe, text = widget))
    fwidgetlist[-1].grid(row = rowval, column = 0, sticky = "W")
    rowval+=1
  for widget in datelist:
    fwidgetlist.append(tk.Label(app.printframe, text = widget))
    fwidgetlist[-1].grid(row = rowval, column = 0, sticky = "W")
    rowval+=1
  fwidgetlist.append(tk.Button(app.printframe, text = "Close", command = app.forgetall))
  fwidgetlist[-1].grid(row = rowval, column = 1)
  fwidgetlist.append(tk.Button(app.printframe, text = "Print", command = lambda: os.startfile("Report1.txt", "print")))
  fwidgetlist[-1].grid(row = rowval, column = 0)
def deleteperson(num):
  del person_list[person_list.index(num)]
  pickle_all()
  app.Create_PersonList(person_list)
def deletebook(num):
  del book_list[book_list.index(num)]
  pickle_all()
  app.Create_BookList(book_list)
def NewDay(test, object1 = "nevermind"):
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
class Application(tk.Frame):
  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.grid()
    self.bwidgetlist = []
    self.pwidgetlist = []
    self.mb = tk.Menubutton(self, text = 'Menu')
    self.mb.grid(row = 0, column = 0, sticky = 'NW')
    self.mb.menu = tk.Menu(self.mb)
    self.mb['menu'] = self.mb.menu
    self.mb.menu.add_command(label = 'New Person', command = self.PersonFC)
    self.mb.menu.add_command(label = 'New Book', command = self.BookFC)
    self.mb.menu.add_command(label = 'Show Books', command = self.gridbooklist)
    self.mb.menu.add_command(label = 'Show People', command = self.gridpersonlist)
    self.mb.menu.add_command(label = "Make File", command = makefile)
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
  def showprint():
    self.forgetall()
    for widget in self.printlist:
      widget.grid_forget()
      widget.destroy()
    self.printframe.grid(row = 1, column = 1)
    self.fineslist = makefinefile()
  def forgetall(self):
    self.NextDay.grid_forget
    self.searchbox.grid_forget()
    self.searchtext.grid_forget
    self.clearviewframe()
    self.formframea.grid_forget()
    self.formframeb.grid_forget()
    self.booksframe.grid_forget()
    self.peopleframe.grid_forget()
    self.printframe.grid_forget()
  def PersonFC(self):
      self.formframeb.grid_forget()
      self.printframe.grid_forget()
      self.clearviewframe()
      self.NewPersonForm()
      self.Add.bind("<Button-1>", self.NewPerson)
  def BookFC(self):
      self.formframea.grid_forget()
      self.printframe.grid_forget()
      self.clearviewframe()
      self.NewBookForm()
      self.Add.bind("<Button-1>", self.NewBook)
  def NewPersonForm(self):
      self.Add.grid_forget()
      self.formframea.grid(row= 1, column = 0)
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
      self.formframeb.grid(row= 1, column = 0)
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
          self.bwidgetlist[-1][-1].grid(row = self.rownum, column = self.columnnum)

  def Create_PersonList(self, alist):
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
              booklist+= ", "
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
        self.pwidgetlist[-1][-1].grid(row = self.rownum, column = self.columnnum)
  def gridbooklist(self):
      self.peopleframe.grid_forget()
      self.booksframe.grid_forget()
      self.clearviewframe()
      self.searchbox.bind('<Return>', self.searchbook)
      self.searchbox.grid(row = 0, column = 3, sticky = "W")
      self.searchtext.grid(row = 0, column = 2, sticky = "E")
      self.Create_BookList(book_list)
  def gridpersonlist(self):
      self.booksframe.grid_forget()
      self.peopleframe.grid_forget()
      self.clearviewframe()
      self.searchbox.bind('<Return>', self.searchperson)
      self.searchbox.grid(row = 0, column = 3, sticky = "W")
      self.searchtext.grid(row = 0, column = 2, sticky = "E")
      self.Create_PersonList(person_list)
  def NewPerson(self, useless):
    self.x = self.Name.get()
    self.z = self.Type.get()
    self.a = "lol"
    if self.z == "Student":
      self.a = '2'
    if self.z == "Teacher":
      self.a == '10'
    if self.z == "Admin":
      self.a == 129864880
    newdatap(self.x, self.z, self.a)
  def NewBook(self, useless):
      self.x = self.NameEntry.get()
      self.z = self.DeweyEntry.get()
      self.a = self.AuthorEntry.get()
      self.b = self.GenreEntry.get()

      newdatab(self.x, self.z, self.a, self.b)
  def minimumcell(self, frame):
    row_count, column_count = frame.grid_size()
    for col in range(column_count):
      frame.grid_columnconfigure(col, minsize= 20)
    for row in range(row_count):
      frame.grid_rowconfigure(col, minsize = 40)
  def clearviewframe(self):
    for num in range(len(self.labellist)):
      self.labellist[num].grid_forget()
      self.labellist[num].destroy()
    for num in range(len(self.extralist)):
      self.extralist[num].grid_forget()
    self.viewframe.grid_forget()
    self.labellist.clear()
  def searchperson(self, searchvalue):
    self.sentlist = []
    searchvalue = self.searchbox.get()
    if searchvalue == "":
      self.Create_PersonList(person_list)
      return
    for aperson in person_list:
      self.attributelist = [aperson.id, aperson.name, aperson.type, aperson.fines]
      for attribute in self.attributelist:
        if searchvalue == attribute:
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
    if searchvalue == "":
      self.Create_BookList(book_list)
      return
    for abook in book_list:
      self.attributelist = [abook.id, abook.name, abook.dewey, abook.author, abook.genre, abook.genre]
      for attribute in self.attributelist:
        if searchvalue == attribute:
          if abook not in self.sentlist:
            self.sentlist.append(abook)
    self.Create_BookList(self.sentlist)
app = Application()


class data:
  def __init__(self, x, y):
    self.name = x
    self.id = str(y + 1)
    self.datehis = []
    self.datahis = []
    self.actionhis = []
    self.listlistlist = [self.datehis, self.datahis, self.actionhis]
    self.currentlistvars = []
    self.currentlist1 = []
  def hisupdate(self, d2, a):
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
    app.extraviewframe.grid(row = self.rowval, column = 2, columnspan = 5)
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
class person(data):
  def __init__(self, x, y, a, c):
    super().__init__(x, y)
    self.type = a
    self.maxbooks = c
    self.booksout = []
    self.fines = 0
    idvalue[0]+=1
  def check(self, the_book = 0):
    self.test = False
    for abooklist in self.booksout:
      if the_book.id == abooklist[0].id:
        self.booksout.remove(abooklist)
        self.hisupdate(the_book.name, "Checked In")
        the_book.hisupdate(self.name, "Checked In")
        self.test = True
        break
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
    the_book.viewbook()
    pickle_all()
  def deletewp(self):
    for widgetlist in app.pwidgetlist:
      for checkwidg in widgetlist:
        widgtext = checkwidg.cget("text")
        if widgtext == self.id:
          for widgetfound in widgetlist:
            widgetfound.grid_forget()
    deleteperson(self)
  def viewperson(self):
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
    for books in self.booksout:
      app.labellist.append(tk.Label(app.viewframe, text = books[0].name))
      app.labellist[-1].grid(row = self.rowval, column = 3)
      app.labellist.append(tk.Label(app.viewframe, text = books[1]))
      app.labellist[-1].grid(row = self.rowval, column = 4)
      self.rowval+=1
    self.rowval+=1
    app.minimumcell(app.viewframe)
    self.createhis()
  def editperson(self):
    app.formframeb.grid_forget()
    app.NewPersonForm()
    app.Add["text"] = "Change"
    app.Add.bind("<Button-1>", self.realpedit)
    app.NameEntry.insert(0, self.name)
  def realpedit(self, useless):
      self.name = app.NameEntry.get()
      self.type = app.Type.get()
      pickle_all()
      app.Create_PersonList(person_list)
      app.searchperson("lol")
class book(data):
  def __init__(self, x, z, a, b, c):
    super().__init__(x, z)
    self.dewey = a
    self.author = b
    self.genre = c
    self.rowval = 0
    idvalue[1]+=1
    self.fines = 0
  def deletewb(self):
    for widgetlist in app.bwidgetlist:
      for checkwidg in widgetlist:
        widgtext = checkwidg.cget("text")
        if widgtext == self.id:
          for widgetfound in widgetlist:
            widgetfound.grid_forget()
    deletebook(self)

  def viewbook(self):
    app.forgetall()
    app.searchtext.grid_forget()
    app.NextDay.grid_forget()
    app.NextDay.destroy()
    app.NextDay = tk.Button(app, text = "Next Day", command = lambda test = 3: NewDay(test, self))
    app.NextDay.grid(column = 5, row = 4, sticky = "SE")
    app.viewframe.grid(row = 1, column = 1)
    app.labellist = []

    app.labellist.append(tk.Label(app.viewframe, text = self.name))
    app.labellist[-1].grid(row = 1, column = 0, columnspan = 2, sticky = 'W')

    self.author1 = "By " + self.author
    app.labellist.append(tk.Label(app.viewframe, text = self.author1))
    app.labellist[-1].grid(row = 2, column = 0, sticky = 'W')

    app.labellist.append(tk.Label(app.viewframe, text = "Id"))
    app.labellist[-1].grid(row = 0, column = 3)

    app.labellist.append(tk.Label(app.viewframe, text = "Checked"))
    app.labellist[-1].grid(row = 0, column = 4, columnspan = 2, sticky = 'W')

    self.rowval = 1
    app.viewframe.grid_columnconfigure(3, minsize = 0)

    for books in book_list:
      if books.name == self.name:
        app.labellist.append(tk.Label(app.viewframe, text = books.id))
        app.labellist[-1].grid(row = self.rowval, column = 3)
        self.inlistcheck = False
        for aperson in person_list:
          for abooklist in aperson.booksout:
            if abooklist[0].id == books.id:
              app.labellist.append(tk.Button(app.viewframe, text = "Check In", command = lambda: aperson.check(books)))
              app.labellist[-1].grid(row = self.rowval, column = 2)
              self.checkbookname = "Checked Out By " + aperson.name
              app.labellist.append(tk.Label(app.viewframe, text = self.checkbookname))
              self.inlistcheck = True
              break
          if self.inlistcheck == True:
            break
        if self.inlistcheck == False:
          app.labellist.append(tk.Button(app.viewframe, text = "Check Out", command = self.checkout))
          app.labellist[-1].grid(row = self.rowval, column = 2)
          app.labellist.append(tk.Label(app.viewframe, text = "Checked In"))
        app.labellist[-1].grid(row = self.rowval, column = 4)

        app.labellist.append(tk.Button(app.viewframe, text = "History", command = self.createhis))
        app.labellist[-1].grid(row = self.rowval, column = 6)
        self.rowval+=1
    self.genre1 = "Genre: " + self.genre
    app.labellist.append(tk.Label(app.viewframe, text = self.genre1))
    app.labellist[-1].grid(row = 3, column = 0, sticky = 'W')
    self.rowval+=1
    app.minimumcell(app.viewframe)
  def checkout(self):
    app.extraviewframe.grid(row = self.rowval, column = 2, columnspan = 5)
    for num in range(len(app.extralist)):
      app.extralist[num-1].grid_forget()
      app.extralist[num-1].destroy()
    app.extralist = []
    self.rowval+=1
    app.extralist.append(tk.Label(app.extraviewframe, text = "Enter a full name, or id"))
    app.extralist[-1].grid(row = 0, column = 0, columnspan = 3)
    app.extralist.append(tk.Entry(app.extraviewframe))
    app.extralist[-1].bind('<Return>', self.checkout2)
    app.extralist[-1].grid(row = self.rowval+1, column = 0, columnspan = 3, sticky = "W")
  def checkout2(self, search):
    search = app.extralist[-1].get()
    for person in person_list:
      if search == person.name:
        person.check(self)
      if search == person.id:
        person.check(self)
    app.clearviewframe()
    self.labellist = []
    self.viewbook()
  def editbook(self):
    app.formframea.grid_forget()
    app.NewBookForm()
    app.Add["text"] = "Change"
    app.Add.bind("<Button>", self.realbedit)
    app.NameEntry.insert(0, self.name)
    app.DeweyEntry.insert(0, self.dewey)
    app.AuthorEntry.insert(0, self.author)
    app.GenreEntry.insert(0, self.genre)
  def realbedit(self, useless):
      self.name = app.NameEntry.get()
      self.dewey = app.DeweyEntry.get()
      self.author = app.AuthorEntry.get()
      self.genre = app.GenreEntry.get()
      pickle_all()
      app.Create_BookList(book_list)
      app.searchbook("lol")
with open(PickledPeople, 'r+b') as file1:
    person_list = pickle.load(file1)
    file1.close()
with open(PickledBooks, 'r+b') as file2:
    book_list = pickle.load(file2)
    file2.close()
with open(PickledId, 'r+b') as file3:
    idvalue = pickle.load(file3)
    file3.close()
fine_calculation()
app.master.title('Sample application')
app.mainloop()
