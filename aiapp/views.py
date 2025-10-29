from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from . import state

def home_view(request):
    return render(request, "test_form.html")

@csrf_exempt
def generate_local_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "use POST"}, status=405)

    prompt = request.POST.get("prompt")
    if not prompt:
        return JsonResponse({"error": "no prompt"}, status=400)

    try:
        image_url = state.generator.generate(prompt)
    except Exception as e:
        return JsonResponse(
            {"error": "generation_failed", "detail": str(e)},
            status=500
        )

    return JsonResponse({
        "image_url": image_url,
        "prompt_used": prompt
    })
