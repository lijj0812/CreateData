import psycopg2
import requests
import json
import random
from login import get_token
# 查询没有服务站的城市
# select distinct a.new_name,a.new_province_idname from new_city a,new_srv_station b
# where a.new_name not in (select distinct new_city_idname from new_srv_station) and b.new_name not like 'Station%'

token = get_token()
conn = psycopg2.connect(database='saascrmcloud_data2', user='postgres', password='p@ssw0rd', host='192.168.7.176',
                        port='5432')
curs = conn.cursor()

curs.execute("select distinct new_city_idname from new_srv_station")  # 查出有服务站的城市list
nowCitysList = curs.fetchall()

curs.execute(
    "select new_name from new_city where new_province_idname != '台湾省' and new_province_idname != '澳门特别行政区' and new_province_idname != '香港特别行政区'")
allCitysList = curs.fetchall()  # 除去港澳台的所有城市list

for l in nowCitysList:
    if l in allCitysList:
        allCitysList.remove(l)

usefulList = allCitysList  # 没有服务站的城市list
for ll in usefulList:
    if ll[0] == '省直辖行政单位-湖北省':
        usefulList.remove(ll)
"""
目前还有112个城市没有服务站(除了港澳台)，即usefulList，给这112个城市加上服务站 (这112个城市里有9个城市没有县区，所以只加103个服务站)
"""


def extraCreate():
    StaCount = 500
    phoneCount = 100000
    zzidList = []
    for cityIndex, city in enumerate(usefulList):
        '''通过城市名查下面的区县 随机取一个区县，这里就取第一个'''
        # odata接口通过城市名查下面的区县
        urlSearchCounty = 'https://dev.recloud.com.cn:7181/api/dynamic/new_county?$filter=new_city_idname eq ' + \
                          city[0] + '&$select=new_name'
        headerSearchCounty = {'Authorization': 'Bearer ' + token,
                              'Accept-Language': 'zh-CN'}
        resCounty = requests.get(urlSearchCounty, headers=headerSearchCounty, verify=False)
        print(resCounty.json())
        if resCounty.json()['Data']['Entities'] != []:
            countyId = resCounty.json()['Data']['Entities'][0]['new_countyid']  # 区县id

            '''通过城市名对应的省市id'''
            # odata接口通过城市名查对应的省市id
            urlSearchProvinceAndCityId = 'https://dev.recloud.com.cn:7181/api/dynamic/new_city?$filter=new_name eq ' + \
                                         city[0] + '&$select=new_province_id,new_cityid'
            headerSearchProvinceAndCityId = {'Authorization': 'Bearer ' + token,
                                             'Accept-Language': 'zh-CN'}
            resSearchProvinceAndCityId = requests.get(urlSearchProvinceAndCityId, headers=headerSearchProvinceAndCityId,
                                                      verify=False)
            cityId = resSearchProvinceAndCityId.json()['Data']['Entities'][0]['$id']  # 市id
            provinceId = resSearchProvinceAndCityId.json()['Data']['Entities'][0]['new_province_id']['id']  # 省id

            """
            创建服务站主档
            """
            StaCount += 1
            discount = '%.1f' % random.random()  # [0,1]的随机一位小数
            # print(discount)
            if float(discount) < 0.7:
                discount = 0.7
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
                    "id": provinceId,
                    # "name": " ",
                    "logicalName": "new_province"
                },
                "new_city_id": {
                    "id": cityId,
                    # "name": " ",
                    "logicalName": "new_city"
                },
                "new_county_id": {
                    "id": countyId,
                    # "name": " ",
                    "logicalName": "new_county"
                },
                "new_town_id": None,  # 街道（镇）
                "new_discount": str(discount),
                "new_level": 2,  # 服务站级别
                "new_type": 1,  # 服务站类型
                "new_code": "S" + str(StaCount),  # 服务站编码
                "new_name": "Station" + str(StaCount)  # 服务站名称
                }
            res = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
            stationid = res.json()['Data']['new_srv_stationid']
            for k in range(10):  # 每个服务站的服务站长数量
                """
                创建服务站长
                """
                phoneCount += 1
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
                    "new_name": "S" + str(StaCount) + "站长" + str(k + 1),  # 服务站长名字
                    "new_personalrole": 2,  # random.randint(1, 2),  人员角色 1服务人员 2服务站长 3社会工程师
                    "new_outterworker_status": None,
                    "new_phone": '1888' + "%07d" % phoneCount,
                    "new_job": 3,  # random.randint(1, 3),  岗位 1初级工程师 2中级 3高级
                    "new_province_id": {
                        # "name": " ",
                        "id": provinceId,
                        "logicalname": "new_province"
                    },
                    "new_city_id": {
                        # "name": " ",
                        "id": cityId,
                        "logicalname": "new_city"
                    },
                    "new_county_id": {
                        "id": countyId,
                        # "name": " ",
                        "logicalName": "new_county"
                    },
                    "new_address": "S" + str(StaCount) + "站长" + str(k + 1) + "的详细地址"
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
                phoneCount += 1
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
                    "new_name": "S" + str(StaCount) + "人员" + str(l + 1),  # 服务人员名字
                    "new_personalrole": 1,  # random.randint(1, 2),  人员角色 1服务人员 2服务站长 3社会工程师
                    "new_outterworker_status": None,
                    "new_phone": '1888' + "%07d" % phoneCount,
                    "new_job": random.randint(1, 2),  # random.randint(1, 3),  岗位 1初级工程师 2中级 3高级
                    "new_province_id": {
                        # "name": " ",
                        "id": provinceId,
                        "logicalname": "new_province"
                    },
                    "new_city_id": {
                        # "name": " ",
                        "id": cityId,
                        "logicalname": "new_city"
                    },
                    "new_county_id": {
                        "id": countyId,
                        # "name": " ",
                        "logicalName": "new_county"
                    },
                    "new_address": "S" + str(StaCount) + "人员" + str(l + 1) + "的详细地址"
                }
                resW = requests.post(urlW, data=json.dumps(bodyW), headers=headersW, verify=False)
                if l == 189:
                    """同步"""
                    urlSyncW = 'https://dev.recloud.com.cn:7181/api/custom/new_service_bg/Worker/SyncUnitAndUser'
                    headerSyncW = {'Authorization': 'Bearer ' + token,
                                   'Accept-Language': 'zh-CN'}
                    bodySyncW = {"stationId": stationid}
                    resSyncW = requests.post(urlSyncW, data=json.dumps(bodySyncW), headers=headerSyncW,
                                             verify=False)
                    print(resSyncW.text)
                    print("进度:%d" % (StaCount-500))


if __name__ == '__main__':
    extraCreate()
