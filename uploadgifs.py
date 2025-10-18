import requests
from PIL import Image


def upload_gif_to_server(file_path, tags, width, height, length):
    url = 'http://192.168.1.171:8079/api/resource/gifs/upload'

    # 构建form-data数据
    files = {
        'file': ('image.gif', open(file_path, 'rb'), 'image/gif')
    }

    data = {
        'tags': tags,
        'width': str(width),
        'height': str(height),
        'length': str(length)
    }

    # 发送POST请求
    response = requests.post(url, files=files, data=data)
    return response


def getWH(path):
    with Image.open(path) as img:
        # 获取图片的宽度和高度
        width, height = img.size
        return width, height


if __name__ == '__main__':
    import os

    for file in os.listdir('files/gif'):
        if file.endswith('.gif'):
            # 获取文件的大小
            gif_file = 'files/gif/' + file
            file_size = os.path.getsize(gif_file)
            # 获取文件的宽度和高度
            # 获取图片文件的宽度和高度
            width, height = getWH(gif_file)
            # 上传文件
            # 获取文件名，不包含后缀
            file_name = os.path.splitext(file)[0]
            response = upload_gif_to_server(gif_file, file_name, width, height, file_size)
            print(response.status_code)
            print(response.text)
