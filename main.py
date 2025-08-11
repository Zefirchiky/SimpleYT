from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QCheckBox,
)


class App:
    def __init__(self):
        self.app = QApplication()
        self.app.setApplicationName('YtDownloader')
        self.window = QMainWindow()
        self.window.resize(500, 100)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Url of YouTube video")
        self.url_input.setFixedHeight(25)
        
        self.video_selection_checkbox = QCheckBox()
        self.video_selection_checkbox.setFixedWidth(17)
        self.video_selection_checkbox.setChecked(False)

        self.audio_selection_checkbox = QCheckBox()
        self.audio_selection_checkbox.setFixedWidth(17)
        self.audio_selection_checkbox.setChecked(True)
        
        self.download_button = QPushButton("Download")
        self.download_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.download_button.setFixedHeight(30)
        self.download_button.setFixedWidth(100)
        
        self.download_layout = QHBoxLayout()
        self.download_layout.setContentsMargins(5, 0, 5, 0)
        self.download_layout.addWidget(QLabel('Video:'))
        self.download_layout.addWidget(self.video_selection_checkbox)
        self.download_layout.addSpacing(15)
        self.download_layout.addWidget(QLabel('Audio:'))
        self.download_layout.addWidget(self.audio_selection_checkbox)
        self.download_layout.addStretch(1)
        self.download_layout.addWidget(self.download_button)

        self.root_layout = QVBoxLayout()
        self.root_layout.addWidget(self.url_input)
        self.root_layout.addLayout(self.download_layout)

        self.root = QWidget()
        self.root.setLayout(self.root_layout)

        self.window.setCentralWidget(self.root)

    def run(self):
        self.window.show()
        self.app.exec()


if __name__ == "__main__":
    app = App()
    app.run()
