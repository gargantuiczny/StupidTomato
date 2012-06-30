from sys import argv
from PySide.QtGui import QApplication
from core.window import Window
from settings import APP_NAME

app = QApplication(argv)
app.setApplicationName(APP_NAME)

window = Window()
window.show()

app.exec_()