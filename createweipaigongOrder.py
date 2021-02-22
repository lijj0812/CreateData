import requests
import json
import datetime
import random
from getRandomData import getRandomProvinceCityCounty, getRandomGroupModelProduct, getRandomAccCon
from login import get_token

token = get_token()


def createWeiPaiGongWO():
    """造服务单"""
    for i in range(5000):
        now_time = datetime.datetime.now()
        randomProvinceCityCounty = getRandomProvinceCityCounty(u'省市县.xlsx', 0)
        randomAccCon = getRandomAccCon(u'客户联系人.xlsx', 0)

        urlSaveZhuDang = 'https://dev.recloud.com.cn:7181/api/dynamic/new_srv_workorder/save'
        headerSaveZhuDang = {'Authorization': 'Bearer ' + token,
                             'Accept-Language': 'zh-CN'}
        bodySaveZhuDang = {
            "new_accepttime": now_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "new_source": 20,  # 服务单来源 20CRM
            "new_surveystatus": 1,  # 回访状态  1待回访 2进行中  3已回访
            "new_samplestatus": 1,  # 抽样状态  1未抽中访 2已抽中  3已回访
            "new_dealstatus": 1,  # 处理状态 1未派工 2已派工 3已响应 4已出发 5已到位 6已拍照 7已完工 8已评价 9已取消 10回访异常 11待确认
            "new_approvalstatus": 1,  # 审核状态 1制单 2审核中 3已审核 4已驳回 5已否决
            "ownerid": {
                "id": "67781f72-450c-e611-80bc-000c292d3ec1",
                "logicalname": "systemuser",
                "name": "Administrator"
            },
            "new_servicemode": 1,  # 服务方式 1需路上用时 2不需路上用时
            "new_type": random.choice([1, 3]),  # 1维修 3保养
            "new_feedbacktel": randomAccCon[4],  # 反馈电话
            "new_contact": randomAccCon[3],  # 反馈人
            "new_province_id": {
                "id": randomProvinceCityCounty[0],
                # "name": "",
                "logicalName": "new_province"
            },
            "new_city_id": {
                "id": randomProvinceCityCounty[2],
                # "name": "",
                "logicalName": "new_city"
            },
            "new_county_id": {
                "id": randomProvinceCityCounty[4],
                # "name": "",
                "logicalName": "new_county"
            },
            "new_address": randomProvinceCityCounty[5] + "街道",
            "new_contact_id": {
                "id": randomAccCon[2],
                # "name": ""
            },
            "new_customerid": {
                "id": randomAccCon[0],
                # "name": "",
                "logicalname": "account"
            },
            "new_servermemo": "来自" + randomAccCon[1] + "的服务单备注",
            "new_memo": "来自" + randomAccCon[1] + "的反馈内容",
            "new_appointmenttime": (now_time + datetime.timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "new_appointmentendtime": (now_time + datetime.timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        }
        resSaveZhuDang = requests.post(urlSaveZhuDang, data=json.dumps(bodySaveZhuDang), headers=headerSaveZhuDang,
                                       verify=False)
        print("保存服务单主档接口", resSaveZhuDang.elapsed.total_seconds())
        workOrderId = resSaveZhuDang.json()['Data']  # 服务单id

        # '''服务单产品明细时，设备档案lookup  这里只返回5个设备档案随机选'''
        # urlProfile = 'https://dev.recloud.com.cn:7181/api/custom/new_service/WorkOrderForm/GetUserProfiles?condition=new_customerid,' + \
        #              randomAccCon[
        #                  0] + '&entityName=new_srv_userprofile&page=1&count=5&select=new_name,new_srv_userprofileid,new_product_id,new_customerid,new_enddate&orderby=new_name%20asc&filter=&filterValue=&countType=0&returnTotalRecordCount=true'
        # headerProfile = {'Authorization': 'Bearer ' + token,
        #                  'Accept-Language': 'zh-CN'}
        # resSN = requests.get(urlProfile, headers=headerProfile, verify=False)
        # ProfileList = resProfile.json()["Data"]
        # profile = ProfileList[random.randint(0, 4)]

        '''查设备档案的设备序列号 这里实时在最新的前20个名字Product开头的设备档案里随机取一个'''
        # odata接口通过设备档案的产品名称查设备序列号
        urlSearchSN = "https://dev.recloud.com.cn:7181/api/dynamic/new_srv_userprofile?$pageindex=1&$pagesize=20&$select=new_name,new_product_id&$filter=contains(new_product_idname,'Product')"
        headerSearchSN = {'Authorization': 'Bearer ' + token,
                          'Accept-Language': 'zh-CN'}
        resSN = requests.get(urlSearchSN, headers=headerSearchSN, verify=False)
        print("查设备档案的设备序列号的接口", resSN.elapsed.total_seconds())
        profileIndex = random.randint(0, 19)
        SN = resSN.json()['Data']['Entities'][profileIndex]['new_name']  # 设备序列号
        profileId = resSN.json()['Data']['Entities'][profileIndex]['new_srv_userprofileid']  # 设备档案id
        productName = resSN.json()['Data']['Entities'][profileIndex]['new_product_id']['name']  # 成品名称
        print(SN)
        print(profileId)
        print(productName)

        '''选中设备档案'''
        urlSaveProfile = 'https://dev.recloud.com.cn:7181/api/dynamic/new_srv_userprofile?$filter=new_name%20eq%20%27' + SN + '%27%20and%20statecode%20eq%200'
        headerSaveProfile = {'Authorization': 'Bearer ' + token,
                             'Accept-Language': 'zh-CN'}
        resSaveProfile = requests.get(urlSaveProfile, headers=headerSaveProfile, verify=False)
        print("选中设备档案的接口", resSaveProfile.elapsed.total_seconds())
        userProfile = resSaveProfile.json()["Data"]['Entities'][0]

        '''保存产品明细'''
        urlSaveLine = 'https://dev.recloud.com.cn:7181/api/dynamic/new_srv_productline/SaveAndFetch'
        headerSaveLine = {'Authorization': 'Bearer ' + token,
                          'Accept-Language': 'zh-CN'}
        bodySaveLine = {
            "new_qty": 1,
            "new_workorder_id": {
                "id": workOrderId,
                # "name": "",
                "logicalName": "new_srv_workorder"
            },
            "new_userprofile_id": {
                "id": profileId,
                # "name": "",
                "logicalname": "new_srv_userprofile"
            },
            "new_userprofile_number": SN,
            "new_product_id": {
                "id": userProfile['new_product_id']['id'],
                # "name": "",
                "logicalname": "product"
            },
            "new_productgroup_id": {
                "id": userProfile['new_productgroup']['id'],
                # "name": "",
                "logicalname": "new_productgroup"
            },
            "new_productmodel_id": {
                "id": userProfile['new_productmodel']['id'],
                # "name": "",
                "logicalname": "new_productmodel"
            },
            "new_enddate": userProfile['FormattedValues']['new_enddate'],
            "new_warranty": 1,  # 保内写死
            "new_buydate": userProfile['FormattedValues']['new_buydate'],
            "new_name": 'Sp_' + productName + '_' + SN
        }
        resSaveLine = requests.post(urlSaveLine, data=json.dumps(bodySaveLine), headers=headerSaveLine, verify=False)
        print("保存产品明细的接口", resSaveLine.elapsed.total_seconds())


if __name__ == '__main__':
    createWeiPaiGongWO()
