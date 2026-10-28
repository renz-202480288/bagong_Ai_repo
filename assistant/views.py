from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google import genai
import json
import os


def service_worker(request):
    sw_path = os.path.join(settings.BASE_DIR, 'assistant', 'static', 'sw.js')
    
    try:
        with open(sw_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='application/javascript')
    except FileNotFoundError:
        return HttpResponse("Service worker not found", status=404)
    
def index_view(request):
    return render(request, 'index.html')

client = genai.Client(api_key=settings.GEMINI_API_KEY)

@csrf_exempt
def generate_ai_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_prompt = data.get("prompt", "")
            
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=user_prompt,
            )
            
            return JsonResponse({"status": "success", "reply": response.text})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "invalid method"}, status=400)