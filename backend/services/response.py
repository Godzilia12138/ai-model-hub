def success(model, data):
    return {
        "success": True,
        "model": model,
        "data": data,
        "error": None
    }


def fail(model, error):
    return {
        "success": False,
        "model": model,
        "data": None,
        "error": str(error)
    }