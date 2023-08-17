import fitz
# 需要安装依赖包：PyMuPDF
# pip install PyMuPDF
def caj2pdf(caj_file):
    # 找到工作路径
    caj_file = 'tempfiles\\'+caj_file
    # 打开 caj 文件
    doc = fitz.open(caj_file)
    # 保存为 pdf 文件
    firstName = caj_file.split('.')[0]
    pdf_file = firstName + '.pdf'
    doc.save(pdf_file)
    # 关闭文件
    doc.close()

    return(pdf_file)

 
# if __name__ == '__main__':
#     file_name = "awd"
#     file_name += '.caj'
#     caj_to_pdf(file_name)