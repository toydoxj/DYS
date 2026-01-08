from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QPropertyAnimation, Qt
from PyQt6.QtWidgets import QAbstractItemView

import rc_resource


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1700,650)
        MainWindow.setWindowIcon(QtGui.QIcon('icons\icons.png'))

       # Centralwidget
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: #007e8e; \n") 
                                        
        # 1차 정렬
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # mainbody 구성 
        self.mainbody = QtWidgets.QWidget(parent=self.centralwidget)
        self.mainbody.setObjectName("mainbody")
        self.mainbody.setStyleSheet("background-color:#fefefe;")

        # header 구성
        self.headerFrame = QtWidgets.QWidget(parent=self.mainbody)
        self.headerFrame.setMinimumSize(QtCore.QSize(0, 40))
        self.headerFrame.setObjectName("headerFrame")
        self.headerFrame.setStyleSheet("QWidget#headerFrame { border-bottom: 1px solid black; border-right: none; border-top: none; border-left: none; } QLabel#Title_Label { border: none; }\n"
                                       "QPushButton {border-color:#cfcfcf; border-style:solid; border-width: 1px;}\n"
                                       "QPushButton:hover {background-color:#007e8e; color:white ;}")
        # hearder 내용 입력
        self.horizontalLayout_header = QtWidgets.QHBoxLayout(self.headerFrame)

        # Label
        self.Title_Label = QtWidgets.QLabel(parent=self.headerFrame)
        self.Title_Label.setObjectName("Title_Label")
        self.Title_Label.setText('Project Information')
        self.Title_Label.setFixedSize(600,25)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(50)
        self.Title_Label.setFont(font)

        # Button
        btn_FileNew = QtWidgets.QPushButton(parent=self.headerFrame)
        btn_FileNew.setText('New')
        btn_FileNew.setFixedSize(100,25)
        btn_FileNew.clicked.connect(lambda: self.on_click_New(page1,page2))
       
        btn_FileOpen = QtWidgets.QPushButton(parent=self.headerFrame)
        btn_FileOpen.setText('Open')
        btn_FileOpen.setFixedSize(100,25)
        btn_FileOpen.clicked.connect(lambda: self.on_click_FileOpen(page1, page2))

        btn_FileSave = QtWidgets.QPushButton(parent=self.headerFrame)
        btn_FileSave.setText('Save')
        btn_FileSave.setFixedSize(100,25)
        btn_FileSave.clicked.connect(lambda: self.on_click_FileSave(page1, page2))

        btn_FileSaveAs = QtWidgets.QPushButton(parent=self.headerFrame)
        btn_FileSaveAs.setText('SaveAs')
        btn_FileSaveAs.setFixedSize(100,25)
        btn_FileSaveAs.clicked.connect(lambda: self.on_click_FileSaveAs(page1, page2))

        spacerItem_header = QtWidgets.QSpacerItem(350, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)

        self.horizontalLayout_header.addWidget(self.Title_Label)
        self.horizontalLayout_header.addWidget(btn_FileNew)
        self.horizontalLayout_header.addWidget(btn_FileOpen)
        self.horizontalLayout_header.addWidget(btn_FileSave)
        self.horizontalLayout_header.addWidget(btn_FileSaveAs)
        self.horizontalLayout_header.addItem(spacerItem_header)
        
        
        # mainFrame 구성
        self.mainFrame = QtWidgets.QWidget(parent=self.mainbody)
        self.mainFrame.setObjectName("mainFrame")

        # Footer Frame 구성
        self.cardsFrame = QtWidgets.QWidget(parent=self.mainbody)
        self.cardsFrame.setMinimumSize(QtCore.QSize(0, 40))
        self.cardsFrame.setObjectName("cardsFrame")
        self.cardsFrame.setStyleSheet("QWidget#cardsFrame { border-top: 1px solid black; border-right: none; border-bottom: none; border-left: none; } QLabel#myLabel { border: none; }")

        # Footer 내용 입력
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.cardsFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        #Copyright
        self.label_Copyright = QtWidgets.QLabel(parent=self.cardsFrame)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_Copyright.setFont(font)
        self.label_Copyright.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_Copyright.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft)
        self.label_Copyright.setObjectName("label_Copyright")

        #Spacer
        spacerItem8 = QtWidgets.QSpacerItem(350, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        
        #Dongyang LOGO
        self.label_Dylogo = QtWidgets.QLabel(parent=self.cardsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Dylogo.sizePolicy().hasHeightForWidth())
        self.label_Dylogo.setSizePolicy(sizePolicy)
        self.label_Dylogo.setMaximumSize(QtCore.QSize(130, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(True)
        self.label_Dylogo.setFont(font)
        self.label_Dylogo.setText("")
        self.label_Dylogo.setPixmap(QtGui.QPixmap(":/logo/Icons/logo/DY-S.png"))
        self.label_Dylogo.setObjectName("label_Dylogo")
        

        self.horizontalLayout_2.addWidget(self.label_Copyright)
        self.horizontalLayout_2.addItem(spacerItem8)
        self.horizontalLayout_2.addWidget(self.label_Dylogo)

        # Frame 정렬
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainbody)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(self.headerFrame)
        self.verticalLayout.addWidget(self.mainFrame)
        self.verticalLayout.addWidget(self.cardsFrame)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.mainFrame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        #STACK
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.mainFrame)
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.stackedWidget.setLineWidth(0)
        self.stackedWidget.setObjectName("stackedWidget")
        
        self.verticalLayout_3.addWidget(self.stackedWidget)

        # 좌측 Frame 함수 호출
        self.leftmargin = LeftMargin(parent=self.centralwidget) # 좌측 여백 Frame
        self.leftmargin.setObjectName('leftmargin')

        self.leftMenu = LeftMenu(parent=self.centralwidget) # 메뉴 Frame
        self.leftMenu.setObjectName('leftMenu')
        self.leftMenu.setStyleSheet("background-color:#007e8e;")
        
        # 1차 정렬
        self.horizontalLayout.addWidget(self.leftmargin)
        self.horizontalLayout.addWidget(self.leftMenu)
        self.horizontalLayout.addWidget(self.mainbody)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DY-Module - ver0.0.1(beta)"))
        self.label_Copyright.setText(_translate("MainWindow", "Copyright 2023. Jeong Jihun, jjh@dyce.kr"))

class LeftMargin(QtWidgets.QWidget):
    ''' 
    좌측 여백 
    폭 20px
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setStyleSheet(' background-color: #007e8e; ')
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(20, 0))
        self.setMaximumSize(QtCore.QSize(20, 16777215))

class LeftMenu(QtWidgets.QWidget):
    ''' 
    메뉴창
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stackedWidget = parent.findChild(QtWidgets.QStackedWidget, "stackedWidget")
        self.label = parent.findChild(QtWidgets.QLabel, "Title_Label")
        
        self.setMinimumSize(QtCore.QSize(40, 0))
        self.setMaximumSize(QtCore.QSize(40, 16777215))
        self.Anim_menu()
        self.setStyleSheet("QPushButton { background-color:#007e8e; border-style:solid; text-align: left; color:#fefeff; padding:5px; }\n"
                            "QPushButton#BtnGL:hover{ border-color:#fefeff; border-style:solid; border-width: 2px; \n"
                                                            " text-align: left; color:#000000; padding:5px; }\n"
                                    "QPushButton#BtnWL:hover{  border-color:#fefeff; border-style:solid; border-width: 2px; \n"
                                                            " text-align: left; color:#000000; padding:5px; }\n"
                                    "QPushButton#BtnEL:hover{  border-color:#fefeff; border-style:solid; border-width: 2px; \n"
                                                            "; text-align: left; color:#000000; padding:5px; }\n"
                                    "QPushButton#BtnLC:hover{  border-color:#fefeff; border-style:solid; border-width: 2px; \n"
                                                            " text-align: left; color:#000000; padding:5px; }\n"
                                    "QPushButton#BtnInfo:hover{ border-color:#fefeff; border-style:solid; border-width: 2px; \n"                                    
                                                            " text-align: left; color:#000000; padding:5px; }")

        
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)

        # 메뉴 펼침 버튼
        self.BtnMenu = QtWidgets.QPushButton(parent=self)
        self.BtnMenu.clicked.connect(self.Anim_menu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BtnMenu.sizePolicy().hasHeightForWidth())

        self.BtnMenu.setSizePolicy(sizePolicy)
        self.BtnMenu.setMinimumSize(QtCore.QSize(0, 50))
        self.BtnMenu.setMaximumSize(QtCore.QSize(16777215, 50))

        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.BtnMenu.setFont(font)
        self.BtnMenu.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.PreventContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/White_Icon/Icons/white/iconmonstr-menu-1-240 (1).png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.BtnMenu.setIcon(icon)
        self.BtnMenu.setIconSize(QtCore.QSize(24, 24))
        self.BtnMenu.setObjectName("BtnMenu")
        self.verticalLayout_2.addWidget(self.BtnMenu)

        # Sapcer
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)
        self.BtnGL = QtWidgets.QPushButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BtnGL.sizePolicy().hasHeightForWidth())

        # Input 버튼
        self.BtnGL.setSizePolicy(sizePolicy)
        self.BtnGL.setMaximumSize(QtCore.QSize(16777215, 30))
        self.BtnGL.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.BtnGL.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/White_Icon/Icons/white/iconmonstr-construction-10-240.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.BtnGL.setIcon(icon1)
        self.BtnGL.setIconSize(QtCore.QSize(24, 24))
        self.BtnGL.setObjectName("BtnGL")
        self.BtnGL.clicked.connect(lambda: self.change_widget(1))
        self.verticalLayout_2.addWidget(self.BtnGL)

        # Spacer
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_2.addItem(spacerItem2)

        # Check-Midas 버튼
        self.BtnWL = QtWidgets.QPushButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BtnWL.sizePolicy().hasHeightForWidth())
        self.BtnWL.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.BtnWL.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/White_Icon/Icons/white/iconmonstr-weather-64-240.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.BtnWL.setIcon(icon2)
        self.BtnWL.setIconSize(QtCore.QSize(24, 24))
        self.BtnWL.setObjectName("BtnWL")
        self.BtnWL.clicked.connect(lambda: self.change_widget(2))
        self.verticalLayout_2.addWidget(self.BtnWL)

        # Spacer
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_2.addItem(spacerItem3)

        # 지진하중 버튼
        self.BtnEL = QtWidgets.QPushButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BtnEL.sizePolicy().hasHeightForWidth())
        self.BtnEL.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.BtnEL.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/White_Icon/Icons/white/iconmonstr-sound-wave-8-240.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.BtnEL.setIcon(icon3)
        self.BtnEL.setIconSize(QtCore.QSize(24, 24))
        self.BtnEL.setObjectName("BtnEL")
        self.BtnEL.clicked.connect(lambda: self.change_widget(3))
        self.verticalLayout_2.addWidget(self.BtnEL)

        

        # Spacer
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)


        self.retranslateUi(MainWindow)

    def Anim_menu(self):
        width = self.width()
        normal = 40
        if width == normal:
            extender = 210            
        else:
            extender = normal
        self.anim = QPropertyAnimation(self, b"minimumWidth")  # 속성 이름을 변경한 변수를 사용합니다.
        self.anim.setDuration(100)
        self.anim.setStartValue(width)
        self.anim.setEndValue(extender)
        self.anim.start()

    def retranslateUi(self, MainWidow):
        _translate = QtCore.QCoreApplication.translate
        self.BtnMenu.setText(_translate("MainWindow", "  DY-Module"))
        self.BtnGL.setText(_translate("MainWindow", "  Input"))
        self.BtnWL.setText(_translate("MainWindow", "  Check-Midas"))
        self.BtnEL.setText(_translate("MainWindow", "  Result"))


        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())