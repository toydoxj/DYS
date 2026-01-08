from pdf2image import convert_from_path

# Poppler 경로 지정
poppler_path = r"C:\poppler-xx\bin"

# PDF를 이미지로 변환
images = convert_from_path("1.pdf", dpi=300, poppler_path=poppler_path)

for i, image in enumerate(images):
    image.save(f"output_page_{i+1}.jpg", "JPEG")
