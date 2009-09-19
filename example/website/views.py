from django.shortcuts import render_to_response


def home(request):
    return render_to_response('home.html')


def say_hello(request):
    x = 1/0
    first_name = request.POST.get('first_name')
    return render_to_response('hello.html', { 'first_name': first_name })
