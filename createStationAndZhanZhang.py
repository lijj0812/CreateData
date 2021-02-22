import requests
import json
import random
from login import get_token
from getRandomData import getRandomGroupModelProduct, getRandomProvinceCityCounty

token = get_token()


def createStationWorker():
    """
    创建服务站主档
    """
    # print(randomProvinceCityCounty)
    count = 0
    zzidList = []
    for j in range(500):  # 服务站数量
        discount = '%.1f' % random.random()  # [0,1]的随机一位小数
        # print(discount)
        if float(discount) < 0.7:
            discount = 0.7
        randomProvinceCityCounty = getRandomProvinceCityCounty(u'省市县.xlsx', 0)
        url = 'https://dev.recloud.com.cn:7181/api/dynamic/new_srv_station/SaveAndFetch'
        headers = {'Authorization': 'Bearer ' + token,
                   'Accept-Language': 'zh-CN'}
        body = {
            "eeee": "3424234",
            "new_settledbyothers": 2,  # 是否代结
            "new_limitamount": True,  # 是否控制额度
            "ownerid": {
                "id": "67781f72-450c-e611-80bc-000c292d3ec1",
                "logicalname": "systemuser",
                "name": "Administrator"
            },
            "new_region_id": {  # 大区与省无关联，所以直接写死
                "id": "8ec437ec-8e16-e611-80c0-000c292d3ec1",
                "name": "华东区",
                "logicalName": "new_region"
            },
            "new_province_id": {
                "id": randomProvinceCityCounty[0],
                # "name": " ",
                "logicalName": "new_province"
            },
            "new_city_id": {
                "id": randomProvinceCityCounty[2],
                # "name": " ",
                "logicalName": "new_city"
            },
            "new_county_id": {
                "id": randomProvinceCityCounty[4],
                # "name": " ",
                "logicalName": "new_county"
            },
            "new_town_id": None,  # 街道（镇）
            "new_discount": str(discount),
            "new_level": 2,  # 服务站级别
            "new_type": 1,  # 服务站类型
            "new_code": "S" + str(j + 1),  # 服务站编码
            "new_name": "Station" + str(j + 1)  # 服务站名称
        }
        res = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
        stationid = res.json()['Data']['new_srv_stationid']
        for k in range(10):  # 每个服务站的服务站长数量
            """
            创建服务站长
            """
            count += 1
            urlWorker = 'https://dev.recloud.com.cn:7181/api/dynamic/new_srv_worker/SaveAndFetch'
            headersWorker = {'Authorization': 'Bearer ' + token,
                             'Accept-Language': 'zh-CN'}
            bodyWorker = {
                "new_workyear": 0,
                "new_trainnumber": 0,
                "new_load": 100,
                "ownerid": {
                    "id": "67781f72-450c-e611-80bc-000c292d3ec1",
                    "logicalname": "systemuser",
                    "name": "Administrator"
                },
                "new_offstate": 10,  # 在岗状态 10在岗 20请假
                "new_srv_station_id": {
                    "id": stationid,  # 服务站id
                    "logicalname": "new_srv_station",
                    # "name": " "
                },
                "new_name": "S" + str(j + 1) + "站长" + str(k + 1),  # 服务站长名字
                "new_personalrole": 2,  # random.randint(1, 2),  人员角色 1服务人员 2服务站长 3社会工程师
                "new_outterworker_status": None,
                "new_phone": '1888' + "%07d" % count,
                "new_job": 3,  # random.randint(1, 3),  岗位 1初级工程师 2中级 3高级
                "new_province_id": {
                    # "name": " ",
                    "id": randomProvinceCityCounty[0],
                    "logicalname": "new_province"
                },
                "new_city_id": {
                    # "name": " ",
                    "id": randomProvinceCityCounty[2],
                    "logicalname": "new_city"
                },
                "new_county_id": {
                    "id": randomProvinceCityCounty[4],
                    # "name": " ",
                    "logicalName": "new_county"
                },
                "new_address": "S" + str(j + 1) + "站长" + str(k + 1) + "的详细地址"
            }
            res = requests.post(urlWorker, data=json.dumps(bodyWorker), headers=headersWorker, verify=False)
            if k == 9:
                """同步"""
                urlSync = 'https://dev.recloud.com.cn:7181/api/custom/new_service_bg/Worker/SyncUnitAndUser'
                headerSync = {'Authorization': 'Bearer ' + token,
                              'Accept-Language': 'zh-CN'}
                bodySync = {"stationId": stationid}
                resSync = requests.post(urlSync, data=json.dumps(bodySync), headers=headerSync, verify=False)
                print(resSync.text)
                '''更改负责人'''
                zzidList = []  # 很关键 一开始没注意 每次更改负责人前都要清空zzidlist 不然会累加
                urlUser = 'https://dev.recloud.com.cn:7181/api/dynamic/systemuser?$filter=new_stationid/id eq ' + stationid + '&$select=systemuserid'
                headerUser = {'Authorization': 'Bearer ' + token,
                              'Accept-Language': 'zh-CN'}
                rUser = requests.get(url=urlUser, headers=headerUser, verify=False)
                List = rUser.json()['Data']['Entities']  # 放站长id的list
                for index, dict in enumerate(List):
                    zzid = dict['$id']
                    zzidList.append(zzid)

                urlC = 'https://dev.recloud.com.cn:7181/api/dynamic/new_srv_station/SaveAndFetch'
                headersC = {'Authorization': 'Bearer ' + token,
                            'Accept-Language': 'zh-CN'}
                bodyC = {
                    "ownerid": {
                        "id": zzidList[random.randint(0, len(zzidList) - 1)],
                        # "name": " ",
                        "logicalName": "systemuser"
                    },
                    "$id": stationid
                }
                r = requests.post(urlC, data=json.dumps(bodyC), headers=headersC, verify=False)
                # print(stationid)
                # print(r.text)
        for l in range(190):  # 每个服务站服务人员角色数量
            """
            创建服务人员
            """
            count += 1
            urlW = 'https://dev.recloud.com.cn:7181/api/dynamic/new_srv_worker/SaveAndFetch'
            headersW = {'Authorization': 'Bearer ' + token,
                        'Accept-Language': 'zh-CN'}
            bodyW = {
                "new_workyear": 0,
                "new_trainnumber": 0,
                "new_load": 50,
                "ownerid": {
                    "id": "67781f72-450c-e611-80bc-000c292d3ec1",
                    "logicalname": "systemuser",
                    "name": "Administrator"
                },
                "new_offstate": 10,  # 在岗状态 10在岗 20请假
                "new_srv_station_id": {
                    "id": stationid,  # 服务站id
                    "logicalname": "new_srv_station",
                    # "name": " "
                },
                "new_name": "S" + str(j + 1) + "人员" + str(l + 1),  # 服务人员名字
                "new_personalrole": 1,  # random.randint(1, 2),  人员角色 1服务人员 2服务站长 3社会工程师
                "new_outterworker_status": None,
                "new_phone": '1888' + "%07d" % count,
                "new_job": random.randint(1, 2),  # random.randint(1, 3),  岗位 1初级工程师 2中级 3高级
                "new_province_id": {
                    # "name": " ",
                    "id": randomProvinceCityCounty[0],
                    "logicalname": "new_province"
                },
                "new_city_id": {
                    # "name": " ",
                    "id": randomProvinceCityCounty[2],
                    "logicalname": "new_city"
                },
                "new_county_id": {
                    "id": randomProvinceCityCounty[4],
                    # "name": " ",
                    "logicalName": "new_county"
                },
                "new_address": "S" + str(j + 1) + "人员" + str(l + 1) + "的详细地址"
            }
            resW = requests.post(urlW, data=json.dumps(bodyW), headers=headersW, verify=False)
            if l == 189:
                """同步"""
                urlSyncW = 'https://dev.recloud.com.cn:7181/api/custom/new_service_bg/Worker/SyncUnitAndUser'
                headerSyncW = {'Authorization': 'Bearer ' + token,
                               'Accept-Language': 'zh-CN'}
                bodySyncW = {"stationId": stationid}
                resSyncW = requests.post(urlSyncW, data=json.dumps(bodySyncW), headers=headerSyncW, verify=False)
                print(resSyncW.text)
                print("进度:%d" % (j+1))


if __name__ == '__main__':
    createStationWorker()
