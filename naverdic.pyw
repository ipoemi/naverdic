#!/usr/bin/env python
#encoding: utf-8

from getdic import *
import gtk, gobject

class NaverDictionary(object):
	# pixel unit
	TEXT_AREA_INDENT = 10
	NUMBER_OF_RESULT = 10
	CONTENTS_WIDTH = 300
	CONTENTS_HEIGHT = 300

	ICON_FILE_NAME = "naverdic.png"

	def __init__(self):
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.connect("delete-event", self.hide)
		window.set_property("skip-taskbar-hint", True)
		window.set_keep_above(True)
		# draw widgets and make widget tree
		window.set_title("Naver Dictionary")
		window.set_icon_from_file(self.ICON_FILE_NAME)
		statusIcon = gtk.status_icon_new_from_file(self.ICON_FILE_NAME)
		statusIcon.connect("popup-menu", self.getStatusIconPopup)
		statusIcon.connect("activate", self.toggleVisible)
		statusIconMenu = gtk.Menu()
		statusIconMenuItem = gtk.ImageMenuItem(gtk.STOCK_OPEN)
		statusIconMenuItem.connect("button-press-event", self.show)
		statusIconMenu.append(statusIconMenuItem)
		statusIconMenuItem = gtk.SeparatorMenuItem()
		statusIconMenu.append(statusIconMenuItem)
		statusIconMenuItem = gtk.ImageMenuItem(gtk.STOCK_CLOSE)
		statusIconMenuItem.connect("button-press-event", self.gtk_main_quit)
		statusIconMenu.append(statusIconMenuItem)
		mainBox = gtk.VBox()
		mainBox.set_size_request(
		NaverDictionary.CONTENTS_WIDTH, NaverDictionary.CONTENTS_HEIGHT)
		titleLabel = gtk.Label()
		titleLabel.set_use_markup(True)
		titleLabel.set_markup("<b>Naver Dictionary</b>")
		mainBox.pack_start(titleLabel, False)
		mainBox.pack_start(gtk.HSeparator(), False, True, 5)
		searchBox = gtk.HBox()
		searchEntry = gtk.Entry()
		searchBox.add(searchEntry)
		searchButton = gtk.Button()
		searchButton.set_label("Search")
		searchBox.add(searchButton)
		mainBox.pack_start(searchBox, False)
		resultNotebook = gtk.Notebook()
		resultNotebook.set_tab_pos(gtk.POS_BOTTOM)
		resultNotebook.set_scrollable(True)
		mainBox.add(resultNotebook)
		mainBox.pack_start(gtk.HSeparator(), False, True, 5)
		sponsorLink = gtk.LinkButton("http://www.naver.com/")
		mainBox.pack_end(sponsorLink, False)
		window.add(mainBox)
		# set timer and handler connect
		gobject.timeout_add(1500, self.onTimer)
		# signal handler connect
		searchEntry.connect("key-press-event", self.onEnterKeyPressed)
		searchButton.connect("clicked", self.onSearchButtonClicked)
		# get clipboard
		self.clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
		# necessary widget store in self instance
		self.resultNotebook = resultNotebook
		self.searchEntry = searchEntry
		self.statusIconMenu = statusIconMenu
		self.window = window
		self.window.show_all()
		# etc valuable
		self.lastClipboardText = ""

	def toggleVisible(self, *args):
		if self.window.is_active():
			self.hide()
		else:
			self.show()
		return True

	def show(self, *args):
		self.window.present()
		self.window.move(self.windowPositionX, self.windowPositionY)
		return True

	def hide(self, *args):
		(self.windowPositionX, self.windowPositionY) =\
			self.window.get_position()
		self.window.hide()
		return True

	def getStatusIconPopup(self, data, eventButton, eventTime):
		self.statusIconMenu.show_all()
		self.statusIconMenu.popup(None, None, None, eventButton, eventTime)

	def onTimer(self):
		self.clipboard.request_text(self.treatClipboardText)
		return True

	def treatClipboardText(self, clipboard, text, data):
		if not text:
			return
		text.strip()
		if self.lastClipboardText != text:
			self.lastClipboardText = text
			self.searchEntry.set_text(text)
			self.onSearchButtonClicked()


	def onEnterKeyPressed(self, widget, event, *args):
		if event.keyval == 65293:
			self.onSearchButtonClicked(self)

	def onSearchButtonClicked(self, *args):
		notebook = self.resultNotebook
		word = self.searchEntry.get_text()
		words = notebook.get_children()
		pageNum = 0
		for child in words:
			label = notebook.get_tab_label(child)
			if label.get_label() == word:
				notebook.set_current_page(pageNum)
				return
			pageNum += 1
		else:
			result = getDic(word)
			self.insertResult(word, result)
			pass

	def insertResult(self, word, contents):
		notebook = self.resultNotebook
		txtBuffer = gtk.TextBuffer()
		txtBuffer.set_text(contents)
		txtView = gtk.TextView(txtBuffer)
		txtView.set_editable(False)
		txtView.set_indent(NaverDictionary.TEXT_AREA_INDENT)
		#txtView.set_wrap_mode(gtk.WRAP_WORD)
		scrolledWindow = gtk.ScrolledWindow()
		scrolledWindow.set_policy(
		gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		scrolledWindow.add(txtView)
		label = gtk.Label()
		label.set_label(word)
		txtView.show()
		label.show()
		scrolledWindow.show()
		if notebook.get_n_pages() == NaverDictionary.NUMBER_OF_RESULT:
			tmp = notebook.get_nth_page(NaverDictionary.NUMBER_OF_RESULT-1)
			notebook.remove_page(NaverDictionary.NUMBER_OF_RESULT-1)
			tmp.destroy()
		notebook.insert_page(scrolledWindow, label, 0)
		notebook.set_current_page(0)

	def run(self):
		gtk.main();

	def gtk_main_quit(self, *args):
		gtk.main_quit(*args)

if __name__ == "__main__":
	naverdic = NaverDictionary()
	naverdic.run()
