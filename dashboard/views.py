import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404

from dashboard.models import Rental, Iha, Category


def rentals_view(request):
    if request.user.is_anonymous:
        return redirect('login')

    if request.method == 'POST':
        try:
            _rental = Rental()
            _body = json.loads(request.body)
            _rental.start_date = _body['startDate']
            _rental.end_date = _body['endDate']
            _rental.user = User.objects.get(id=_body['userId'])
            _rental.iha = Iha.objects.get(id=_body['ihaId'])
            _rental.save()
        except Exception as e:
            return HttpResponse('{}'.format(e), status=400)

        return HttpResponse('{}', status=200)

    else:
        if request.user.is_staff:
            _rentals = Rental.objects.all()
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
        try:
            _body = json.loads(request.body)
            _rental = Rental.objects.get(id=id)
            _rental.start_date = _body['startDate']
            _rental.end_date = _body['endDate']
            _rental.save()
        except Exception as e:
            return HttpResponse('{}'.format(e), status=400)

        return HttpResponse('{}', status=200)

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

    _members = User.objects.all()
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

    return HttpResponse('Unauthorized', status=401)


def iha_categories_view(request):
    if request.user.is_anonymous:
        return redirect('login')
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    if request.method == 'POST':
        if not request.user.is_staff:
            return HttpResponse('Unauthorized', status=401)

        try:
            _body = json.loads(request.body)
            _category = Category()
            _category.name = _body['name']
            _category.added_date = timezone.now()
            _category.save()
            return HttpResponse('{}', status=200)
        except Exception as e:
            return HttpResponse('{}'.format(e), status=400)

    else:
        _categories = Category.objects.all()
        if not _categories.exists():
            _categories = []
        return render(request, 'categories_list.html', {'categories': _categories})


def iha_category_view(request, id):
    if request.user.is_anonymous:
        return redirect('login')

    if request.user.is_staff and request.method == 'PUT':
        try:
            _category = get_object_or_404(Category, id=id)
            _body = json.loads(request.body)
            _category.name = _body['name']
            _category.save()
        except Exception as e:
            return HttpResponse('{}'.format(e), status=400)

        return HttpResponse('{}', status=200)

    elif request.user.is_staff and request.method == 'DELETE':
        try:
            _category = get_object_or_404(Category, id=id)
            _category.delete()
        except Exception as e:
            return HttpResponse('{}'.format(e), status=400)

        return HttpResponse('{}', status=200)

    return HttpResponse('Unauthorized', status=401)


def categorized_ihas_view(request, category):
    if request.user.is_anonymous:
        return redirect('login')

    _category = Category.objects.get(name=category)
    _ihas = Iha.objects.filter(category=_category)
    if not _ihas.exists():
        _ihas = []

    _categories = Category.objects.all()
    if not _categories.exists():
        _categories = []

    return render(request, 'ihas_list.html', {'ihas': _ihas, 'categories': _categories})


def ihas_view(request):
    if request.user.is_anonymous:
        return redirect('login')

    if request.method == 'POST':
        if not request.user.is_staff:
            return HttpResponse('Unauthorized', status=401)

        try:
            _iha = Iha()
            _body = json.loads(request.body)
            _cat = Category.objects.get(name=_body['category'])
            _iha.category = _cat
            _iha.brand = _body['brand']
            _iha.model = _body['model']
            _iha.weight = _body['weight']
            _iha.serial_number = _body['serialNumber']
            _iha.added_date = timezone.now()
            _iha.save()
        except Exception as e:
            return HttpResponse('{}'.format(e), status=400)

        return HttpResponse('{}', status=200)

    else:
        _ihas = Iha.objects.all()
        if not _ihas.exists():
            _ihas = []

        _categories = Category.objects.all()
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

        try:
            _iha = get_object_or_404(Iha, id=id)
            _body = json.loads(request.body)
            _cat = Category.objects.get(name=_body['category'])
            _iha.category = _cat
            _iha.brand = _body['brand']
            _iha.model = _body['model']
            _iha.weight = _body['weight']
            _iha.serial_number = _body['serialNumber']
            _iha.save()
        except Exception as e:
            return HttpResponse('{}'.format(e), status=400)

        return HttpResponse('{}', status=200)

    return redirect('ihas')
