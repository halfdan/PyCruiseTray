import gtk
import sys

class BuildIcons:
    success = 'icon-success.png'
    failure = 'icon-failure.png'
    inactive = 'icon-inactive.png'
    building = 'icon-building.png'

    def __init__(self):
        self.icon_mapping = {
	    'Success.Sleeping': self.success,
	    'Success.CheckingModifications': self.success,
	    'Success.Building': self.building,
	    'Failure.Sleeping': self.failure, 
	    'Failure.CheckingModifications': self.failure,
	    'Failure.Building': self.building,
	    'Unknown.Sleeping': self.inactive,
	    'unavailable': self.inactive 
	}

    def get_icon(self, status):
        return gtk.gdk.pixbuf_new_from_file(sys.path[0] +"/icons/" + self.icon_mapping[status])
