from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_GET
def health_check(request):
    return JsonResponse({"status": "ok", "service": "baby-care"})