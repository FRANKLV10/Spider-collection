import list_data
import time

def get_industry(companyCate1, companyCate2 ):
    """

    @param companyCate1: 行业代码1
    @param companyCate2: 行业代码2
    @return:
    """
    industry_data = list_data.industry()
    for i in industry_data:
        if i["primInduCode"] == companyCate1:
            secInduData = i["secList"]

            for j in secInduData:
                if j["secInduCode"] == companyCate2:
                    # terInduData = j["terList"]
                    return j["secnduName"]
                    # for k in terInduData:
                    #     if k["terInduCode"] == cate:
                    #         pass


def get_area(areaCode):
    '''
    获取地区
    中文名称
    areaCode：区域代码
    '''
    areaCode = str(areaCode)
    area = ''
    area_data = list_data.area()
    for i in area_data:
        if i["areaCode"] ==  areaCode[:2] and "city" in i:
            city = i["city"]
            for j in city:
                if j["areaCode"] == areaCode[:4]:
                    district = j["district"]
                    if areaCode[4:6] == "00":
                        area = j["name"]
                    else:
                        for k in district:
                            if k["areaCode"] == areaCode:
                                area = k["name"]
                            # print(area)



        elif i["areaCode"] ==  areaCode[:2]:
            area = i["name"]
            # print(area)

    return area

#
# def get_area_code(area):
#     area_code = ''
#     area_data = list_data.area()
#
#     for i in area_data:
#         if i['name'] == area:
#             area_code =i['area_code']
#     for



if __name__ == '__main__':
    # get_industry("C","35","351")

    area = get_area("520100")
    print(area)

