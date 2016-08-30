from django.shortcuts import render


def home(request):
    # It actually doesn't change anything already
    return render(request, "main/home.html", {'message': 'hi, there!'})