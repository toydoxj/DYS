from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt
from controllers.project_controller import ProjectController
from controllers.load_controller import LoadController
from .pages.info_page import InfoPage
from .pages.gravity_load_page import GravityLoadPage
from .pages.wind_load_page import WindLoadPage

class MainWindow(QtWidgets.QMainWindow):
    """메인 윈도우 클래스"""
    
    def __init__(self, project_controller: ProjectController, load_controller: LoadController):
        super().__init__()
        self.project_controller = project_controller
        self.load_controller = load_controller
        
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """UI 초기 설정"""
        # 기본 윈도우 설정
        self.setWindowTitle("DYL - ver0.0.2(beta)")
        self.resize(1700, 650)
        self.setWindowIcon(QtGui.QIcon('icons/icons.png'))
        
        # 중앙 위젯 설정
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 메인 레이아웃
        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 좌측 메뉴 설정
        self.setup_left_menu()
        
        # 메인 컨텐츠 영역 설정
        self.setup_main_content()
        
    def setup_left_menu(self):
        """좌측 메뉴 설정"""
        # 좌측 메뉴 프레임
        self.left_menu = QtWidgets.QFrame()
        self.left_menu.setMaximumWidth(200)
        self.left_menu.setMinimumWidth(40)
        self.left_menu.setStyleSheet("background-color: #007e8e;")
        
        # 메뉴 레이아웃
        menu_layout = QtWidgets.QVBoxLayout(self.left_menu)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(0)
        
        # 메뉴 버튼들
        self.btn_info = self.create_menu_button("Project Info", "icons/info.png")
        self.btn_gravity = self.create_menu_button("Gravity Load", "icons/gravity.png")
        self.btn_wind = self.create_menu_button("Wind Load", "icons/wind.png")
        self.btn_earthquake = self.create_menu_button("Earthquake Load", "icons/earthquake.png")
        self.btn_combination = self.create_menu_button("Load Combination", "icons/combination.png")
        
        # 버튼 추가
        menu_layout.addWidget(self.btn_info)
        menu_layout.addWidget(self.btn_gravity)
        menu_layout.addWidget(self.btn_wind)
        menu_layout.addWidget(self.btn_earthquake)
        menu_layout.addWidget(self.btn_combination)
        menu_layout.addStretch()
        
        self.main_layout.addWidget(self.left_menu)
        
    def setup_main_content(self):
        """메인 컨텐츠 영역 설정"""
        # 메인 컨텐츠 프레임
        self.main_content = QtWidgets.QFrame()
        self.main_content.setStyleSheet("background-color: #ffffff;")
        
        # 컨텐츠 레이아웃
        content_layout = QtWidgets.QVBoxLayout(self.main_content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # 헤더 프레임
        self.setup_header()
        
        # 스택 위젯 설정
        self.stack_widget = QtWidgets.QStackedWidget()
        
        # 페이지 생성 및 추가
        self.info_page = InfoPage(self.project_controller)
        self.gravity_load_page = GravityLoadPage(self.load_controller)
        self.wind_load_page = WindLoadPage(self.project_controller)
        
        self.stack_widget.addWidget(self.info_page)
        self.stack_widget.addWidget(self.gravity_load_page)
        self.stack_widget.addWidget(self.wind_load_page)
        
        content_layout.addWidget(self.stack_widget)
        self.main_layout.addWidget(self.main_content)
        
    def setup_header(self):
        """헤더 영역 설정"""
        self.header = QtWidgets.QFrame()
        self.header.setMinimumHeight(40)
        self.header.setMaximumHeight(40)
        self.header.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-bottom: 1px solid #cccccc;
            }
        """)
        
        # 헤더 레이아웃
        header_layout = QtWidgets.QHBoxLayout(self.header)
        header_layout.setContentsMargins(10, 0, 10, 0)
        
        # 파일 관리 버튼들
        self.btn_new = self.create_header_button("New")
        self.btn_open = self.create_header_button("Open")
        self.btn_save = self.create_header_button("Save")
        self.btn_save_as = self.create_header_button("Save As")
        
        header_layout.addWidget(self.btn_new)
        header_layout.addWidget(self.btn_open)
        header_layout.addWidget(self.btn_save)
        header_layout.addWidget(self.btn_save_as)
        header_layout.addStretch()
        
        self.main_content.layout().addWidget(self.header)
        
    def create_menu_button(self, text: str, icon_path: str = None) -> QtWidgets.QPushButton:
        """메뉴 버튼 생성"""
        btn = QtWidgets.QPushButton(text)
        btn.setMinimumHeight(40)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 5px 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        
        if icon_path:
            btn.setIcon(QtGui.QIcon(icon_path))
            
        return btn
        
    def create_header_button(self, text: str) -> QtWidgets.QPushButton:
        """헤더 버튼 생성"""
        btn = QtWidgets.QPushButton(text)
        btn.setFixedSize(80, 30)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #007e8e;
                color: white;
            }
        """)
        return btn
        
    def connect_signals(self):
        """시그널 연결"""
        # 메뉴 버튼 시그널
        self.btn_info.clicked.connect(lambda: self.stack_widget.setCurrentWidget(self.info_page))
        self.btn_gravity.clicked.connect(lambda: self.stack_widget.setCurrentWidget(self.gravity_load_page))
        self.btn_wind.clicked.connect(lambda: self.stack_widget.setCurrentWidget(self.wind_load_page))
        
        # 파일 관리 버튼 시그널
        self.btn_new.clicked.connect(self.on_new_project)
        self.btn_open.clicked.connect(self.on_open_project)
        self.btn_save.clicked.connect(self.on_save_project)
        self.btn_save_as.clicked.connect(self.on_save_as_project)
