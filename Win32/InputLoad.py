
from pywinauto import controls
from pywinauto import findwindows
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
#import pandas as pd
import time
import pyperclip




def ExportGen(file_name, df):

    try:
        handle = findwindows.find_windows(title_re=f"^Gen 2024.*{file_name}.*\[MIDAS\/Gen\]$")[0]
    
        app = Application().connect(handle=handle)


        midasgen_window = app.window(title_re=f"^Gen 2024.*{file_name}.*\[MIDAS\/Gen\]$")
        #midasgen_window.set_focus()
        midasgen_window.type_keys("^{F12}")


        time.sleep(1)
        handle = findwindows.find_window(title="MGT Command Shell")

        child_handle = findwindows.find_windows(top_level_only=False, class_name="RICHEDIT", parent=handle)[0]

        edit = controls.win32_controls.EditWrapper(child_handle)
    
        makeMGT(df)

        time.sleep(1)
        text = pyperclip.paste()
        edit.set_edit_text(text)
        time.sleep(1)
        send_keys('%r')  # Alt+R
        send_keys('%c')  # Alt+C
        return 0

    except IndexError:
        return 1
    
    except findwindows.WindowNotFoundError:
        return 2
   

def makeMGT(df):

    # Workbook 열기
    
    # 파일에 저장할 문자열 초기화
    result = '점유⋅사용하지 않는 지붕(지붕활하중)' in df['subcategory'].values

    text = "*UNIT    ; Unit System\n"
    text += "; FORCE, LENGTH, HEAT, TEMPER\n"
    text += "KN   , M, KCAL, C\n"

    if result: text += "*STLDCASE    ; Static Load Cases \n ; LCNAME, LCTYPE, DESC \n    DL   , D , \n    LL   , L ,\n   LR   , LR ,\n *FLOADTYPE    ; Define Floor Load Type\n ; NAME, DESC                                           ; 1st line\n ; LCNAME1, FLOAD1, bSBU1, ..., LCNAME8, FLOAD8, bSBU8  ; 2nd line\n"
    else: text += "*STLDCASE    ; Static Load Cases \n ; LCNAME, LCTYPE, DESC \n    DL   , D , \n    LL   , L ,\n *FLOADTYPE    ; Define Floor Load Type\n ; NAME, DESC                                           ; 1st line\n ; LCNAME1, FLOAD1, bSBU1, ..., LCNAME8, FLOAD8, bSBU8  ; 2nd line\n"

    for index, row in df.iterrows():
        room = row['name']
        floor = row['floor']
        DLoad = row['DL']
        LLoad = row['LL']
        if row['subcategory'] == '점유⋅사용하지 않는 지붕(지붕활하중)': 
            text += f'"({floor}){room}",\n DL, -{DLoad}, YES, LR, -{LLoad}, NO\n'
        else:
            text += f'"({floor}){room}",\n DL, -{DLoad}, YES, LL, -{LLoad}, NO\n'

    pyperclip.copy(text)


