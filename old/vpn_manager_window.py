import gi
import threading
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from vpn_manager import VpnManager
from common import ThreadedConnector
class ConnectionBox(Gtk.ListBox):
    def __init__(self):
        Gtk.ListBox.__init__(self)
        self.set_selection_mode(Gtk.SelectionMode.NONE)
        self.connection_button = Gtk.Button(label="Connect")
        self.connection_button.connect("clicked", self.connection_button_clicked)
        self.connection_label = Gtk.Label("Connection status:")
        self.connection_status_label = Gtk.Label("N/A")
        self.header = Gtk.Box()
        self.add(self.header)
        self.header.pack_start(self.connection_button, True, True, 0)
        self.header.pack_start(self.connection_label, True, True, 0)
        self.header.pack_start(self.connection_status_label, True, True, 0)
        self.manager = VpnManager(self)

    def notify(self, state, msg):
        self.connection_status_label.set_text(msg)

    def connection_button_clicked(self, widget):
        thread = ThreadedConnector(self.manager)
        thread.daemon = True
        thread.start() 

class VpnManagerWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="VPN Manager")
        self.set_size_request(640, 480)
        self.__init_layout()
        self.show_all()
        self.connect("delete-event", Gtk.main_quit)

    def __init_layout(self):
        self.connection_box = ConnectionBox()
        self.add(self.connection_box)

window = VpnManagerWindow()
Gtk.main()
