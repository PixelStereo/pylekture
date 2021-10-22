import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *


from collections import defaultdict
from functools import cached_property


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(188, 267)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(50, 140, 75, 24))
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(30, 40, 104, 71))
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, parent=None)
        self.dragPos = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.register("device_viewer", self.ui.textEdit)
        # self.register("another_key", another_textedit)

    def register(self, key, textedit):
        if not isinstance(textedit, QTextEdit):
            raise TypeError(f"{textedit} must be a QTextEdit")
        self.registry_viewers[key].append(textedit)

    @cached_property
    def registry_viewers(self):
        return defaultdict(list)

    @Slot(str, str)
    def update_text(self, key, value):
        for textedit in self.registry_viewers[key]:
            textedit.setText(textedit.toPlainText() + value)
            textedit.verticalScrollBar().setValue(
                textedit.verticalScrollBar().maximum()
            )


class Account(QThread):
    textUpdate = Signal(str, str)

    def run(self):
        print("thread is work")
        self.textUpdate.emit("device_viewer", "Connect to device\n")
        # self.textUpdate.emit("another_key", "message")


if __name__ == "__main__":
    app = QApplication()

    main = MainWindow()
    acc_instance = Account()

    #acc_instance.textUpdate.connect(main.update_text)
    #main.ui.pushButton.clicked.connect(acc_instance.start)

    sys.exit(app.exec())