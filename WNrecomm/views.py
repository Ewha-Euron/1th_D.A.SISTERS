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
        selected = request.GET.get('chb')
        print(selected)
        if '6' in selected:
            return render(request, 'keyword.html')
        return render(request, 'q3.html')

def result(request):
    return render(request, 'result.html')