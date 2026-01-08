from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt
from controllers.project_controller import ProjectController

class InfoPage(QtWidgets.QWidget):
    """프로젝트 정보 페이지"""
    
    def __init__(self, project_controller: ProjectController, parent=None):
        super().__init__(parent)
        self.project_controller = project_controller
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """UI 초기 설정"""
        # 메인 레이아웃
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 프로젝트 정보 그룹
        self.setup_project_info_group()
        
        # 건물 정보 그룹
        self.setup_building_info_group()
        
        # 여백 추가
        main_layout.addStretch()
        
    def setup_project_info_group(self):
        """프로젝트 정보 그룹 설정"""
        group = QtWidgets.QGroupBox("Project Information")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        
        layout = QtWidgets.QFormLayout(group)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 프로젝트 코드
        self.txt_code = self.create_line_edit("프로젝트 코드를 입력하세요")
        layout.addRow("Project Code:", self.txt_code)
        
        # 프로젝트명
        self.txt_project = self.create_line_edit("프로젝트명을 입력하세요")
        layout.addRow("Project Name:", self.txt_project)
        
        # 주소
        self.txt_address = self.create_line_edit("주소를 입력하세요")
        layout.addRow("Address:", self.txt_address)
        
        # 용도
        self.txt_occupancy = self.create_line_edit("건물 용도를 입력하세요")
        layout.addRow("Occupancy:", self.txt_occupancy)
        
        self.layout().addWidget(group)
        
    def setup_building_info_group(self):
        """건물 정보 그룹 설정"""
        group = QtWidgets.QGroupBox("Building Information")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        
        layout = QtWidgets.QFormLayout(group)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 면적
        self.txt_area = self.create_line_edit("면적을 입력하세요")
        layout.addRow("Area (m²):", self.txt_area)
        
        # 지상층수
        self.txt_sfloor = self.create_line_edit("지상층수를 입력하세요")
        layout.addRow("Stories (Above):", self.txt_sfloor)
        
        # 지하층수
        self.txt_bfloor = self.create_line_edit("지하층수를 입력하세요")
        layout.addRow("Stories (Below):", self.txt_bfloor)
        
        # 건물높이
        self.txt_height = self.create_line_edit("건물높이를 입력하세요")
        layout.addRow("Height (m):", self.txt_height)
        
        # 중요도
        self.cmb_importance = QtWidgets.QComboBox()
        self.cmb_importance.addItems(["특", "1", "2", "3"])
        layout.addRow("Importance:", self.cmb_importance)
        
        self.layout().addWidget(group)
        
    def create_line_edit(self, placeholder: str) -> QtWidgets.QLineEdit:
        """라인 에디트 위젯 생성"""
        line_edit = QtWidgets.QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 1px solid #007e8e;
            }
        """)
        return line_edit
        
    def connect_signals(self):
        """시그널 연결"""
        # 텍스트 변경 시그널
        self.txt_code.textChanged.connect(lambda text: self.update_project_info('code', text))
        self.txt_project.textChanged.connect(lambda text: self.update_project_info('project', text))
        self.txt_address.textChanged.connect(lambda text: self.update_project_info('address', text))
        self.txt_occupancy.textChanged.connect(lambda text: self.update_project_info('occupancy', text))
        self.txt_area.textChanged.connect(lambda text: self.update_project_info('area', text))
        self.txt_sfloor.textChanged.connect(lambda text: self.update_project_info('sfloor', text))
        self.txt_bfloor.textChanged.connect(lambda text: self.update_project_info('bfloor', text))
        self.txt_height.textChanged.connect(lambda text: self.update_project_info('height', text))
        self.cmb_importance.currentTextChanged.connect(lambda text: self.update_project_info('importance', text))
        
    def update_project_info(self, key: str, value: str):
        """프로젝트 정보 업데이트"""
        success, message = self.project_controller.update_project_info(key, value)
        if not success:
            QtWidgets.QMessageBox.warning(self, "경고", message)
            
    def load_project_info(self):
        """프로젝트 정보 로드"""
        self.txt_code.setText(self.project_controller.get_project_info('code'))
        self.txt_project.setText(self.project_controller.get_project_info('project'))
        self.txt_address.setText(self.project_controller.get_project_info('address'))
        self.txt_occupancy.setText(self.project_controller.get_project_info('occupancy'))
        self.txt_area.setText(self.project_controller.get_project_info('area'))
        self.txt_sfloor.setText(self.project_controller.get_project_info('sfloor'))
        self.txt_bfloor.setText(self.project_controller.get_project_info('bfloor'))
        self.txt_height.setText(self.project_controller.get_project_info('height'))
        
        importance = self.project_controller.get_project_info('importance')
        index = self.cmb_importance.findText(importance)
        if index >= 0:
            self.cmb_importance.setCurrentIndex(index)
