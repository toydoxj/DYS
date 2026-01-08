


import os
from tkinter import Tk, filedialog, Button, Label, messagebox
from pdf2image import convert_from_path
from PIL import Image
import io
import win32clipboard  # Windows에서 클립보드 조작

pop_path = 'C:\\poppler-xx\\Library\\bin\\'

# 클립보드에 이미지를 복사하는 함수
def copy_image_to_clipboard(image):
    try:
        # 이미지를 BMP 형식으로 변환
        output = io.BytesIO()
        image.convert("RGB").save(output, format="BMP")
        data = output.getvalue()[14:]  # BMP 헤더 제거
        output.close()

        # 클립보드에 BMP 데이터를 설정
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

        messagebox.showinfo("Success", "Image copied to clipboard!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy image to clipboard: {str(e)}")

# PDF를 이미지로 변환하고 클립보드에 복사하는 함수
def convert_pdf_to_clipboard(pdf_files):
    for pdf_file in pdf_files:
        try:
            # PDF를 이미지로 변환
            images = convert_from_path(pdf_file, dpi=300, poppler_path=pop_path)
            for i, image in enumerate(images):
                copy_image_to_clipboard(image)
                status_label.config(text=f"Copied page {i + 1} of {pdf_file} to clipboard")
        except Exception as e:
            status_label.config(text=f"Error converting {pdf_file}: {str(e)}")

# 파일 선택 버튼 콜백 함수
def select_files():
    pdf_files = filedialog.askopenfilenames(
        title="Select PDF Files",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if pdf_files:
        convert_pdf_to_clipboard(pdf_files)

# GUI 설정
root = Tk()
root.title("PDF to JPG Clipboard Copier")
root.geometry("400x250")  # 창 크기 조정 (높이를 늘려 하단 공간 확보)

# 상단 레이블 및 버튼
Label(root, text="PDF to Clipboard Copier", font=("Arial", 16)).pack(pady=10)
Button(root, text="Select PDF Files", command=select_files, width=20).pack(pady=10)
status_label = Label(root, text="", fg="green")
status_label.pack(pady=10)

# 하단 저작권 표시
copyright_label = Label(root, text="Copyright : (주)동양구조", font=("Arial", 10), fg="gray")
copyright_label.pack(side="bottom", pady=10)  # 하단에 배치

# 프로그램 실행
root.mainloop()

