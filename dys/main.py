"""DYS 애플리케이션 진입점"""

import sys
import warnings
import os

# 경고 필터 설정
warnings.simplefilter("ignore", UserWarning)

# Win32 모듈 import 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# PyQt6 애플리케이션
from PyQt6 import QtWidgets
from dys.ui.main_window import MainWindow


def main():
    """메인 함수"""
    # 애플리케이션 생성
    app = QtWidgets.QApplication(sys.argv)
    
    try:
        # 메인 윈도우 생성 및 표시
        window = MainWindow()
        window.show()
        
        # 애플리케이션 실행
        sys.exit(app.exec())
        
    except Exception as e:
        QtWidgets.QMessageBox.critical(
            None,
            "Error",
            f"애플리케이션 오류: {str(e)}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
