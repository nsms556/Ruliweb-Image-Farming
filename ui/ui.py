from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
from PyQt5.QtCore import QCoreApplication
from PyQt5 import uic

ui_class = uic.loadUiType('ui/window.ui')[0]

class DisplayWindow(QMainWindow, ui_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.folder_change.clicked.connect(self.target_change)
        self.bt_close.clicked.connect(QCoreApplication.instance().quit)

    def target_change(self) :
        new_target = QFileDialog.getExistingDirectory(self, 'Select Directory')

        if new_target :
            self.folder_edit.setText(new_target)

    def reset_progress(self) :
        self.progress_bar.reset()

    def change_progress(self, value) :
        self.progress_bar.setValue(value)

if __name__ == '__main__' :
    import sys

    app = QApplication(sys.argv)
    
    window = DisplayWindow()
    window.show()

    app.exec_()