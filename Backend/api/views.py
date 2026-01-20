from django.http import HttpResponse

# 요청이 오면 "Hello World"를 응답하는 함수
def hello_world(request):
    return HttpResponse("Hello World")
