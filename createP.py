import requests
import json
from login import get_token

"""造产品线数据"""
token = get_token()


def createProduct():

    productgroupidList = []  # 放产品线id
    for i in range(20):
        url = 'https://dev.recloud.com.cn:7181/api/dynamic/new_productgroup/SaveAndFetch'
        headers = {'Authorization': 'Bearer ' + token,
                   'Accept-Language': 'zh-CN'}
        body = {
            "ownerid": {
                "id": "67781f72-450c-e611-80bc-000c292d3ec1",
                "logicalname": "systemuser",
                "name": "Administrator"
            },
            "new_name": "PG" + str(i + 1),
            "new_code": "PG" + str(i + 1)
        }
        res1 = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
        print(res1.text)
        productgroupid = res1.json()['Data']['new_productgroupid']
        productgroupidList.append(productgroupid)

    """造产品型号数据"""
    modelidlist = []  # 放产品型号id
    count1 = 0
    for j in range(20):  # 产品线数量
        for k in range(20): # 产品型号数量
            count1 += 1
            url = 'https://dev.recloud.com.cn:7181/api/dynamic/new_productmodel/SaveAndFetch'
            headers = {'Authorization': 'Bearer ' + token,
                       'Accept-Language': 'zh-CN'}
            body = {
                "ownerid": {
                    "name": "Administrator",
                    "id": "67781f72-450c-e611-80bc-000c292d3ec1",
                    "logicalname": "systemuser"
                },
                "new_name": "PM" + str(count1),
                "new_code": "PM" + str(count1),
                "new_productgroup_id": {
                    "id": productgroupidList[j],
                    # "name": " ",
                    "logicalname": "new_productgroup"
                }
            }
            res2 = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
            print(res2.text)
            modelid = res2.json()['Data']['new_productmodelid']
            modelidlist.append(modelid)
    """造产品物料(成品)数据 8000条40分钟"""
    count2 = 0
    for j in range(20):  # 线
        for k in range(20):  # 型号
            for l in range(20):  # 成品
                count2 += 1
                url = 'https://dev.recloud.com.cn:7181/api/dynamic/product/SaveAndFetch'
                headers = {'Authorization': 'Bearer ' + token,
                           'Accept-Language': 'zh-CN'}
                body = {
                    "new_ifapplied": 1,
                    "new_isreturn": True,
                    "name": "Product" + str(count2),
                    "productnumber": "Product" + str(count2),
                    "new_itemtype": 1,
                    "defaultuomid": {
                        "id": "e7880001-0000-7f21-0000-05d35461595d",
                        "name": "个",
                        "logicalName": "uom"
                    },
                    "new_productgroupid": {
                        "id": productgroupidList[j],
                        # "name": " ",
                        "logicalName": "new_productgroup"
                    },
                    "new_productmodule_id": {
                        "id": modelidlist[20 * j + k],  # 这个20取决于一条线下面有多少个型号
                        # "name": " ",
                        "logicalName": "new_productmodel"
                    }
                }
                res3 = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
                productid = res3.json()['Data']['productid']
                # print(productid)
                '''发布成品'''
                urlRelease = 'https://dev.recloud.com.cn:7181/api/dynamic/product/SaveAndFetch'
                headerRelease = {'Authorization': 'Bearer ' + token,
                                 'Accept-Language': 'zh-CN'}
                bodyRelease = {"statuscode": 1, "$id": productid}
                resRelease = requests.post(urlRelease, data=json.dumps(bodyRelease), headers=headerRelease)
                print(resRelease.text)


if __name__ == '__main__':
    createProduct()
