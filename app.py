import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

import farmer
from ui import DisplayWindow


class Application(DisplayWindow) :
    def __init__(self):
        super().__init__()

        self.ori_size = True
        self.post_url = ""

        self.bt_dl.clicked.connect(self.bt_dl_func)
        self.radio_original.clicked.connect(self.size_radio_func)
        self.radio_resize.clicked.connect(self.size_radio_func)

    def size_radio_func(self) :
        if self.radio_original.isChecked() :
            self.ori_size = True
        elif self.radio_resize.isChecked() :
            self.ori_size = False

    def bt_dl_func(self) :
        self.change_progress(0)

        self.post_url = self.url_edit.text()

        img_urls = farmer.parsing_image_urls(self.post_url, self.ori_size)
        img_count = len(img_urls)

        if img_count == 0 :
            QMessageBox.critical(self, '짤이 없음', '다운로드할 짤이 없습니다')
        else :
            for i, url in enumerate(img_urls) :
                farmer.download_image(url, self.folder_edit.text())

                self.change_progress(self.calc_progress(i, img_count))

    def calc_progress(self, now, total) :
        return int((now+1) / total * 100)

if __name__ == '__main__' :
    app = QApplication(sys.argv)

    window = Application()
    window.show()

    app.exec_()