from rest_framework.response import Response
from rest_framework import status as http_status
from common import errorcode
from common.exceptions import RequestInputParserError
from datetime import datetime, timedelta
import math
import re

# Response回傳
def api_response(
    result=None,
    status=http_status.HTTP_200_OK,
    code=errorcode.OK,
    message=None,
    **kargs,
):
    """
        Response回傳
    """
    content = {}
    if type(result) is not list:
        if result is None:
            content["result"] = []
        elif type(result) is dict and "token" in result:
            content = result
        else:
            content["result"] = [result]
    else:
        content["result"] = result

    if "code" not in content:
        content["code"] = code
    if message != None:
        content["message"] = message
    return Response(content, status=status, content_type="application/json", **kargs)


# input檢查
def get_request_input(
    request: object, method: str = "POST", required_data: list = [], router: dict = {}
):
    """
        input檢查
    """
    if method == "GET":
        input_data = dict(request.query_params)
        for key in input_data:
            if type(input_data[key]) is list and len(input_data[key]) == 1:
                input_data[key] = input_data[key][0]
    else:
        input_data = dict(request.data)

    for item in required_data:
        if item not in input_data:
            raise RequestInputParserError("Required data not found: {0}".format(item))

    # Dirty fix
    if request._read_started:
        request._read_started = False
    return input_data, router

# 頁數計算
def page_helper(page, limit_by_page, data_count):
    """
        para:
            - page : 第幾頁
            - limit_by_page : 一頁限制回傳?筆
            - data_count : 資料總比數
        return:
            - page :第幾頁
            - page_total : 總頁數
            - start : 陣列開始
            - end :陣列結束
    """
    try:
        page = int(page)
    except:
        page = 0
    start = 0
    if page > 1:
        start = (page - 1) * limit_by_page
    else:
        page = 1
    end = start + limit_by_page
    try:
        page_total = math.ceil(data_count / limit_by_page)
    except:
        page_total = 1
    return page, page_total, start, end

# 手機正規化 
def normalize_phone_number(phone_number):
    digits = re.sub(r'\D', '', phone_number)
    if len(digits) == 10:
        return '{}-{}-{}'.format(digits[:4], digits[4:7], digits[7:])
    else:
        raise ValueError("Invalid phone number. Must contain exactly 10 digits.")