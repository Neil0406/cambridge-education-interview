from functools import wraps
import time
from common import errorcode
from rest_framework import status as http_status
from common.helperfunc import get_request_input, api_response
from common.exceptions import RequestInputParserError
from django.conf import settings
from common.logs_writer import logswriter
from django.conf import settings

# input檢查
class InputCheck:
    def __init__(
        self, SystemName=None, FileName="log", RemainDays=settings.LOGS_REMOVE_DAYS
    ):
        self.logswriter_ = logswriter(
            SystemName=SystemName, FileName=FileName, RemainDays=RemainDays
        )

    def key_check(self, required_data=None):
        if required_data is None:
            required_data = []
        logswriter_ = self.logswriter_

        def f(func):
            @wraps(func)
            def wrapper(self, *args, **router):
                request = args[0]
                logswriter_.write_log(massage=request.META)
                try:
                    input_data, router = get_request_input(
                        request, request.method, required_data, router
                    )
                    ret = func(self, request, input_data, router)
                except RequestInputParserError as e:
                    file, line_num, func_name = logswriter_.get_msg_info()
                    logswriter_.write_log(
                        f"{str(e)}", status="ERROR", error_path=f"{file}: {line_num}"
                    )
                    ret = api_response(
                        result=None,
                        status=http_status.HTTP_400_BAD_REQUEST,
                        code=errorcode.INPUT_ERROR,
                        message=str(e),
                    )
                except Exception as e:
                    file, line_num, func_name = logswriter_.get_msg_info()
                    logswriter_.write_log(
                        f"{str(e)}", status="ERROR", error_path=f"{file}: {line_num}"
                    )
                    ret = api_response(
                        result=None,
                        status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                        code=errorcode.UNKNOW_ERROR,
                        message=str(e),
                    )
                return ret

            return wrapper

        return f


# request method轉換
class RequestMethod:
    def method(self):
        def f(func):
            def wrapper(self, *args, **kwargs):
                method_dic = {
                    "GET": "_get",
                    "POST": "_post",
                    "PUT": "_put",
                    "PATCH": "_patch",
                    "DELETE": "_delete",
                }
                method = args[0].method
                method = method_dic.get(method)
                return func(self, request=args[0], method=method, input_data=args[1])
            return wrapper
        return f


# Function 計時
class Timer:
    def __init__(
        self, SystemName=None, FileName="log", RemainDays=settings.LOGS_REMOVE_DAYS
    ):
        if SystemName:
            self.logswriter_ = logswriter(
                SystemName=SystemName, FileName=FileName, RemainDays=RemainDays
            )

    def timer(self, func):
        logswriter_ = self.logswriter_

        def wrapper(self, *args, **kwargs):
            ret = None
            start = time.time()
            try:
                ret = func(self, *args, **kwargs)
                end = time.time()
                finish = round(end - start, 3)
                m, s = divmod(end - start, 60)
                h, m = divmod(m, 60)
                finish = "%d:%02d:%02d" % (h, m, s)
                logswriter_.write_log(f"{finish}")
            except Exception as e:
                file, line_num, func_name = logswriter_.get_msg_info()
                logswriter_.write_log(
                    f"{str(e)}", status="ERROR", error_path=f"{file}: {line_num}"
                )
            return ret

        return wrapper
