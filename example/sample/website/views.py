from django.shortcuts import render_to_response


def home(request):
    return render_to_response('home.html')


def say_hello(request):
    first_name = request.POST['first_name']
    return render_to_response('hello.html', { 'first_name': first_name })
