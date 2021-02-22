import string
import random
import requests
import json
from login import get_token
from getRandomData import getRandomProvinceCityCounty
# -*- coding: utf-8 -*-
token = get_token()


def createAccAndContact():
    while True:
        try:
            randomProvinceCityCounty = getRandomProvinceCityCounty(u'1.xls', 0)
            urlAcc = 'https://dev.recloud.com.cn:5202/api/dynamic/account/SaveAndFetch'
            headersAcc = {'Authorization': 'Bearer ' + token,
                          'Accept-Language': 'zh-CN'}
            cus = ''.join(
                random.sample(
                    string.ascii_letters +
                    string.digits,
                    5))
            tellist = ['186', '187', '188', '189']
            tele = random.choice(tellist) + \
                ''.join(random.sample('0123456789', 8))
            tele1 = random.choice(tellist) + \
                ''.join(random.sample('0123456789', 8))
            bodyAcc = {
                "ownerid": {
                    "id": "67781f72-450c-e611-80bc-000c292d3ec1",
                    "logicalname": "systemuser",
                    "name": "Administrator"
                },
                "accounttypecode": 2,  # 客户类型 默认2   1:2B   2:2C
                "accountratingcode": 1,  # 客户等级 默认1   1:A   2:B   3::C
                "name": "gavin" + cus,
                # "accountnumber": " ",  # 客户编号
                "telephone1": tele,
                "new_region_id": {  # 大区与省无关联，所以直接写死
                    "id": "eb3b0101-0000-7f41-0000-05e59c2f2d13",
                    "name": "华南区",
                    "logicalName": "new_region"
                },
                "new_provinceid": {
                    # "name": "江苏省",
                    "id": randomProvinceCityCounty[0],
                    "logicalname": "new_province"
                },
                "new_cityid": {
                    # "name": "苏州市",
                    "id": randomProvinceCityCounty[2],
                    "logicalname": "new_city"
                },
                "new_countyid": {
                    # "name": "姑苏区",
                    "id": randomProvinceCityCounty[4],
                    "logicalname": "new_county"
                },
                "address1_composite": randomProvinceCityCounty[5] + "街道"
            }
            resAcc = requests.post(
                urlAcc,
                data=json.dumps(bodyAcc),
                headers=headersAcc,
                verify=False)
            print('客户：%s' % resAcc.text)
            if resAcc.json()['ErrorCode'] == 0:
                accountid = resAcc.json()['Data']['accountid']
                """新增联系人"""
                urlCon = 'https://dev.recloud.com.cn:5202/api/dynamic/contact/SaveAndFetch'
                headersCon = {'Authorization': 'Bearer ' + token,
                              'Accept-Language': 'zh-CN'}
                bodyCon1 = {
                    "new_origin": 1,
                    "parentcustomerid": {
                        "id": accountid,
                        # "name": "",
                        "logicalName": "account"
                    },
                    "ownerid": {
                        "id": "67781f72-450c-e611-80bc-000c292d3ec1",
                        "logicalname": "systemuser",
                        "name": "Administrator"
                    },
                    "fullname": "gavin" + cus + "的联系人1",
                    "mobilephone": tele1,
                    "new_region_id": {  # 大区与省无关联，所以直接写死
                        "id": "eb3b0101-0000-7f41-0000-05e59c2f2d13",
                        "name": "华南区",
                        "logicalName": "new_region"
                    },
                    "new_province_id": {
                        # "name": "江苏省",
                        "id": randomProvinceCityCounty[0],
                        "logicalname": "new_province"
                    },
                    "new_city_id": {
                        # "name": "苏州市",
                        "id": randomProvinceCityCounty[2],
                        "logicalname": "new_city"
                    },
                    "new_county_id": {
                        # "name": "姑苏区",
                        "id": randomProvinceCityCounty[4],
                        "logicalname": "new_county"
                    },
                    "address1_name": randomProvinceCityCounty[5] + "街道"
                }
                res1 = requests.post(
                    urlCon,
                    data=json.dumps(bodyCon1),
                    headers=headersCon,
                    verify=False)
                print('联系人：%s' % res1.text)
            elif resAcc.text.__contains__('存在相同手机号的'):
                print("===号码重复了!!!存在相同手机号=============")
                continue
            else:
                print('=====服务错误请重试=====================')
                continue
        except BaseException:
            print('===============出现异常了===================')


if __name__ == '__main__':
    createAccAndContact()
