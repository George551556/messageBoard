import os
from pdf2docx import Converter
# 被调用的工具脚本
# 将pdf转换为word。使用虚拟环境base

def pdf_docx(file_name):
    # 获取当前工作目录
    file_path = os.getcwd() + r"\tempfiles"
    print("当前工作目录："+file_path)
    # pdf文件名称
    pdf_name = file_path + '\\' + file_name + '.pdf'
    # docx文件名称
    docx_name = file_path + '\\' + file_name + '.docx'

    # 加载pdf文档
    cv = Converter(pdf_name)
    cv.convert(docx_name, start=0, end=50)
    cv.close()

    return docx_name


# if __name__ == '__main__':
#     name = "teset"
#     print(pdf_docx(name))