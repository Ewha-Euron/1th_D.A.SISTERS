from django.shortcuts import render

def main(request):
    return render(request, 'main.html')

def q1(request):
    return render(request, 'q1.html')

def result(request):
    return render(request, 'result.html')