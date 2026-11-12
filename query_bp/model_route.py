from dataclasses import dataclass
from database.select import select_dict
from query_bp.config import QUERY_CONFIG

@dataclass
class ResultInfo:
    result: dict
    status: bool
    err_message: str


def model_route(provider,query_info, params):
    filename = query_info.get("sql")
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