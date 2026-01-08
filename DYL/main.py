import sys
from PyQt6 import QtWidgets
from models import ProjectModel, LoadModel
from controllers import ProjectController, LoadController
from views import MainWindow

def main():
    # PyQt 애플리케이션 생성
    app = QtWidgets.QApplication(sys.argv)
    
    try:
        # 모델 인스턴스 생성
        project_model = ProjectModel()
        load_model = LoadModel()
        
        # 컨트롤러 인스턴스 생성
        project_controller = ProjectController(project_model, load_model)
        load_controller = LoadController(load_model)
        
        # 메인 윈도우 생성
        main_window = MainWindow(project_controller, load_controller)
        main_window.show()
        
        # 애플리케이션 실행
        sys.exit(app.exec())
        
    except Exception as e:
        QtWidgets.QMessageBox.critical(None, "Error", f"Application Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
