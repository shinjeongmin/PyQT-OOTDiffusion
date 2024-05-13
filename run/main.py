import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QLineEdit, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt


class OotdApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model_path = ""
        self.cloth_path = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle('OOTDiffusion')

        self.model_label = QLabel('Model Path: Not Selected', self)
        self.model_label.setAlignment(Qt.AlignCenter)

        self.cloth_label = QLabel('Cloth Path: Not Selected', self)
        self.cloth_label.setAlignment(Qt.AlignCenter)

        self.scale_label = QLabel('Scale:', self)
        self.scale_input = QLineEdit(self)
        self.scale_input.setText("2.0")

        self.sample_label = QLabel('Sample:', self)
        self.sample_input = QLineEdit(self)
        self.sample_input.setText("1")

        self.model_button = QPushButton('Select Model', self)
        self.model_button.clicked.connect(self.select_model)

        self.cloth_button = QPushButton('Select Cloth', self)
        self.cloth_button.clicked.connect(self.select_cloth)

        self.run_button = QPushButton('Run', self)
        self.run_button.clicked.connect(self.run_command)

        layout = QVBoxLayout()
        layout.addWidget(self.model_label)
        layout.addWidget(self.model_button)
        layout.addWidget(self.cloth_label)
        layout.addWidget(self.cloth_button)
        layout.addWidget(self.scale_label)
        layout.addWidget(self.scale_input)
        layout.addWidget(self.sample_label)
        layout.addWidget(self.sample_input)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_model(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Model File", "", "All Files (*);;PNG Files (*.png)",
                                                   options=options)
        if file_path:
            self.model_path = file_path
            self.model_label.setText(f'Model Path: {file_path}')

    def select_cloth(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Cloth File", "",
                                                   "All Files (*);;JPEG Files (*.jpg; *.jpeg)", options=options)
        if file_path:
            self.cloth_path = file_path
            self.cloth_label.setText(f'Cloth Path: {file_path}')

    def run_command(self):
        scale = self.scale_input.text()
        sample = self.sample_input.text()

        if not self.model_path or not self.cloth_path:
            print("Please select both model and cloth files.")
            return

        command = f'python run_ootd.py --model_path {self.model_path} --cloth_path {self.cloth_path} --scale {scale} --sample {sample}'
        print(f'Executing: {command}')

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        if process.returncode == 0:
            print("Command executed successfully")
            print(out.decode('utf-8'))
        else:
            print("Error executing command")
            print(err.decode('utf-8'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OotdApp()
    ex.show()
    sys.exit(app.exec_())
