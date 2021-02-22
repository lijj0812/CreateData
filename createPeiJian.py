import requests
import json
import random
from login import get_token
'''新增配件  1w/h左右'''
token = get_token()

def createPJ():
    for i in range(10000):

        url = 'https://dev.recloud.com.cn:7181/api/dynamic/product/SaveAndFetch'
        headers = {'Authorization': 'Bearer ' + token,
                   'Accept-Language': 'zh-CN'}
        body = {
            "new_isreturn": random.choice([True, False]),  # 是否返厂
            "name": "配件" + str(i + 1 + 70439),
            "productnumber": "PeiJian" + str(i + 1 + 70439),  # 配件编码
            "new_itemtype": 2,  # 配件类型的物料类别
            "defaultuomid": {
                "id": "e7880001-0000-7f21-0000-05d35461595d",
                "name": "个",
                "logicalName": "uom"
            },
            "description": "配件" + str(i + 1 + 70439) + "的说明",
            "new_ifapplied": random.randint(1, 2)  # 是否可申请 1是  2否
        }
        res = requests.post(url=url, data=json.dumps(body), headers=headers)
        productid = res.json()['Data']['productid']
        '''发布配件'''
        urlFa = 'https://dev.recloud.com.cn:7181/api/dynamic/product/SaveAndFetch'
        headersFa = headers = {'Authorization': 'Bearer ' + token,
                               'Accept-Language': 'zh-CN'}
        bodyFa = {"statuscode": 1, "$id": productid}
        res = requests.post(urlFa, data=json.dumps(bodyFa), headers=headersFa)
        print(res.text)
        print(i + 1 + 70439)


if __name__ == '__main__':
    createPJ()
