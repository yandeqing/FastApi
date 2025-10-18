import uvicorn
from fastapi import FastAPI, Request
from typing import Dict, Any
import socket  # 新增：导入网络模块用于获取IP

from FcmService import FcmService

app = FastAPI()


# 新增：获取本机IP的工具函数
def get_local_ip():
    """获取本机对外通信的IP地址（非127.0.0.1）"""
    try:
        # 通过临时Socket连接外部服务器确定出口IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # 连接DNS服务器（无需实际通信）
            return s.getsockname()[0]  # 获取本地绑定的IP地址
    except Exception:
        return "127.0.0.1"  # 异常时返回本地回环地址



# 合并：同时支持GET和POST请求的登录接口
@app.get("/api/login/v1/login")
@app.post("/api/login/v1/login")
async def login(request: Request):
    if request.method == "GET":
        # GET请求：获取查询参数
        params = dict(request.query_params)
    else:  # POST请求
        # POST请求：获取请求体参数
        params = await request.json()

    return {"request_type": request.method, "parameters": params}




# 合并：同时支持GET和POST请求的登录接口
@app.get("/api/login/v1/send-sms-code")
@app.post("/api/login/v1/send-sms-code")
async def sms_login(request: Request):
    if request.method == "GET":
        # GET请求：获取查询参数
        params = dict(request.query_params)
    else:  # POST请求
        # POST请求：获取请求体参数
        params = await request.json()

    return {"request_type": request.method, "parameters": params}

# 编写推送测试接口
@app.get("/api/send_notification")
async def send_test_notification(request: Request):
    if request.method == "GET":
        # GET请求：获取查询参数
        params = dict(request.query_params)
    else:  # POST请求
        # POST请求：获取请求体参数
        params = await request.json()

    # 调用FcmService发送测试通知
    fcm_service = FcmService('./uchat-9d016-firebase-adminsdk-fbsvc-7493c4b2eb.json')
    response = fcm_service.sendTest()
    return {"request_type": request.method, "parameters": params, "notification_response": response}

# 新增：启动事件处理器 - 应用启动时执行
local_ip = get_local_ip()
print(f"=== 应用启动成功 ===")
print(f"本机IP地址: {local_ip}")
# print(f"服务文档地址: http://{local_ip}:8079/api/login/v1/login")  # 附带文档地址方便访问 (端口已修改为8079)
print(f"服务文档地址: http://{local_ip}:8079/api/send_notification")  # 附带文档地址方便访问 (端口已修改为8079)

# 新增：程序入口，使用Uvicorn运行应用并指定端口
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8079, reload=True)
