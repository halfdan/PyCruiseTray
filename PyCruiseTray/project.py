import urllib
from xml.dom import minidom

class Project:
    def __init__(self, project):
        self.name = project['name']
        self.activity = project['activity']
        self.status = project['lastBuildStatus']
        self.url = project['webUrl']
        self.buildTime = project['lastBuildTime']

    def get_build_status(self):
        return self.status + "." + self.activity


class CruiseControlServer:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def load_projects(self):
        self.projects = []
        try:
            xml = minidom.parse(urllib.urlopen(self.url))
            for node in xml.getElementsByTagName('Project'):
                self.projects.append(Project({
                    'webUrl': node.getAttribute('webUrl'),
                    'lastBuildStatus': node.getAttribute('lastBuildStatus'),
                    'lastBuildTime': node.getAttribute('lastBuildTime'),
                    'name': node.getAttribute('name'),
                    'activity': node.getAttribute('activity')
                }))
        except IOError:
            print "Cannot connect to server %s" % self.name
