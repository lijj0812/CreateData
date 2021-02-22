import random
import xlrd


def getRandomProvinceCityCounty(filename, index):
    """
    随机获取一个省市县的名称和id
    :param filename: '省市县.xlsx'
    :param index: 0
    :return: 例如['3fd0ec1b-8d41-e611-80c3-000c292d3ec1', '广东省',
                  'ea43048b-8f41-e611-80c3-000c292d3ec1', '清远市',
                  'eaa96ef7-9041-e611-80c3-000c292d3ec1', '英德市']
    """
    xlsx = xlrd.open_workbook(filename)
    sheet = xlsx.sheet_by_index(index)
    rows = sheet.nrows
    row = random.randint(2, rows)
    data = sheet.row_values(row - 1)
    return data


def getRandomGroupModelProduct(filename, index):
    """
    随机获取一个产品线、产品型号、成品物料的名称和id
    :param filename: '成品.xlsx'
    :param index: 0
    :return: 例如['58e60001-0000-7fd7-0000-05d610151079', 'PG14',
                  '58e60001-0000-7f56-0000-05d6101b1db7', 'PM268',
                  '58e60001-0000-7fb1-0000-05d6110ee3e1', 'Product5348']

    """
    xlsx = xlrd.open_workbook(filename)
    sheet = xlsx.sheet_by_index(index)
    rows = sheet.nrows
    row = random.randint(2, rows)
    data = sheet.row_values(row - 1)
    return data


def getRandomAccCon(filename, index):
    """
    随机获取一个客户和对应联系人的名称和id
    :param filename: '客户联系人.xlsx'
    :param index: 0
    :return: 例如['265d0001-0000-7f20-0000-05d61392f7a5', '客户3026',
                  'e84a0001-0000-7f2b-0000-05d61392fe48', '客户3026的联系人']

    """
    xlsx = xlrd.open_workbook(filename)
    sheet = xlsx.sheet_by_index(index)
    rows = sheet.nrows
    row = random.randint(2, rows)
    data = sheet.row_values(row - 1)
    return data

# if __name__ == '__main__':
# # #     # data1 = getRandomProvinceCityCounty(u'省市县.xlsx', 0)
# #     data2 = getRandomGroupModelProduct(u'成品.xlsx', 0)
#     data3 = getRandomAccCon(u'客户联系人.xlsx', 0)
#     print(data3)
