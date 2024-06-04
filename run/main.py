import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget,
    QGridLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer


class OotdApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model_path = ""
        self.cloth_path = ""
        self.output_image_path = "D:/MediaAILab/Multimedia/OOTDiffusion/run/images_output/out_hd_0.png"
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Virtual Fitting')

        # Model and Cloth Labels
        self.model_label = QLabel('Model Path: Not Selected', self)
        self.model_label.setAlignment(Qt.AlignCenter)

        self.cloth_label = QLabel('Cloth Path: Not Selected', self)
        self.cloth_label.setAlignment(Qt.AlignCenter)

        # Scale and Sample Inputs
        self.scale_label = QLabel('Scale:', self)
        self.scale_input = QLineEdit(self)
        self.scale_input.setText("2.0")

        self.sample_label = QLabel('Sample:', self)
        self.sample_input = QLineEdit(self)
        self.sample_input.setText("1")

        # Buttons
        self.model_button = QPushButton('Select Model', self)
        self.model_button.clicked.connect(self.select_model)

        self.cloth_button = QPushButton('Select Cloth', self)
        self.cloth_button.clicked.connect(self.select_cloth)

        self.run_button = QPushButton('Run', self)
        self.run_button.clicked.connect(self.run_command)

        # Image Labels for displaying input and output images
        self.input_model_image_label = QLabel('Model Image', self)
        self.input_model_image_label.setAlignment(Qt.AlignCenter)
        self.input_model_image = QLabel(self)
        self.input_model_image.setAlignment(Qt.AlignCenter)
        self.input_model_image.setFixedSize(300, 300)  # 이미지 크기 조정
        self.input_model_image.setStyleSheet("border: 1px solid black;")  # 경계선 추가
        self.input_model_image.setScaledContents(True)  # 이미지가 QLabel 크기에 맞추어 조정되도록 설정

        self.input_cloth_image_label = QLabel('Cloth Image', self)
        self.input_cloth_image_label.setAlignment(Qt.AlignCenter)
        self.input_cloth_image = QLabel(self)
        self.input_cloth_image.setAlignment(Qt.AlignCenter)
        self.input_cloth_image.setFixedSize(300, 300)  # 이미지 크기 조정
        self.input_cloth_image.setStyleSheet("border: 1px solid black;")  # 경계선 추가
        self.input_cloth_image.setScaledContents(True)  # 이미지가 QLabel 크기에 맞추어 조정되도록 설정

        self.output_image_label = QLabel('Output Image', self)
        self.output_image_label.setAlignment(Qt.AlignCenter)
        self.output_image = QLabel(self)
        self.output_image.setAlignment(Qt.AlignCenter)
        self.output_image.setFixedSize(300, 300)  # 이미지 크기 조정
        self.output_image.setStyleSheet("border: 1px solid black;")  # 경계선 추가
        self.output_image.setScaledContents(True)  # 이미지가 QLabel 크기에 맞추어 조정되도록 설정

        # Loading Label
        self.loading_label = QLabel('', self)
        self.loading_label.setAlignment(Qt.AlignCenter)

        # Layouts
        grid_layout = QGridLayout()

        # Add images to the grid layout
        grid_layout.addWidget(self.input_model_image_label, 0, 0)
        grid_layout.addWidget(self.input_model_image, 1, 0)
        grid_layout.addWidget(self.input_cloth_image_label, 0, 1)
        grid_layout.addWidget(self.input_cloth_image, 1, 1)
        grid_layout.addWidget(self.output_image_label, 0, 2)
        grid_layout.addWidget(self.output_image, 1, 2)

        # Add controls to the grid layout
        grid_layout.addWidget(self.model_button, 2, 0)
        grid_layout.addWidget(self.cloth_button, 2, 1)
        grid_layout.addWidget(self.run_button, 2, 2)
        grid_layout.addWidget(self.model_label, 3, 0)
        grid_layout.addWidget(self.cloth_label, 3, 1)
        grid_layout.addWidget(self.scale_label, 4, 0)
        grid_layout.addWidget(self.scale_input, 4, 1)
        grid_layout.addWidget(self.sample_label, 5, 0)
        grid_layout.addWidget(self.sample_input, 5, 1)
        grid_layout.addWidget(self.loading_label, 4, 2, 2, 1)

        container = QWidget()
        container.setLayout(grid_layout)
        self.setCentralWidget(container)

        # Loading animation timer
        self.loading_timer = QTimer(self)
        self.loading_timer.timeout.connect(self.update_loading_text)
        self.loading_dots = 0

    def select_model(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Model File", "", "All Files (*);;PNG Files (*.png)",
                                                   options=options)
        if file_path:
            self.model_path = file_path
            self.model_label.setText(f'Model Path: {file_path}')
            pixmap = QPixmap(file_path)
            self.input_model_image.setPixmap(pixmap)

    def select_cloth(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Cloth File", "",
                                                   "All Files (*);;JPEG Files (*.jpg; *.jpeg)", options=options)
        if file_path:
            self.cloth_path = file_path
            self.cloth_label.setText(f'Cloth Path: {file_path}')
            pixmap = QPixmap(file_path)
            self.input_cloth_image.setPixmap(pixmap)

    def run_command(self):
        scale = self.scale_input.text()
        sample = self.sample_input.text()

        if not self.model_path or not self.cloth_path:
            print("Please select both model and cloth files.")
            return

        command = f'python run_ootd.py --model_path {self.model_path} --cloth_path {self.cloth_path} --scale {scale} --sample {sample}'
        print(f'Executing: {command}')

        self.run_button.setEnabled(False)  # Run 버튼 비활성화
        self.loading_label.setText('Loading.')
        self.loading_label.setStyleSheet('color: black')  # 초기 색상 설정
        self.loading_timer.start(1000)  # 1초마다 타이머 업데이트
        self.thread = CommandThread(command)
        self.thread.finished.connect(self.command_finished)
        self.thread.start()

    def update_loading_text(self):
        self.loading_dots = (self.loading_dots % 3) + 1
        self.loading_label.setText('Loading' + '.' * self.loading_dots)

    def command_finished(self, success):
        self.run_button.setEnabled(True)  # Run 버튼 다시 활성화
        self.loading_timer.stop()
        if success:
            print("Command executed successfully")
            if os.path.exists(self.output_image_path):
                pixmap = QPixmap(self.output_image_path)
                self.output_image.setPixmap(pixmap)
            self.loading_label.setText('Complete!')
            self.loading_label.setStyleSheet('color: green')
        else:
            print("Error executing command")
            self.loading_label.setText('Error occurred')
            self.loading_label.setStyleSheet('color: red')


class CommandThread(QThread):
    progress_changed = pyqtSignal(int)
    finished = pyqtSignal(bool)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        total_lines = 100  # 임의의 총 라인 수. 실제로는 적절한 값으로 설정해야 합니다.
        current_line = 0

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())  # 콘솔에 출력
                if "Progress" in output:
                    try:
                        progress = int(output.split("Progress")[1].strip().split('%')[0])
                        self.progress_changed.emit(progress)
                    except ValueError:
                        pass
                current_line += 1
                progress = int((current_line / total_lines) * 100)
                self.progress_changed.emit(progress)

        process.stdout.close()
        process.stderr.close()
        success = process.returncode == 0
        self.finished.emit(success)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OotdApp()
    ex.show()
    sys.exit(app.exec_())
