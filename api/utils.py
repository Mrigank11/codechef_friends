from django.http import JsonResponse


def APIResponse(result=None, error=None):
    return JsonResponse({
        "success": not error,
        "result": result or error
    })
