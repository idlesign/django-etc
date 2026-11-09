from django.shortcuts import render


def index(request):
    return render(request, 'this.html', {'postfix_var': 'dynamic'})
