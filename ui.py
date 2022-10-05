import json
from getpass import getuser

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from farmer import resource_path
import utils.static as static


ui = resource_path(static.UI_FILE_DIR)
ui_class = uic.loadUiType(ui)[0]

class DisplayWindow(QMainWindow, ui_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(resource_path(static.ICON_DIR)))

        self.default_target = static.DEFAULT_TARGET.format(getuser())
        self.config = self.load_config()

        self.folder_edit.setText(self.config['target_dir'] if self.config['target_dir'] else self.default_target)

        self.folder_change.clicked.connect(self.target_change)
        self.bt_close.clicked.connect(self.close_event)

    def load_config(self) :
        with open(resource_path(static.CONFIG_DIR), 'r') as f :
            config_dict = json.load(f)

        return config_dict

    def save_config(self) :
        with open(resource_path(static.CONFIG_DIR), 'w') as f :
            json.dump(self.config, f)

    def target_change(self) :
        new_target = QFileDialog.getExistingDirectory(self, 'Select Directory')

        if new_target :
            self.folder_edit.setText(new_target)
            self.config['target_dir'] = new_target

    def reset_progress(self) :
        self.progress_bar.reset()

    def change_progress(self, value) :
        self.progress_bar.setValue(value)

    def close_event(self) :
        self.save_config()
        
        return QCoreApplication.instance().quit()

if __name__ == '__main__' :
    import sys

    app = QApplication(sys.argv)
    
    window = DisplayWindow()
    window.show()

    app.exec_()