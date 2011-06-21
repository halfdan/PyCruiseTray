import webbrowser
import gtk
from settings_dialog import SettingsDialog

class ContextMenu(gtk.Menu):
    def __init__(self, main_window, build_icons):
        super(ContextMenu, self).__init__()
        self.main_window = main_window
        self.build_icons = build_icons
        self.__create_default_menus()

    def __create_default_menus(self):
        about = gtk.ImageMenuItem(gtk.STOCK_ABOUT, "About")
        settings = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES, "Preferences")
        quit = gtk.ImageMenuItem(gtk.STOCK_QUIT, "Quit")
        
        about.connect("activate", self.show_about_dialog)
        settings.connect("activate", self.show_settings_dialog)
        quit.connect("activate", gtk.main_quit)
        
        self.append(about)
        self.append(settings)
        self.append(quit)
        self.show_all()

    def clear(self):
        for i in self.get_children():
            self.remove(i)

    def update(self, projects):
        self.clear()
        for project in projects:
            # Fetch our icon according to the build status
            icon = self.build_icons.get_icon(project.get_build_status())
            image = gtk.image_new_from_pixbuf(icon)
            # Create new ImageMenuItem
            menu_item = gtk.ImageMenuItem()
            menu_item.set_label(project.name)
            menu_item.set_image(image)
            # Open up webbrowser on click
            proc = lambda ignore,url=project.url: self.open_url(url)
            menu_item.connect("activate", proc)
            self.append(menu_item)

        self.append(gtk.SeparatorMenuItem())
        self.__create_default_menus()
        self.show_all()


    def open_url(self, url):
        webbrowser.open(url)


    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("PyCruiseTray")
        about_dialog.set_version("1.0")
        about_dialog.set_website("https://github.com/halfdan/PyCruiseTray")
        about_dialog.set_authors(["Fabian Becker"])

        about_dialog.run()
        about_dialog.destroy()

    def show_settings_dialog(self, widget):
        settings_dialog = SettingsDialog()
        settings_dialog.run()
        settings_dialog.destroy()
