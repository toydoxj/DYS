"""프로젝트 정보 페이지"""

from PyQt6 import QtWidgets, QtCore, QtGui
from typing import Optional

from dys.core.models.project import ProjectModel
from dys.core.services.file_service import FileService
from dys.config.constants import PROJECT_INFO_FIELDS


class InfoPage(QtWidgets.QWidget):
    """프로젝트 정보 페이지"""
    
    # 시그널 정의
    update_address = QtCore.pyqtSignal(str)  # 주소 업데이트 시그널
    
    def __init__(
        self,
        project_model: ProjectModel,
        file_service: Optional[FileService] = None,
        parent=None
    ):
        """
        프로젝트 정보 페이지 초기화
        
        Args:
            project_model: 프로젝트 모델
            file_service: 파일 서비스 (선택적)
            parent: 부모 위젯
        """
        super().__init__(parent)
        self.project_model = project_model
        self.file_service = file_service
        
        self.setup_ui()
        self.connect_signals()
        self.load_from_model()
    
    def setup_ui(self):
        """UI 설정"""
        # 메인 레이아웃
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Label Frame
        label_frame = QtWidgets.QFrame(self)
        label_frame.setMinimumSize(QtCore.QSize(120, 0))
        label_frame.setMaximumSize(QtCore.QSize(120, 16777215))
        label_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        label_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        
        label_layout = QtWidgets.QVBoxLayout(label_frame)
        
        # 레이블 생성
        self.labels = {}
        label_texts = {
            'code': 'Project Code',
            'project': '용역명',
            'address': '주소',
            'occupancy': '용도',
            'area': '연면적',
            'sfloor': '지상층수',
            'bfloor': '지하층수',
            'height': '높이',
            'importance': '중요도'
        }
        
        for field in PROJECT_INFO_FIELDS:
            label = self.create_label(label_texts.get(field, field))
            self.labels[field] = label
            label_layout.addWidget(label)
        
        label_layout.addSpacerItem(
            QtWidgets.QSpacerItem(
                20, 169,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Expanding
            )
        )
        
        # 입력 필드 Frame
        input_frame = QtWidgets.QFrame(self)
        input_frame.setMinimumSize(QtCore.QSize(450, 0))
        input_frame.setMaximumSize(QtCore.QSize(450, 16777215))
        input_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        input_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        
        input_layout = QtWidgets.QVBoxLayout(input_frame)
        
        # 입력 필드 생성
        self.line_edits = {}
        for field in PROJECT_INFO_FIELDS:
            line_edit = self.create_line_edit()
            self.line_edits[field] = line_edit
            input_layout.addWidget(line_edit)
        
        input_layout.addSpacerItem(
            QtWidgets.QSpacerItem(
                20, 169,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Expanding
            )
        )
        
        # 정보 표시 Frame
        info_frame = QtWidgets.QFrame(self)
        info_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        info_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        
        info_layout = QtWidgets.QVBoxLayout(info_frame)
        
        self.text_browser = QtWidgets.QTextBrowser(info_frame)
        self.setup_info_text()
        info_layout.addWidget(self.text_browser)
        
        # 레이아웃에 추가
        layout.addWidget(label_frame)
        layout.addWidget(input_frame)
        layout.addWidget(info_frame)
    
    def create_label(self, text: str) -> QtWidgets.QLabel:
        """
        레이블 생성
        
        Args:
            text: 레이블 텍스트
            
        Returns:
            QtWidgets.QLabel: 생성된 레이블
        """
        label = QtWidgets.QLabel(text)
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        label.setFont(font)
        label.setStyleSheet("QLineEdit {background-color: #cfcfcf; border: 1px solid #cccccc;}")
        label.setFixedSize(100, 25)
        return label
    
    def create_line_edit(self) -> QtWidgets.QLineEdit:
        """
        입력 필드 생성
        
        Returns:
            QtWidgets.QLineEdit: 생성된 입력 필드
        """
        line_edit = QtWidgets.QLineEdit()
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        line_edit.setFont(font)
        line_edit.setStyleSheet("QLineEdit { border: 1px solid #cccccc;}")
        line_edit.setFixedSize(300, 25)
        return line_edit
    
    def setup_info_text(self):
        """정보 텍스트 설정"""
        html_content = """
        <html><head><meta name="qrichtext" content="1" /><style type="text/css">
        p, li { white-space: pre-wrap; }
        </style></head><body style=" font-family:'Gulim'; font-size:9pt; font-weight:400; font-style:normal;">
        <p> <span style=" font-size:16pt; font-weight:600;"><br>DYL - 하중관리 프로그램</span></p>
        <p> <span style=" font-size:16px; font-weight:600; color:#a60000;"><br />현재 주요기능</span></p>
        <p>1. 하중 파일을 저장하고 읽습니다. (확장자는 dyl로 저장됨)</p>
        <p>2. 하중 DATA를 등록, 수정, 삭제, 화살표를 이용해서 정렬가능</p>
        <p>3. 자동으로 EXCEL하중표 작성</p>
        <p>4. 자동으로 MiDAS/Gen으로 하중입력</p>
        <hr />
        <p><span style=" font-size:16px; font-weight:600; color:#a60000;"><br />사용 시 주요 사항</span></p>
        <ul style="-qt-list-indent: 1;">
        <li style="-qt-block-indent:0;"><p>'중요' Gen Export를 위해서는 관리자 권한으로 실행할 것.\n</p></li>
        <li style="-qt-block-indent:0;"><p>Gen 파일은 가급적 입력하고자 하는 파일 1개만 열어 놓는 것이 좋음\n</p></li>
        <li style="-qt-block-indent:0;"><p>Gen 파일명 입력은 창 구분을 위한 것으로 다른 파일과 구분할 수 있도록 몇자만 적어두면 됨.\n</p></li>
        <li style="-qt-block-indent:0;"><p>매크로 돌아갈 때 안내창 뜰 때까지 가급적 다른 작업을 하지 말 것 (Excel, MiDAS Import)</p></li></ul>
        <hr />
        <p><span style=" font-size:16px; font-weight:600; color:#a60000;"><br />Release Note : ver0.2(beta)</span></p>
        <ul style="-qt-list-indent: 1;">
        <li style="-qt-block-indent:0;"><p>UI개선(추후 기능 추가를 위한 선작업)\n</p></li>
        <li style="-qt-block-indent:0;"><p>계단하중 입력 기능 추가\n</p></li>
        <li style="-qt-block-indent:0;"><p>지붕활하중을 구분하여 Gen으로 Export\n</p></li>
        <li style="-qt-block-indent:0;"><p>Gen Export 시 자동으로 저장하기 기능 추가함.(가끔 튕길 때가 있어 대비함)\n</p></li>
        </ul>
        <hr />
        """
        self.text_browser.setHtml(html_content)
    
    def connect_signals(self):
        """시그널 연결"""
        # 각 입력 필드의 변경 사항을 모델에 반영
        for i, field in enumerate(PROJECT_INFO_FIELDS):
            line_edit = self.line_edits[field]
            line_edit.textChanged.connect(
                lambda text, f=field: self.on_field_changed(f, text)
            )
    
    def on_field_changed(self, field: str, value: str):
        """
        필드 변경 핸들러
        
        Args:
            field: 필드 이름
            value: 새로운 값
        """
        self.project_model.set_info(field, value)
        
        # 주소 변경 시 시그널 발생
        if field == 'address':
            self.update_address.emit(value)
    
    def load_from_model(self):
        """모델에서 데이터 로드"""
        for field in PROJECT_INFO_FIELDS:
            value = self.project_model.get_info(field)
            self.line_edits[field].setText(value)
    
    def clear(self):
        """입력 필드 초기화"""
        for field in PROJECT_INFO_FIELDS:
            self.line_edits[field].clear()
    
    def refresh(self):
        """페이지 새로고침"""
        self.load_from_model()
