from django.shortcuts import render

# Create your views here.
def volunter(request):
    return render(request, 'volunteers/volunter.html')
