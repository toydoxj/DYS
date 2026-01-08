import sys
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget

class Page1(QWidget):
    updateLabelText = pyqtSignal(str)  # 시그널 정의

    def __init__(self, stackedWidget):
        super().__init__()
        self.stackedWidget = stackedWidget

        layout = QVBoxLayout()
        self.textEdit = QPushButton("텍스트 변경")
        self.textEdit.clicked.connect(self.changeText)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)

    def changeText(self):
        new_text = "텍스트가 변경되었습니다."
        # 페이지 2로 시그널을 보내어 레이블 텍스트를 변경
        self.updateLabelText.emit(new_text)

class Page2(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.label = QLabel("이곳에 텍스트가 표시됩니다.")
        layout.addWidget(self.label)
        self.setLayout(layout)

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Stacked Widget 예제")

        self.stackedWidget = QStackedWidget()

        # 페이지 1과 페이지 2 생성
        self.page1 = Page1(self.stackedWidget)
        self.page2 = Page2()

        self.stackedWidget.addWidget(self.page1)
        self.stackedWidget.addWidget(self.page2)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.stackedWidget)
        self.setLayout(mainLayout)

        # 페이지 1에서 페이지 2로 텍스트 업데이트를 위한 시그널/슬롯 연결
        self.page1.updateLabelText.connect(self.page2.label.setText)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
