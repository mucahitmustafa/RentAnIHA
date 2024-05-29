from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from django.http import HttpResponse
from dashboard.models import Rental, Iha, Category
from django.contrib.auth.models import User


def rentals_view(request):
    if request.user.is_anonymous:
        return redirect('login')

    if request.method == 'POST':
        if not request.user.is_staff:
            return HttpResponse('Unauthorized', status=401)
        return render(request, 'rentals_new.html')
        pass  # TODO: Sadece Yönetici. Kiralama oluşturma sayfası.

    else:
        if request.user.is_staff:
            _rentals = Rental.objects.filter()
        else:
            _rentals = Rental.objects.filter(user=request.user)

        if not _rentals.exists():
            _rentals = []
        return render(request, 'rentals_list.html', {'rentals': _rentals})


def rental_view(request, id):
    if request.user.is_anonymous:
        return redirect('login')

    _rental = get_object_or_404(Rental, id=id)

    if request.method == 'DELETE' and request.user.is_staff:
        try:
            _rental.delete()
            return HttpResponse('{}', status=200)
        except Exception as e:
            return HttpResponse('{}'.format(e), status=400)

    elif request.method == 'PUT' and (request.user.is_staff or _rental.user == request.user):
        # TODO: Edit rental.
        return render(request, 'rentals_edit.html')

    elif request.method == 'PATCH' and (request.user.is_staff or _rental.user == request.user):
        try:
            _rental.is_returned = True
            _rental.save()
        except Exception as e:
            return HttpResponse('{}'.format(e), status=400)

        return HttpResponse('{}', status=200)

    return HttpResponse('Unauthorized', status=401)


def members_view(request):
    if request.user.is_anonymous:
        return redirect('login')
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    _members = User.objects.filter()
    if not _members.exists():
        _members = []
    return render(request, 'members_list.html', {'members': _members})


def member_view(request, id):
    if request.user.is_anonymous:
        return redirect('login')
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    _user = get_object_or_404(User, id=id)
    if request.method == 'DELETE':
        try:
            _user.delete()
            return HttpResponse('{}', status=200)
        except Exception as e:
            return HttpResponse('{}'.format(e), status=400)

    else:
        return render(request, 'members_detail.html', {'member': _user})


def iha_categories_view(request):
    if request.user.is_anonymous:
        return redirect('login')
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    _categories = Category.objects.filter()
    if not _categories.exists():
        _categories = []
    return render(request, 'categories_list.html', {'categories': _categories})


def ihas_view(request):
    if request.user.is_anonymous:
        return redirect('login')

    if request.method == 'POST':
        if not request.user.is_staff:
            return HttpResponse('Unauthorized', status=401)

        return render(request, 'ihas_new.html')
        pass  # TODO: Sadece Yönetici. İHA oluşturma sayfası.

    else:
        _ihas = Iha.objects.filter()
        if not _ihas.exists():
            _ihas = []

        _categories = Category.objects.filter()
        if not _categories.exists():
            _categories = []

        return render(request, 'ihas_list.html', {'ihas': _ihas, 'categories': _categories})


def iha_view(request, id):
    if request.user.is_anonymous:
        return redirect('login')

    _iha = get_object_or_404(Iha, id=id)

    if request.method == 'DELETE':
        if not request.user.is_staff:
            return HttpResponse('Unauthorized', status=401)
        try:
            _iha.delete()
            return HttpResponse('{}', status=200)
        except Exception as e:
            return HttpResponse('{}'.format(e), status=400)

    elif request.method == 'PUT':
        if not request.user.is_staff:
            return HttpResponse('Unauthorized', status=401)
        return render(request, 'ihas_edit.html')
        pass  # TODO: Sadece Yönetici. İHA bilgilerini güncelleme sayfası.

    else:
        return render(request, 'ihas_detail.html', {'iha': _iha})
