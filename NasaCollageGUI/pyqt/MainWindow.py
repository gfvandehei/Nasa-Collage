from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMainWindow
from PyQt5.QtWidgets import *
from NasaCollageGUI.model.pythonstatusjson import PythonStatusJson

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.task_manager = PythonStatusJson()
        self.setWindowTitle("Nasa Collage Creator")
        self.arguments = {}

        self.combobox = QComboBox()
        self.combobox.addItems(["GetThumbsList", "DownloadImages"])
        self.combobox.currentIndexChanged.connect(self.on_choose_method)
        self.args_container = QWidget()
    def on_choose_method(self, method_name):
        if method_name == "GetThumbsList":

