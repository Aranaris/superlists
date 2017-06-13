from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def home_page(request):   
    return render(request, 'home.html', {
        'new_item_text': request.POST.get('item_text', ''),
        })
