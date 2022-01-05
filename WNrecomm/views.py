from django.shortcuts import render

def main(request):
    return render(request, 'main.html')


def q_base(request):
    return render(request, 'q_base.html')

def q1(request):
    return render(request, 'q1.html')

def q2(request):
    return render(request, 'q2.html')

def keyword(request):
    return render(request, 'keyword.html')

def q3(request):
    if request.method == 'GET':
        selected = request.GET.getlist('impt')
        print(selected)
        if '7' in selected:
            return render(request, 'keyword.html')
        else:
            return render(request, 'q3.html')

def result(request):
    return render(request, 'result.html')