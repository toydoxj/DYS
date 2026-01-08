import pandas as pd
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLabel, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import rc_resource

def convert(file_path):

    # # 텍스트 파일 경로 설정
    # file_path = "./UI/1.BWP"

    # 데이터 가져오기
    data = []
    columns = ["ID", "WallMark"]
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("TOTALSTORY"):
                total_story = int(line.split(",")[1])
            if line.startswith("S_"):
                story = str(line.split(",")[1]).strip()
                columns = columns+[story]
            if line.startswith("CURNT_SET"):
                break
        

    # 데이터프레임 생성
    df = pd.DataFrame(columns=columns)

    start_line = "WMARK-DATA"
    end_line = "ID_MEMB_INDEX"
    start_reading = False
    Exist_wallmark = False
 
    wall_id=[]
    temp_rebar=[]
    rebar = []
    j = 0


    rebar_pass = False


    with open(file_path, "r") as file:
        for line in file:
            if start_reading and line.strip() == end_line:
                break
            elif line.strip() == start_line:
                start_reading = True

            # 벽체 Mark 시작점 확인    
            elif start_reading and (line.startswith("W") or line.startswith("EW") or line.startswith("SW") or line.startswith("HW") or line.startswith("BW") or line.startswith("THW") or line.startswith("TW") or line.startswith("기초")):
                Exist_wallmark = True
                wall_id_count = 0
                i = 0
                j = 0
                wallmark = str(line.split(",")[0]).strip()


    
            #Wall ID 갯수 확인
            elif start_reading and Exist_wallmark and wall_id_count == 0 and i == 0 and j ==0:  
                wall_id_count = int(line.strip())
            
            #Wall ID DATA 수집
            elif start_reading and Exist_wallmark and wall_id_count !=0 and j == 0 and not rebar_pass:
                
                if wall_id_count == i :
                    j = 0
                    i = 0
                    rebar_pass = True
                else : 
                    wall_id.append(int(line.strip()))
                    i +=1 #wall id 수집되면 1씩 증가

            elif start_reading and j == 0:
                j +=1

            elif start_reading and j !=0 :
                if j == total_story * 4:
                    j = 0

                    for idx, id_value in enumerate(wall_id):
                        data_row = [id_value, wallmark] + rebar
                        df.loc[len(df)] = data_row
                        print(wallmark)

                    rebar = []
                    Exist_wallmark= False
                    rebar_pass = False
                    wall_id =[]

                if j % 4 == 1:
                    
                    if int(line.split(",")[5].strip()) == 0: temp_rebar.append(int(line.split(",")[0].strip()))
                    else : temp_rebar.append(int(line.split(",")[4].strip()))
                    temp_rebar.append(int(line.split(",")[1].strip()))
                    temp_rebar.append(int(line.split(",")[2].strip()))
                    temp_rebar.append(int(line.split(",")[3].strip()))
                    rebar.append(temp_rebar)
                    temp_rebar=[]
                
                    j += 1
                    
                else: j += 1

                
    # 결과 출력

    text = f"*REBAR-WALL    ; Modify Wall Rebar Data\n"
    for _, row in df.iterrows():
        wall_id = row['ID']
        wall_mark = row['WallMark']
        for column in df.columns[2:]:
            rebar_value = row[column]
            vbar, hbar, vspace, hspace = rebar_value
            text +=(f"{wall_id}, {column}, YES, 0, D{vbar}, {vspace}, ,0,0, D{hbar}, {hspace}, 20, 20, D10, 200, 0, 1, {column}\n")

    
            

    with open('output.txt', 'w') as f:
        f.write(text)

    
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BWP->MGT변환프로그램")
        self.setFixedSize(400, 200)  # 창 크기를 400x300으로 고정

        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)

        self.label = QLabel("\n BWP 파일을 선택하면, output.txt에 배근정보가 기입됩니다.\n 마이다스의 Mgt Command Shell을 열어 붙여 넣으세요.\n 에러 발생 시 다운 될 수 있으니 주의하기 바랍니다.\n output.txt는 실행파일과 동일 폴더에 저장됩니다.\n\n")
        layout.addWidget(self.label)

        self.button = QPushButton("파일 선택")
        layout.addWidget(self.button)
        self.button.clicked.connect(self.select_file)

        self.label_Dylogo = QLabel()
        layout.addWidget(self.label_Dylogo)
        self.label_Dylogo.setText("")
        self.label_Dylogo.setPixmap(QPixmap(":/logo/Icons/logo/DY-S.png"))
        self.label_Dylogo.setObjectName("label_Dylogo")
        self.label_Dylogo.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignRight)

        self.setCentralWidget(widget)
        self.setStyleSheet("background-color: white;")



    def select_file(self):
        file_dialog = QFileDialog()
        file_dialog.exec()

        selected_files = file_dialog.selectedFiles()
        if selected_files:
            file_path = selected_files[0]
            self.label.setText(f"선택한 파일 경로: {file_path}")
            convert(file_path)
            QMessageBox.information(None, '확인', 'output.txt 파일을 확인하세요.')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

            
    

