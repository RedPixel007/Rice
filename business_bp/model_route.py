from dataclasses import dataclass
from database.select import select_dict

@dataclass
class ResultInfo:
    result: dict
    status: bool
    err_message: str


def model_route(provider,query_info, params):
    filename = query_info.get("sql")
    print("model plan" + filename)
    if filename is None:
        return ResultInfo(
            result=None,
            status=False,
            err_message='Неизвестный запрос'
        )
    q = provider.get(filename)
    result = select_dict(q, params)

    err_message = ''

    if result:
        return ResultInfo(result=result, status=True, err_message=err_message)
    else:
        return ResultInfo(result=None, status=False, err_message='Что-то пошло не так')