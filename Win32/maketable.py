import xlwings as xw
from xlwings.constants import Pattern, ThemeColor, LineStyle, HAlign, VAlign
import pandas as pd
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QApplication
import pywintypes


def make_loadtable(df_load, project):
    
    wb = xw.Book('form\Table_form.xlsx')
    ws = wb.sheets['고정적재하중']

    SDL_Row = 0
    Input_Rows = 0
    Row_Count = -1

    # 기존 시트 내용 지우기
    last_row = ws.range("D"+str(ws.cells.rows.count)).end('up').row

    ws.cells(4,2).value = "Proejct : " + project
    if last_row > 7 :
        ws.range(f"A8:A{last_row}").api.EntireRow.Delete()

    #df_load.reset_index(inplace=True)
    df_load = df_load.fillna("")

    i = 2

    number_load = df_load['ID'].max()

    for index, row in df_load.iterrows():
        Input_Rows = Input_Rows + Row_Count + 1
        Target = ws.cells(8+Input_Rows, 2)

        i = i + 1

        
        list_finish=['f1','f2','f3','f4','f5','f6']
        list_density=['d1','d2','d3','d4','d5','d6']
        list_thk = ['t1','t2','t3','t4','t5','t6']
        list_load = ['l1','l2','l3','l4','l5','l6']
        for j in range(5,-1,-1):
            if df_load.loc[index, list_finish[j]] == "" : SDL_Row = j 
            
    # 층수와 실명 가져오기.

        Target.value = df_load.loc[index,'floor']               #층수
        Target.offset(0,1).value =  df_load.loc[index,'name']   #실명

        for j in range(0,SDL_Row):
            Target.offset(j, 2).value = df_load.loc[index,list_finish[j]]    #재료마감
            Target.offset(j, 3).value = df_load.loc[index,list_thk[j]]      #두께
            Target.offset(j, 4).value = df_load.loc[index,list_density[j]]      #밀도
            Target.offset(j, 5).value = df_load.loc[index,list_load[j]]      #하중
            Target.offset(j, 5).number_format = "0.00"

            #  콘크리트 슬래브 유무 확인

        if not df_load.loc[index,"Type"] == '없음' :
                    
            Target.offset(SDL_Row , 2).resize(1, 4).color = '#dddddd'
            Target.offset(SDL_Row , 2).value = "마감하중 소계"
            Target.offset(SDL_Row , 5).value = df_load.loc[index,"SDL"]
            Target.offset(SDL_Row , 5).number_format = "0.00"
            Target.offset(SDL_Row , 5).font.bold = True

            Target.offset(SDL_Row + 1, 2).value = df_load.loc[index,"Type"]

            if Target.offset(SDL_Row + 1, 2).value == "데크 슬래브" :
                Target.offset(SDL_Row + 2, 2).Value = "데크철판"
                Target.offset(SDL_Row + 2, 5).Value = 0.2
                Row_Count = SDL_Row + 3

                Target.offset(SDL_Row + 1, 4).value = 24
                Target.offset(SDL_Row + 1, 5).value = df_load.loc[index,"conLoad"]
                Target.offset(SDL_Row + 1, 5).number_format = "0.00"

            elif Target.offset(SDL_Row + 1, 2).value == "콘크리트 슬래브":
                Row_Count = SDL_Row + 2
                Target.offset(SDL_Row + 1, 3).value = df_load.loc[index,"conthk"]

                Target.offset(SDL_Row + 1, 4).value = 24
                Target.offset(SDL_Row + 1, 5).value = df_load.loc[index,"conLoad"]
                Target.offset(SDL_Row + 1, 5).number_format = "0.00"

            elif Target.offset(SDL_Row + 1, 2).value == "계단 슬래브":
                Row_Count = SDL_Row + 2
                Target.offset(SDL_Row + 1, 3).value = df_load.loc[index,"conthk"]

                Target.offset(SDL_Row + 1, 4).value = 24
                Target.offset(SDL_Row + 1, 5).value = df_load.loc[index,"conLoad"]
                Target.offset(SDL_Row + 1, 5).number_format = "0.00"

            
            else:
                Target.offset(SDL_Row + 1, 2).value = "( 자중은 프로그램에서 자동 계산 )"
                Target.offset(SDL_Row + 1, 2).resize(1, 2).merge()
                Row_Count = SDL_Row + 2
            
        else:
            Row_Count = SDL_Row 


        # 고정하중 계 입력 부분
        
        Target.offset(Row_Count, 2).resize(1, 4).color = '#dddddd'
        Target.offset(Row_Count, 2).value = "고정하중 계"
        Target.offset(Row_Count, 5).value = df_load.loc[index,"DL"]
        Target.offset(Row_Count, 5).number_format = "0.00"
        Target.offset(Row_Count, 5).font.bold = True
        
            
            
        # 활하중 값 입력
        
        Target.offset(Row_Count, 6).value = df_load.loc[index,"LL"]
        Target.offset(Row_Count, 6).number_format = "0.00"
        Target.offset(Row_Count, 6).font.bold = True
        
        liveloadText = "[" + df_load.loc[index,"subcategory"] + "]"
        Target.offset(0, 6).value = liveloadText
        Target.offset(0, 6).wrap_text = True
        Target.offset(0, 6).resize(Row_Count, 1).merge()
        Target.offset(0, 6).api.HorizontalAlignment = xw.constants.HAlign.xlHAlignCenter
            
        # 사용하중 값 입력
        
        Target.offset(Row_Count, 7).value = df_load.loc[index,"Service"]
        Target.offset(Row_Count, 7).number_format = "0.00"
        Target.offset(Row_Count, 7).font.bold = True

        Target.offset(0, 7).resize(Row_Count, 1).merge()
        Target.offset(0, 7).wrap_text = True
        # Target.offset(0, 7).api.HorizontalAlignment = xw.constants.HAlign.xlHAlignCenter
        # Target.offset(0, 7).api.VerticalAlignment = xw.constants.VAlign.xlVAlignBottom
        
        # 계수하중 값 입력
        
        Target.offset(Row_Count, 8).value = df_load.loc[index,"Strength"]
        Target.offset(Row_Count, 8).number_format = "0.00"
        Target.offset(Row_Count, 8).font.bold = True
        Target.offset(0, 8).resize(Row_Count, 1).merge()
        
        Target.offset(0, 8).wrap_text = True

        
        # 층수 합치기
        Target.resize(Row_Count+1, 1).merge()

        Target.wrap_text = True
        # Target.VerticalAlignment = xlCenter
        
        # 실명 합치기
        Target.offset(0, 1).resize(Row_Count+1, 1).merge()
        
        Target.offset(0, 1).wrap_text = True
        # Target.Offset(0, 1).VerticalAlignment = xlCenter
        
        # Class 참조 https://github.com/xlwings/xlwings/blob/main/xlwings/constants.py

        # '' 선정리
        Target.resize(Row_Count + 1, 1).api.Borders(7).LineStyle = 1
        Target.resize(Row_Count + 1, 1).api.Borders(10).LineStyle = -4118
        Target.offset(0, 1).resize(Row_Count + 1, 1).api.Borders(10).LineStyle = 1
        Target.offset(0, 2).resize(Row_Count + 1, 1).api.Borders(10).LineStyle = -4118
        Target.offset(0, 3).resize(Row_Count + 1, 1).api.Borders(10).LineStyle = -4118
        Target.offset(0, 4).resize(Row_Count + 1, 1).api.Borders(10).LineStyle = -4118
        Target.offset(0, 5).resize(Row_Count + 1, 1).api.Borders(10).LineStyle = 1
        Target.offset(0, 6).resize(Row_Count + 1, 1).api.Borders(10).LineStyle = 1
        Target.offset(0, 7).resize(Row_Count + 1, 1).api.Borders(10).LineStyle = 1
        Target.offset(0, 8).resize(Row_Count + 1, 1).api.Borders(10).LineStyle = 1
        Target.resize(Row_Count + 1, 9).api.Borders(9).LineStyle = 1
        
        # '' 폰트정리
        Target.resize(Row_Count + 1, 9).font.size = 9
        Target.resize(Row_Count + 1, 9).api.HorizontalAlignment = xw.constants.HAlign.xlHAlignCenter

    last_row = ws.range("D"+str(ws.cells.rows.count)).end('up').row

    ws.range("A8:A"+str(last_row)).api.RowHeight = 18
    ws.api.PageSetup.PrintArea = "A1:K"+str(last_row+1)

    app = QApplication.instance()
    reply = QMessageBox.question(None, '확인', '하중표 작성이 완료되었습니다\n 저장하시겠습니까?', QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard)
    
    if reply == QMessageBox.StandardButton.Save:
        click_FileSave(wb)

def click_FileSave(wb):
    file_name, _ = QFileDialog.getSaveFileName(None, "파일 선택", "", "Excel Files (*.xlsx);;All Files (*)")
    if file_name:
        try : 
            wb.save(file_name)
            QMessageBox.information(None, '확인', '저장하였습니다.')
        except pywintypes.com_error as e:
            msg = QMessageBox()
            msg.setText("저장오류")
            msg.setInformativeText(f"Failed to save file {file_name}.\n열려있는 파일을 닫아주세요.")
            msg.setFixedSize(800,100)
            msg.setWindowTitle("Error")
            msg.exec() 
            click_FileSave(wb)             
        except Exception as e:
            msg = QMessageBox()
            msg.setText("저장오류")
            msg.setInformativeText(f"Failed to save file {file_name}.\n열려있는 파일을 닫아주세요.")
            msg.setFixedSize(800,100)
            msg.setWindowTitle("Error")
            msg.exec()  
            click_FileSave(wb)



