"""메인 윈도우"""

import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt

from dys.config.constants import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_PRIMARY, COLOR_BACKGROUND
from dys.config.settings import settings
from dys.core.models.project import ProjectModel
from dys.core.models.load import LoadModel
from dys.core.services.file_service import FileService
from dys.ui.widgets.left_menu import LeftMargin, LeftMenu
from dys.ui.widgets.header import Header
from dys.ui.pages.info_page import InfoPage
from dys.ui.pages.gravity_load_page import GravityLoadPage
from dys.ui.pages.wind_load_page import WindLoadPage
from dys.ui.pages.earthquake_load_page import EarthquakeLoadPage
from dys.ui.pages.load_combination_page import LoadCombinationPage


class MainWindow(QtWidgets.QMainWindow):
    """메인 윈도우 클래스"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 모델 초기화
        self.project_model = ProjectModel()
        self.load_model = LoadModel()
        
        # 서비스 초기화
        self.file_service = FileService(self.project_model, self.load_model)
        
        # UI 설정
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """UI 초기 설정"""
        # 기본 윈도우 설정
        self.setWindowTitle(APP_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # 아이콘 설정
        icon_path = settings.get_icon_path()
        if icon_path.exists():
            self.setWindowIcon(QtGui.QIcon(str(icon_path)))
        
        # 중앙 위젯
        central_widget = QtWidgets.QWidget()
        central_widget.setStyleSheet(f"background-color: {COLOR_PRIMARY};")
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QtWidgets.QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 좌측 여백
        left_margin = LeftMargin()
        main_layout.addWidget(left_margin)
        
        # 좌측 메뉴
        self.left_menu = LeftMenu()
        main_layout.addWidget(self.left_menu)
        
        # 메인 바디
        main_body = QtWidgets.QWidget()
        main_body.setStyleSheet(f"background-color: {COLOR_BACKGROUND};")
        
        body_layout = QtWidgets.QVBoxLayout(main_body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        
        # 헤더
        self.header = Header()
        body_layout.addWidget(self.header)
        
        # 메인 프레임 (페이지들이 들어갈 영역)
        self.main_frame = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout(self.main_frame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 스택 위젯 (페이지 전환용)
        self.stack_widget = QtWidgets.QStackedWidget()
        self.main_layout.addWidget(self.stack_widget)
        
        body_layout.addWidget(self.main_frame)
        main_layout.addWidget(main_body)
        
        # 페이지 설정
        self.setup_pages()
    
    def setup_pages(self):
        """페이지 설정"""
        # 프로젝트 정보 페이지
        self.info_page = InfoPage(self.project_model, self.file_service)
        self.stack_widget.addWidget(self.info_page)
        
        # 중력하중 페이지
        self.gravity_load_page = GravityLoadPage(self.load_model, self.project_model)
        self.stack_widget.addWidget(self.gravity_load_page)
        
        # 풍하중 페이지
        self.wind_load_page = WindLoadPage(self.project_model)
        self.stack_widget.addWidget(self.wind_load_page)
        
        # 지진하중 페이지
        self.earthquake_load_page = EarthquakeLoadPage(self.project_model)
        self.stack_widget.addWidget(self.earthquake_load_page)
        
        # 하중조합 페이지
        self.load_combination_page = LoadCombinationPage(self.project_model)
        self.stack_widget.addWidget(self.load_combination_page)
        
        # InfoPage의 주소 업데이트 시그널을 WindLoadPage에 연결
        self.info_page.update_address.connect(self.wind_load_page.set_address)
        
        # 기본 페이지 설정
        self.stack_widget.setCurrentWidget(self.info_page)
        self.left_menu.set_active_menu(0)
    
    def connect_signals(self):
        """시그널 연결"""
        # 메뉴 클릭 시그널
        self.left_menu.menu_clicked.connect(self.on_menu_clicked)
        
        # 헤더 버튼 시그널
        self.header.new_clicked.connect(self.on_new_project)
        self.header.open_clicked.connect(self.on_open_project)
        self.header.save_clicked.connect(self.on_save_project)
        self.header.save_as_clicked.connect(self.on_save_as_project)
    
    def on_menu_clicked(self, index: int):
        """
        메뉴 클릭 핸들러
        
        Args:
            index: 메뉴 인덱스
        """
        self.left_menu.set_active_menu(index)
        
        # 페이지 전환
        pages = [
            self.info_page,
            self.gravity_load_page,
            self.wind_load_page,
            self.earthquake_load_page,
            self.load_combination_page
        ]
        
        if 0 <= index < len(pages):
            self.stack_widget.setCurrentWidget(pages[index])
            
            # 헤더 제목 업데이트
            titles = [
                "Project Information",
                "Gravity Load",
                "Wind Load",
                "Seismic Load",
                "Load Combination"
            ]
            self.header.set_title(titles[index])
    
    def on_new_project(self):
        """새 프로젝트 버튼 클릭"""
        success, message = self.file_service.new_project(self)
        if success:
            QtWidgets.QMessageBox.information(self, "확인", message)
            # 모든 페이지 새로고침
            self.refresh_all_pages()
        else:
            if message != "취소되었습니다.":
                QtWidgets.QMessageBox.warning(self, "오류", message)
    
    def on_open_project(self):
        """프로젝트 열기 버튼 클릭"""
        success, message, file_path = self.file_service.open_project(self)
        if success:
            QtWidgets.QMessageBox.information(self, "확인", message)
            # 모든 페이지 새로고침
            self.refresh_all_pages()
        else:
            QtWidgets.QMessageBox.warning(self, "오류", message)
    
    def on_save_project(self):
        """프로젝트 저장 버튼 클릭"""
        file_path = self.project_model.current_file_path
        success, message, saved_path = self.file_service.save_project(file_path, self)
        if success:
            QtWidgets.QMessageBox.information(self, "확인", message)
        else:
            QtWidgets.QMessageBox.warning(self, "오류", message)
    
    def on_save_as_project(self):
        """다른 이름으로 저장 버튼 클릭"""
        success, message, saved_path = self.file_service.save_project_as(self)
        if success:
            QtWidgets.QMessageBox.information(self, "확인", message)
        else:
            if message != "파일이 선택되지 않았습니다.":
                QtWidgets.QMessageBox.warning(self, "오류", message)
    
    def refresh_all_pages(self):
        """모든 페이지 새로고침"""
        self.info_page.refresh()
        self.gravity_load_page.refresh()
        self.wind_load_page.refresh()
        # 다른 페이지들도 refresh 메서드가 있으면 호출
