import pygtk, gtk
import pynotify
import gobject

pygtk.require('2.0')

from context_menu import ContextMenu
from build_icons import BuildIcons
from project import CruiseControlServer
from server_manager import ServerManager

gobject.threads_init()

class PyCruiseTray(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)

        pynotify.init('PyCruiseTray')

        # Create ServerManager
        self.server_manager = ServerManager()

        # Load servers
        self.load_servers()

        # Load BuildIcons
        self.build_icons = BuildIcons()

        self.statusicon = gtk.StatusIcon()
        self.statusicon.set_from_stock(gtk.STOCK_APPLY)
        self.statusicon.connect("popup-menu", self.right_click_event)
        self.statusicon.connect("activate", self.status_clicked)
        self.statusicon.set_tooltip("PyCruiseTray")

        self.connect("delete-event", self.delete_event)
        self.connect("destroy", lambda w: gtk.main_quit())

        # Create TreeStore for Server list
        self.liststore = gtk.ListStore(gtk.gdk.Pixbuf, str, str)
        self.treeview = gtk.TreeView(self.liststore)

        # Create TreeViewColumns to display data
        cell = gtk.CellRendererPixbuf()
        col = gtk.TreeViewColumn("Status", cell, pixbuf=0)
        self.treeview.append_column(col)

        cell = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Name", cell, text=1)
        self.treeview.append_column(col)

        cell = gtk.CellRendererText()
        col = gtk.TreeViewColumn("URL", cell, text=2)
        self.treeview.append_column(col)

        self.add(self.treeview)
        self.set_size_request(450, 300)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title("PyCruiseTray")

        self.menu = ContextMenu(self, self.build_icons)
        self.show_all()

        # Start update thread (run every 5 minutes)
        self.update_projects()
        self.thread = gobject.timeout_add(60000, self.update_projects)

    def load_servers(self):
        self.servers = []
        for server in self.server_manager.list():
            self.servers.append(CruiseControlServer(server['name'], server['url']))

    def update_projects(self):
        projects = []
        for server in self.servers:
            server.load_projects()
            projects.extend(server.projects)

        self.show_projects_list(projects)
        self.menu.update(projects)
        failures = filter((lambda p: 'Failure' in p.get_build_status()), projects)


        # Change StatusIcon accordingly
        if len(failures) > 0:
            self.statusicon.set_from_pixbuf(self.build_icons.get_icon('Failure.Sleeping'))
        else:
            self.statusicon.set_from_pixbuf(self.build_icons.get_icon('Success.Sleeping'))

        for fail in failures:
            notification = pynotify.Notification("Build failure", "Project %s failed to build!" % fail.name)
            notification.attach_to_status_icon(self.statusicon)
            notification.set_urgency(pynotify.URGENCY_CRITICAL)
            notification.set_timeout(10000)
            notification.show()
        return True

    def show_projects_list(self, projects):
        self.liststore.clear()
        for project in projects:
            icon = self.build_icons.get_icon(project.get_build_status())
            self.liststore.append([icon, project.name, project.url])

    def status_clicked(self, status):
        self.show_all()

    def delete_event(self, window, event):
        self.hide_on_delete()
        return True
		
    def right_click_event(self, icon, button, time):
        self.menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.statusicon)
        
if __name__ == '__main__':
    PyCruiseTray()
    gtk.main()
