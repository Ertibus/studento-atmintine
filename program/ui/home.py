from PyQt5.QtWidgets import *
from program.ui import Message
from datetime import datetime
from PyQt5.QtCore import QDateTime, Qt
from program.repo import NewRepository
import sys
import pyperclip

class Home():
    def __init__(self, body: QLayout, navigator):
        self.navigator = navigator
        self.body = body
        self.init_ui()

    def init_ui(self):
        def _new():
            self.navigator(Message.new_event)

        def _exit():
            sys.exit(0)
            print("Exit")

        wrapper = QGridLayout()
        wrapper.setColumnStretch(1, 1)
        self.body.addLayout(wrapper)

        button_layout = QVBoxLayout()

        #
        btn_new = QPushButton("New")
        btn_new.clicked.connect(_new)
        button_layout.addWidget(btn_new)
        button_layout.addStretch()

        btn_quit = QPushButton("Quit")
        btn_quit.clicked.connect(_exit)
        button_layout.addWidget(btn_quit)
        #

        scroll = QScrollArea()
        event_layout = QVBoxLayout()

        for event in NewRepository.get_event_list():
            event_layout.addWidget(TrackedEvent(
                event[0],
                event[1],
                event[2],
                event[3],
            ).get_widget())

        event_layout.addStretch()


        button_box = QGroupBox()
        button_box.setLayout(button_layout)

        event_box = QWidget()
        event_box.setLayout(event_layout)

        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(event_box)

        wrapper.addWidget(button_box, 0, 0, 1, 1)
        wrapper.addWidget(scroll, 0, 1, 1, 1)


class TrackedEvent():
    def __init__(self, title: str, description: str, deadline: str, my_id: int):
        self.my_id = my_id
        self.title = title
        self.description = description
        self.deadline = deadline


    def get_widget(self,):
        def _copy():
            pyperclip.copy("Title: {}\n\
            {}\n\
            Description: {}\n".format(lbl_title.text(), deadline_lbl.text(), desc.text()))
            pass


        def _edit():
            def _cancel():
                title_edit.deleteLater()
                desc_edit.deleteLater()
                btn_cancel.deleteLater()
                btn_save.deleteLater()
                deadline_picker.deleteLater()

                lbl_title.setHidden(False)
                desc.setHidden(False)
                deadline_lbl.setHidden(False)
                btn_copy.setHidden(False)
                btn_edit.setHidden(False)
                btn_delete.setHidden(False)


            def _save():
                try:
                    NewRepository.update_event(self.my_id, title_edit.text(), desc_edit.toPlainText(), deadline_picker.text())
                except Exception as err:
                    print(err)
                    QMessageBox.critical(None, "Error", str(err))
                else:
                    lbl_title.setText(title_edit.text())
                    desc.setText(desc_edit.toPlainText())
                    deadline_lbl.setText("Deadline: {}".format(deadline_picker.text()))
                    _cancel()


            title_edit = QLineEdit()
            title_edit.setText(lbl_title.text())
            widget_layout.addWidget(title_edit, 0, 0, 1, 1)

            desc_edit = QTextEdit()
            desc_edit.setText(desc.text())
            widget_layout.addWidget(desc_edit, 1, 0, 7, 7)

            deadline_picker = QDateTimeEdit()
            date_str = self.deadline.split(" ")
            date_date = date_str[0].split("-")
            date_time = date_str[1].split(":")
            deadline_picker.setDateTime(QDateTime(int(date_date[0]), int(date_date[1]), int(date_date[2]), int(date_time[0]), int(date_time[1])))
            deadline_picker.setCalendarPopup(True)
            deadline_picker.setDisplayFormat("yyyy-MM-dd HH:mm")
            widget_layout.addWidget(deadline_picker, 0, 1, 1, 1)


            btn_cancel = QPushButton("Cancel")
            btn_cancel.clicked.connect(_cancel)
            btn_cancel.setFixedWidth(51)
            widget_layout.addWidget(btn_cancel, 0, 5, 1, 1)

            btn_save = QPushButton("Save")
            btn_save.clicked.connect(_save)
            btn_save.setFixedWidth(51)
            widget_layout.addWidget(btn_save, 0, 6, 1, 1)

            lbl_title.setHidden(True)
            desc.setHidden(True)
            deadline_lbl.setHidden(True)
            btn_copy.setHidden(True)
            btn_edit.setHidden(True)
            btn_delete.setHidden(True)

        def _delete():
            NewRepository.delete_event(self.my_id)
            btn_box.deleteLater()


        widget_layout = QGridLayout()

        lbl_title = QLabel(self.title.upper())
        lbl_title.setStyleSheet("font-weight: bold")
        widget_layout.addWidget(lbl_title, 0, 0, 1, 1)

        widget_layout.setColumnStretch(0, 1)

        deadline_lbl = QLabel(f"Deadline: {self.deadline}")
        widget_layout.addWidget(deadline_lbl, 0, 1, 1, 1)

        # [ Buttons ]

        btn_copy = QPushButton("C")
        btn_copy.setFixedWidth(32)
        btn_copy.clicked.connect(_copy)
        widget_layout.addWidget(btn_copy, 0, 5, 1, 1)
        btn_edit = QPushButton("E")
        btn_edit.setFixedWidth(32)
        btn_edit.clicked.connect(_edit)
        widget_layout.addWidget(btn_edit, 0, 6, 1, 1)
        btn_delete = QPushButton("D")
        btn_delete.setFixedWidth(32)
        btn_delete.clicked.connect(_delete)
        widget_layout.addWidget(btn_delete, 0, 7, 1, 1)

        desc = QLabel(self.description)
        desc.setStyleSheet("color: #666666")
        desc.setWordWrap(True)
        widget_layout.addWidget(desc, 1, 0, 7, 7)

        btn_box = QGroupBox()
        btn_box.setLayout(widget_layout)

        return btn_box
