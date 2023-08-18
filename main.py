from fastapi import FastAPI, WebSocket, Request, Depends, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from function import pdf_docx
from caj2pdf import caj2pdf
from typing import List
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 预定义变量
virtualNames = ["顶针","只因","启动","凡凡","沸羊羊","额额","龙卷风摧毁停车场"]
nameIndex = -1 # 用于顺序索引角色名字
messages = []
websocket_connections = []

# 用于自动更改昵称
def increaseNameIndex(request:Request):
    global nameIndex
    nameIndex = (nameIndex+1)%len(virtualNames)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, index: int = Depends(increaseNameIndex)):
    virtualpeople = virtualNames[nameIndex]
    print("临时昵称：",virtualNames[nameIndex])
    return templates.TemplateResponse("index.html", {"request": request, "messages": messages, "virtualpeople":virtualpeople})

# 接收一个socket连接，并保存
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # data = "["+ virtualNames[nameIndex] +"]: "+data
            messages.append(data)
            if len(messages) > 18:
                messages.pop(0)
            await broadcast_message(data)
    except Exception as e:
        print(e)
    finally:
        websocket_connections.remove(websocket)
        

# 把信息广播给每个客户端
async def broadcast_message(message: str):
    for connection in websocket_connections:
        await connection.send_text(message)

# 返回PDF转换的主界面
@app.get("/pdf2word")
def def_jump(request: Request):
    return templates.TemplateResponse("index_pdf2word.html", {"request": request})

# 返回caj转换的主界面
@app.get("/caj2pdf")
def def_jump(request: Request):
    return templates.TemplateResponse("index_caj2pdf.html", {"request": request})

# PDF转换的接口
@app.post('/file_pdf2word')
async def convert(file: UploadFile):
    # 
    if file.filename:
        # file.filename = "好"+file.filename # 这里加“好”是为了加入中文字符故意弄乱编码，从而在前端下载文件时的文件名是undefined.docx
        if file.filename.endswith(".pdf"):
            # 
            save_path = os.path.join("tempfiles",file.filename)
            # 
            with open(save_path, "wb") as f:
                contents = await file.read()
                f.write(contents)
            # 
            temp_filename = file.filename.split(".")[0]
            fullFileName = pdf_docx(temp_filename)
            # 
            file_path = fullFileName
            # file.docx
            endName = file.filename.split(".")[0] + ".docx"
            # 
            # print(file_path, '||||', endName)
            return FileResponse(file_path, filename=endName)
            
            # return {"message": ""}
            print("success!!!")
        else:
            print(file.filename, " with wrong file style...")
    else:
        # return {"message": ""}
        print("failure")

# caj转换接口
@app.post('/file_caj2pdf')
async def convert_1(file: UploadFile):
    if file.filename.endswith(".caj"):
        # file.filename = "好"+file.filename # 这里加“好”是为了加入中文字符故意弄乱编码，从而在前端下载文件时的文件名是undifined.pdf
        # 
        save_path = os.path.join("tempfiles",file.filename)
        # 保存文件到本地
        with open(save_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        # 
        # temp_filename = file.filename.split(".")[0]
        # print('lkz.......')
        fullFileName = caj2pdf(file.filename)
        # print(fullFileName, "12312312")
        # 此处file_path是包含相对路径和文件全名在内
        file_path = fullFileName
        # 
        endName = file.filename.split(".")[0] + ".pdf"
        print("end:", endName)
        # 
        return FileResponse(file_path, filename=endName)
        
        return {"message": ""}
        print("success!!!")
    else:
        print(file.filename, 'with wrong file type...')




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
