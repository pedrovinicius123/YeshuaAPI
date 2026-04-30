def req_response(status_code:int=200, message="", data=None):
    return {
        "status_code":status_code,
        "message": message,
        "data":data
    }
