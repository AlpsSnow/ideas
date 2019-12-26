import requests
import json
import base64
from urllib.parse import quote
import os

# 百度AI平台 文字识别API
API_Key = '7ozPdYCKWpXQhGLZingB9Cm8'
Secret_Key = '53GBqlVoF3PNdCNKT4h3G4YTnoAa0uhI'


# 获取文字识别的access_token
def getAipAccessToken():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token'    
    payload = {
        'grant_type': 'client_credentials',
        'client_id': API_Key,
        'client_secret': Secret_Key}
    response = requests.post(url=host,data=payload,verify=False)
    if response.status_code == 200 :
        response_dict = json.loads(response.text)
        print(response_dict)
        AccessToken =  response_dict['access_token']
        return AccessToken
    return None

# 读取银行回执单
def readReceipt(access_token,image_path):
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'charset': "utf-8"
    }

    # iocr识别api_url
    recognise_api_url = "https://aip.baidubce.com/rest/2.0/solution/v1/iocr/recognise/finance"

    access_token = access_token
    templateSign = 'bank_receipt'   # 银行回执单标准模板
    detectorId = 0
    #classifierId = "your_classifier_id"
    # 测试数据路径
    #image_path = './receipt/chinabank1.png'
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        image_b64 = base64.b64encode(image_data)
        # 请求模板的bodys
        recognise_bodys = 'access_token=' + access_token + '&templateSign=' + templateSign + \
                '&image=' + quote(image_b64)
        # 请求分类器的bodys
        # classifier_bodys = "access_token=" + access_token + "&classifierId=" + classifierId + "&image=" + quote(image_b64.encode("utf8"))
        
        # 混贴票据识别的bodys
        # detector_bodys = "access_token=" + access_token + "&detectorId=" + str(detectorId) + "&image=" + quote(image_b64.encode("utf8"))
        
        # 请求模板识别
        response = requests.post(recognise_api_url, data=recognise_bodys, headers=headers, verify=False)

        # 请求分类器识别
        # response = requests.post(recognise_api_url, data=classifier_bodys, headers=headers)
        # 请求混贴票据识别
        # response = requests.post(recognise_api_url, data=detector_bodys, headers=headers)

        if response.status_code == 200 :
            response_dict = json.loads(response.text)
            print(response_dict)
            return response_dict
        return None
    except Exception as e:
        print(e)
        return None

# 遍历银行回执单图片文件夹
def getReceiptList(dirpath):
    receiptList = []
    for root, dirs, files in os.walk(dirpath):
        print('根目录:{0},文件夹:{1},文件数:{2}'.format(root,dirs,len(files)))
        files.sort()
        for f in files:                          
            receiptList.append(f)
    return receiptList

if __name__ == "__main__":
    dirpath = './receipt'
    receiptList = getReceiptList(dirpath)
    if len(receiptList) == 0:
        print('银行回执单图片列表为空！')
        exit()
    access_token = None
    access_token = getAipAccessToken()
    if access_token == None:
        print('access_token取得失败！')
        exit()
    print('access_token: %s' % (access_token))

    for receipt in receiptList:
        image_path = dirpath + '/' + receiptList[0]
        receipt_date = readReceipt(access_token,image_path)
        if receipt_date == None:
            print('银行回执单数据读取失败！')
            exit()
        
    



        
    



