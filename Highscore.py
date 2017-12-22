# in CMD C:\Python34\python.exe D:\Users\OKO\PycharmProjects\untitled\ESA2.py

# coding: utf8
# -*- coding: iso-8859-15 -*-
__author__ = 'Kossjak'

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sqlite3
from time import strftime

class TreeViewFilterWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="ESA2: Vorgehensmodelle")
        self.set_border_width(10)

        # Einrichten des self.grid, in dem die Elemente positioniert werden sollen
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)
        self.add(self.grid)

        # ListStore Modell erstellen
        self.db_liststore = Gtk.ListStore(int, str, str, str)

        # Ich habe DB Tabelle mit Hilfe des Terminals erstellt, wie im Video 1-34
        # cursor.execute("Create table sprint (id INTEGER, vonbis varchar(32), erlaeuterung VARCHAR(255))")

        # cursor.execute('ALTER TABLE sprint ADD COLUMN checkbox boolean')
        # db.commit()
        db = sqlite3.connect('D:/Users/OKO/PycharmProjects/untitled/okDB.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM sprint")
        for row in cursor:
            #print(self.db_liststore(list(row[0])))
            self.db_liststore.append(list(row))

        # Erstellen der Baumansicht und Hinzufügen der Spalten
        self.treeview = Gtk.TreeView(model=self.db_liststore)
        for i, column_title in enumerate(["ID", "Sprint von - bis", "Erläuterung", "Erledigt"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        # Zeile der Baumansicht Auswahl
        self.selection = self.treeview.get_selection()

        # Einfügen der treeview in ein scrollwindow
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)

        self.grid.attach(self.scrollable_treelist, 0, 0, 9, 12)

        self.datumLabel = Gtk.Label("Sprint von - bis: ")
        self.grid.attach_next_to(self.datumLabel, self.scrollable_treelist, Gtk.PositionType.RIGHT, 1, 1)

        self.datumEntry = Gtk.Entry()
        self.zeit = strftime("%d.%m.%Y - %d.%m.%Y")
        self.datumEntry.set_text(self.zeit)
        self.grid.attach_next_to(self.datumEntry, self.datumLabel, Gtk.PositionType.RIGHT, 2, 1)

        self.beschreibungLabel = Gtk.Label("Erläuterung: ")
        self.grid.attach_next_to(self.beschreibungLabel, self.datumLabel, Gtk.PositionType.BOTTOM, 1, 1)

        self.beschreibungEntry = Gtk.Entry()
        self.beschreibungEntry.set_text("")
        self.grid.attach_next_to(self.beschreibungEntry, self.beschreibungLabel, Gtk.PositionType.RIGHT, 2, 1)

        self.button1 = Gtk.Button(label="speichern")
        self.button1.connect('clicked', self.speichern)
        self.grid.attach_next_to(self.button1, self.beschreibungLabel, Gtk.PositionType.BOTTOM, 1, 1)

        self.button2 = Gtk.Button(label="löschen")
        self.button2.connect('clicked', self.loeschen)
        # letzte Werte sind die Größe des Buttons
        self.grid.attach_next_to(self.button2, self.button1, Gtk.PositionType.RIGHT, 1, 1)

        self.button3 = Gtk.Button(label="erledigt")
        self.button3.connect('clicked', self.erledigt)
        # letzte Werte sind die Größe des Buttons
        self.grid.attach_next_to(self.button3, self.button2, Gtk.PositionType.RIGHT, 1, 1)

        self.scrollable_treelist.add(self.treeview)

        self.show_all()

    def speichern(self, widget):
        # Verbindung mit der Datenbank
        db = sqlite3.connect('D:/Users/OKO/PycharmProjects/untitled/okDB.db')
        cursor = db.cursor()

        # ID Prüfung und Vergabe
        idNummer = 1
        for i in range(len(self.db_liststore)):
            if idNummer == 1:
                idNummer = idNummer + 1
            else:
                idNummer = self.db_liststore[-1][0] + 1

        if self.beschreibungEntry.get_text() == "":
            # Informationdialog macht einen Hinweis
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "Informationsfenster")
            dialog.format_secondary_text("Bitte geben Sie Erläuterung ein.")
            dialog.run()
            dialog.destroy()

        else:
            self.db_liststore.append(list((idNummer, self.datumEntry.get_text(), self.beschreibungEntry.get_text(),'')))
            cursor.execute("INSERT INTO sprint VALUES(?,?,?,?)",(idNummer, self.datumEntry.get_text(), self.beschreibungEntry.get_text(),''))
            db.commit()
            self.beschreibungEntry.set_text("")

    def loeschen(self, widget):
        # Auswahl holen
        (model, iter) = self.selection.get_selected()

        # Wenn es eine Auswahl gibt, wird diese aus dem Modell entfernt
        if iter is not None:

            # Auswahl der DB
            db = sqlite3.connect('D:/Users/OKO/PycharmProjects/untitled/okDB.db')
            cursor = db.cursor()
            # Auswahl der zu löschenden Zeile
            cursor.execute("DELETE FROM sprint WHERE id=?", ((model[iter][0],)))
            # Übertragung an DB
            db.commit()

            # Löschen der dargestellten liststore
            self.db_liststore.clear()
            # Auswahl des DB Inhaltes
            cursor.execute("SELECT * FROM sprint")
            # Eintragen des DB Inhaltes in liststore
            for row in cursor:
                self.db_liststore.append(list(row))

            # Name Eingabefeld wird auf leer gesetzt
            self.beschreibungEntry.set_text("")

        # Andernfalls wird der Benutzer gebeten etwas auszuwählen, was entfernt werden soll.
        else:
            # Informationdialog macht einen Hinweis
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "Informationsfenster")
            dialog.format_secondary_text("Bitte wählen Sie zuerst aus der Liste einen Eintrag aus.")
            dialog.run()
            dialog.destroy()

    def erledigt(self, widget):
        # Auswahl holen
        (model, iter) = self.selection.get_selected()

        # Wenn es eine Auswahl gibt, wird diese aus dem Modell entfernt
        if iter is not None:

            # Auswahl der DB
            db = sqlite3.connect('D:/Users/OKO/PycharmProjects/untitled/okDB.db')
            cursor = db.cursor()
            # Wenn Aufgabe fälschlicherweiese als erledigt markiert wurde, so besteht die möglichkeit dieses wieder rückgängig zu machen
            if model[iter][3] == 'Ja':
                cursor.execute("UPDATE sprint SET checkbox='' WHERE Id=?", (model[iter][0],))
            else:
                # Auswahl der zu löschenden Zeile
                cursor.execute("UPDATE sprint SET checkbox='Ja' WHERE Id=?", (model[iter][0],))
            # Übertragung an DB
            db.commit()

            # Löschen der dargestellten liststore
            self.db_liststore.clear()
            # Auswahl des DB Inhaltes
            cursor.execute("SELECT * FROM sprint")
            # Eintragen des DB Inhaltes in liststore
            for row in cursor:
                self.db_liststore.append(list(row))

            # Name Eingabefeld wird auf leer gesetzt
            self.beschreibungEntry.set_text("")

        # Andernfalls wird der Benutzer gebeten etwas auszuwählen, was entfernt werden soll.
        else:
            # Informationdialog macht einen Hinweis
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "Informationsfenster")
            dialog.format_secondary_text("Bitte wählen Sie zuerst aus der Liste einen Eintrag aus.")
            dialog.run()
            dialog.destroy()

win = TreeViewFilterWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()