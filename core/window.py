# -*- coding: utf-8 -*-
from functools import partial

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.phonon import Phonon

from commons.loaders import *
from .constants import *
from settings import *

class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        icon = get_icon(ICONS_DIR, ICON_NAME)
        self.player = Phonon.createPlayer(Phonon.NoCategory, get_sound(SOUNDS_DIR, SOUND_NAME))

        self.setWindowIcon(icon)
        self.setWindowTitle(APP_NAME)

        self.load_config()

        self.tomato_bar = QProgressBar(self)
        self.tomato_bar.setMaximum(self.tomato_duration)
        self.tomato_bar.setFormat(BAR_FORMAT)

        self.break_bar = QProgressBar(self)
        self.break_bar.setMaximum(self.break_duration)
        self.break_bar.setFormat(BAR_FORMAT)
        self.break_bar.hide()

        self.tomato_button = QPushButton(TOMATO_BUTTON_TEXT, self)
        self.tomato_button.clicked.connect(self.start_tomato)

        self.break_button = QPushButton(BREAK_BUTTON_TEXT, self)
        self.break_button.clicked.connect(self.start_break)
        self.break_button.hide()

        layout = QHBoxLayout(self)
        layout.addWidget(self.tomato_bar)
        layout.addWidget(self.break_bar)
        layout.addWidget(self.tomato_button)
        layout.addWidget(self.break_button)
        self.setLayout(layout)

        self.tomato_timer = QTimer()
        self.tomato_timer.timeout.connect(partial(self.increment_bar, self.tomato_bar, self.finish_tomato))

        self.break_timer = QTimer()
        self.break_timer.timeout.connect(partial(self.increment_bar, self.break_bar, self.finish_break))

        self.tray = QSystemTrayIcon(icon, self)
        self.tray.activated.connect(self.try_toogle_show)
        self.tray.show()


    def load_config(self):
        try:
            config = get_config(CONFIG_DIR, CONFIG_NAME)

            self.setGeometry(
                config.get(WINDOW_X_KEY, DEFAULT_WINDOW_X),
                config.get(WINDOW_Y_KEY, DEFAULT_WINDOW_Y),
                config.get(WINDOW_WIDTH_KEY, DEFAULT_WINDOW_WIDTH),
                config.get(WINDOW_HEIGHT_KEY, DEFAULT_WINDOW_HEIGHT)
            )

            self.tomato_duration = config.get(TOMATO_DURATION_KEY, DEFAULT_TOMATO_DURATION)
            self.break_duration = config.get(BREAK_DURATION_KEY, DEFAULT_BREAK_DURATION)
        except IOError: # Nie chcę, aby brak pliku wywoływał panikę.
            pass

    def start_tomato(self):
        self.tomato_button.hide()
        self.tomato_timer.start(ONE_SECOND)

    def finish_tomato(self):
        self.tomato_timer.stop()
        self.tomato_bar.reset()
        self.tomato_bar.hide()
        self.break_bar.show()
        self.break_button.show()
        self.player.play()
        self.tray.showMessage(TRAY_MESSAGE_TITLE, TRAY_FINISH_TOMATO_MESSAGE)

    def start_break(self):
        self.break_button.hide()
        self.break_timer.start(ONE_SECOND)

    def finish_break(self):
        self.break_timer.stop()
        self.break_bar.reset()
        self.break_bar.hide()
        self.tomato_bar.show()
        self.tomato_button.show()
        self.player.play()
        self.tray.showMessage(TRAY_MESSAGE_TITLE, TRAY_FINISH_BREAK_MESSAGE)

    def increment_bar(self, bar, task):
        value = bar.value() + 1

        if value == bar.maximum():
            task()
        else:
            bar.setValue(value)

    def closeEvent(self, event):
        save_config(CONFIG_DIR, CONFIG_NAME, {
            WINDOW_X_KEY : self.x(),
            WINDOW_Y_KEY : self.y(),
            WINDOW_WIDTH_KEY : self.width(),
            WINDOW_HEIGHT_KEY : self.height(),
            TOMATO_DURATION_KEY : self.tomato_duration,
            BREAK_DURATION_KEY : self.break_duration
        })
        super(Window, self).closeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
            qApp.quit()
        else:
            super(Window, self).keyPressEvent(event)

    def hideEvent(self, event):
        self.hide()
        super(Window, self).hideEvent(event)

    def try_toogle_show(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.setWindowState(Qt.WindowActive)
            self.toggle_show()

    def toggle_show(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()

if __name__ == '__main__':
    from sys import argv
    from PySide.QtGui import QApplication

    app = QApplication(argv)
    app.setApplicationName(APP_NAME)

    window = Window()
    window.show()

    app.exec_()
