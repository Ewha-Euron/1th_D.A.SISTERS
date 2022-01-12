from django.shortcuts import render
#from .models import Post

def main(request):
    return render(request, 'main.html')


def q_base(request):
    return render(request, 'q_base.html')

def q1(request):
    return render(request, 'q1.html')

def q2(request):
    if request.method == 'GET':
        print(request.GET.get('adultchild')) # adult_yes / adult_no
        print(request.GET.get('finished')) # finish_yes / finish_no
    return render(request, 'q2.html')

def q3(request):
    if request.method == 'GET':
        selected = request.GET.get('chb')
        print(selected) # 순서대로 리스트 형태로
        return render(request, 'q3.html')

def result(request):
    return render(request, 'result.html')
'''
def novel_list(request):
    qs = Post.objects.all()
    q = request.Get.get('search', '')
    if q:
        qs = qs.filter(message__icontains=q)
    return render(request, 'q3.html', {'search':qs, 'q':q})
'''
