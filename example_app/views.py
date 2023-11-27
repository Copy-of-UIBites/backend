from django.http import HttpResponse

def index(request):
    return HttpResponse("<html><body><h1>Hello, World!</h1></body></html>", content_type="text/html")
