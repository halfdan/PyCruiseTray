import gtk

from server_manager import ServerManager

class SettingsDialog(gtk.Dialog):
    def __init__(self):
        gtk.Dialog.__init__(self, "Server Settings", self, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)

        # Instantiate ServerManager
        self.server_manager = ServerManager()

        # Create TreeStore for Server list
        self.liststore = gtk.ListStore(str, str)
        self.treeview = gtk.TreeView(self.liststore)

        # Create TreeViewColumns to display data
        cell = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Name", cell, text=0)
        self.treeview.append_column(col)

        cell = gtk.CellRendererText()
        col = gtk.TreeViewColumn("URL", cell, text=1)
        self.treeview.append_column(col)

        self.vbox.pack_start(self.treeview)

        self.button_add = gtk.Button("Add Server", gtk.STOCK_ADD)
        self.vbox.pack_start(self.button_add)
        self.button_add.show()
        self.button_add.connect('clicked', self.add_server)

        self.add_button("Close", gtk.RESPONSE_CLOSE)

        self.resize(500,350)
        self.set_position(gtk.WIN_POS_CENTER)
        self.show_all()

        self.load_server_list()

    def add_server(self, widget):
        add_server_dialog = ServerAddDialog()
        result = add_server_dialog.run()
        if result == gtk.RESPONSE_OK:
            server_name = add_server_dialog.get_name()
            server_url = add_server_dialog.get_url()
            self.server_manager.add(server_name, server_url)
            self.load_server_list()
            add_server_dialog.destroy()

    def load_server_list(self):
        self.liststore.clear()
        servers = self.server_manager.list()
        for server in servers:
            self.liststore.append([server['name'], server['url']])
        self.show_all()

class ServerAddDialog(gtk.Dialog):
    def __init__(self):
        gtk.Dialog.__init__(self, "Add Server", self, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)

        # HBox for Server Name
        self.hbox1 = gtk.HBox(True, 2)
        self.vbox.pack_start(self.hbox1)

        self.label_name = gtk.Label("Server Name")
        self.hbox1.pack_start(self.label_name)

        self.entry_name = gtk.Entry()
        self.hbox1.pack_start(self.entry_name)

        # HBox for Server URL
        self.hbox2 = gtk.HBox(True, 2)
        self.vbox.pack_start(self.hbox2)

        self.label_url = gtk.Label("Server URL")
        self.hbox2.pack_start(self.label_url)

        self.entry_url = gtk.Entry()
        self.hbox2.pack_start(self.entry_url)

        # HBox for Server Type
        self.hbox3 = gtk.HBox(True, 2)
        self.vbox.pack_start(self.hbox3)

        self.label_type = gtk.Label("Server Type")
        self.hbox3.pack_start(self.label_type)

        self.cbentry_type = gtk.combo_box_entry_new_text()
        self.cbentry_type.append_text('Ruby')
        self.cbentry_type.append_text('Java')
        self.cbentry_type.append_text('.NET')
        self.cbentry_type.child.connect('changed', self.set_type)
        self.cbentry_type.set_active(0)
        self.hbox3.pack_start(self.cbentry_type)
        self.server_type = 'Ruby'

        self.add_button("Save", gtk.RESPONSE_OK)
        self.add_button("Cancel", gtk.RESPONSE_CANCEL)

        self.show_all()
        return

    def set_type(self, entry):
        self.server_type = entry.get_text()
        return

    def get_name(self):
        return self.entry_name.get_text()

    def get_url(self):
        return self.entry_url.get_text()
		
    def get_type(self):
        return self.server_type
