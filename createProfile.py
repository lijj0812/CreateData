import requests
import json
import random
from login import get_token
from getRandomData import getRandomProvinceCityCounty, getRandomGroupModelProduct, getRandomAccCon
"""造设备档案"""


def createPro():
    """造设备档案"""

    begindate = ["2020-10-12T00:00:00.000Z", "2020-10-13T00:00:00.000Z", "2020-10-14T00:00:00.000Z"]
    enddate = ["2077-10-12T00:00:00.000Z", "2077-10-13T00:00:00.000Z", "2077-10-14T00:00:00.000Z"]
    buydate = ["2020-10-10T20:00:00.000Z", "2020-10-11T20:00:00.000Z", "2020-10-12T20:00:00.000Z"]\
  #  for i in range(1000000):
    while True:
        randomIndex = random.randint(0, 2)
        randomGroupModelProduct = getRandomGroupModelProduct(u'成品.xlsx', 0)
        randomProvinceCityCounty = getRandomProvinceCityCounty(u'1.xls', 0)
        randomAccCon = getRandomAccCon(u'客户联系人.xlsx', 0)
        url = 'https://dev.recloud.com.cn:5202/api/custom/new_xrmcommon/UserProfile/CreateUserProfile'
        headers = {'Authorization': 'Bearer ' + get_token(),
                   "Content-Type":"application/json"}
        body = {
            "model": {
                "new_customerid": {
                    "id": randomAccCon[0],
                    # "name": "",
                    "logicalName": "account"
                },
                "new_product_id": {
                    "id": randomGroupModelProduct[4],
                    # "name": " ",
                    "logicalName": "product"
                },  # 产品物料
                "new_productmodel": {
                    "id": randomGroupModelProduct[2],
                    # "name": " ",
                    "logicalName": "new_productmodel"
                },  # 产品型号
                "new_productgroup": {
                    "id": randomGroupModelProduct[0],
                    # "name": " ",
                    "logicalName": "new_productgroup"
                },  # 产品线
                "new_datasource": 1,
                "new_begindate": begindate[randomIndex],
                "new_enddate": enddate[randomIndex],
                "new_buydate": buydate[randomIndex],
                "ownerid": {
                    "id": "67781f72-450c-e611-80bc-000c292d3ec1",
                    "logicalname": "systemuser",
                    "name": "Administrator"
                },
                "new_lastcontactaddress": randomProvinceCityCounty[5] + "街道",
                "new_province_id": {
                    # "name": " ",
                    "id": randomProvinceCityCounty[0],
                    "logicalname": "new_province"
                },
                "new_county_id": {
                    # "name": " ",
                    "id": randomProvinceCityCounty[4],
                    "logicalname": "new_county"
                },
                "new_city_id": {
                    # "name": " ",
                    "id": randomProvinceCityCounty[2],
                    "logicalname": "new_city"
                }
            }
        }
        res = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
        print(res.text)


if __name__ == '__main__':
    createPro()
