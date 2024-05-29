import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
import logging

from dashboard.models import Rental, Iha, Category

logger = logging.getLogger('dashboard')


def rentals_view(request):
    if request.user.is_anonymous:
        logger.critical('Rentals request from anonymous user!')
        return redirect('login')

    if request.method == 'POST':  # Rent IHA
        try:
            _rental = Rental()
            _body = json.loads(request.body)
            _rental.start_date = _body['startDate']
            _rental.end_date = _body['endDate']
            _user = User.objects.get(id=_body['userId'])
            _rental.user = _user
            _iha = Iha.objects.get(id=_body['ihaId'])
            _rental.iha = _iha
            _rental.save()
            logger.info("IHA '{}' rent to user '{}'".format(_iha.serial_number, _user.username))
        except Exception as e:
            logger.error("Failure to rent IHA. Error: '{}'".format(e))
            return HttpResponse('{}'.format(e), status=400)

        return HttpResponse('{}', status=200)

    else:  # List rentals
        if request.user.is_staff:
            _rentals = Rental.objects.all()
        else:
            _rentals = Rental.objects.filter(user=request.user)

        if not _rentals.exists():
            _rentals = []
        return render(request, 'rentals_list.html', {'rentals': _rentals})


def rental_view(request, id):
    if request.user.is_anonymous:
        logger.critical('Rental request from anonymous user!')
        return redirect('login')

    _rental = get_object_or_404(Rental, id=id)

    if request.method == 'DELETE' and request.user.is_staff:  # Delete rental. Usable for only admins.
        try:
            _rental.delete()
            logger.debug(f"Rental '{id}' deleted.")
            return HttpResponse('{}', status=200)
        except Exception as e:
            logger.error(f"Failure to delete rental '{id}'. Error: '{e}'")
            return HttpResponse('{}'.format(e), status=400)

    elif request.method == 'PUT' and (request.user.is_staff or _rental.user == request.user):
        # Update rental. Usable for admins and the user who rented the IHA.
        try:
            _body = json.loads(request.body)
            _rental = Rental.objects.get(id=id)
            _rental.start_date = _body['startDate']
            _rental.end_date = _body['endDate']
            _rental.save()
            logger.debug(f"Rental '{id}' updated.")
        except Exception as e:
            logger.error(f"Failure to update rental '{id}'. Error: '{e}'")
            return HttpResponse('{}'.format(e), status=400)

        return HttpResponse('{}', status=200)

    elif request.method == 'PATCH' and (request.user.is_staff or _rental.user == request.user):
        # Return rental. Usable for admins and the user who rented the IHA.
        try:
            _rental.is_returned = True
            _rental.save()
            logger.debug(f"Rental '{id}' returned.")
        except Exception as e:
            logger.error(f"Failure to return rental '{id}'. Error: '{e}'")
            return HttpResponse('{}'.format(e), status=400)

        return HttpResponse('{}', status=200)

    logger.critical('Unauthorized rental request!')
    return HttpResponse('Unauthorized', status=401)


def members_view(request):
    if request.user.is_anonymous:
        logger.critical('Members request from anonymous user!')
        return redirect('login')
    if not request.user.is_staff:
        logger.critical('Non-staff member request!')
        return HttpResponse('Unauthorized', status=401)

    _members = User.objects.all()
    if not _members.exists():
        _members = []
    return render(request, 'members_list.html', {'members': _members})


def member_view(request, id):
    if request.user.is_anonymous:
        logger.critical('Member request from anonymous user!')
        return redirect('login')
    if not request.user.is_staff:
        logger.critical('Non-staff member request!')
        return HttpResponse('Unauthorized', status=401)

    _user = get_object_or_404(User, id=id)
    if request.method == 'DELETE':  # Delete user
        try:
            _user.delete()
            logger.debug(f"User '{id}' deleted.")
            return HttpResponse('{}', status=200)
        except Exception as e:
            logger.error(f"Failure to delete user '{id}'. Error: '{e}'")
            return HttpResponse('{}'.format(e), status=400)

    logger.critical('Unauthorized member request!')
    return HttpResponse('Unauthorized', status=401)


def iha_categories_view(request):
    if request.user.is_anonymous:
        logger.critical('Categories request from anonymous user!')
        return redirect('login')
    if not request.user.is_staff:
        logger.critical('Non-staff member request!')
        return HttpResponse('Unauthorized', status=401)

    if request.method == 'POST':   # Add category.
        if not request.user.is_staff:
            logger.critical('Unauthorized category request!')
            return HttpResponse('Unauthorized', status=401)

        try:
            _body = json.loads(request.body)
            _category = Category()
            _category.name = _body['name']
            _category.added_date = timezone.now()
            _category.save()
            logger.info("Category '{}' added.".format(_category.name))
            return HttpResponse('{}', status=200)
        except Exception as e:
            logger.error("Failure to add category. Error: '{}'".format(e))
            return HttpResponse('{}'.format(e), status=400)

    else:  # List categories.
        _categories = Category.objects.all()
        if not _categories.exists():
            _categories = []
        return render(request, 'categories_list.html', {'categories': _categories})


def iha_category_view(request, id):
    if request.user.is_anonymous:
        logger.critical('Category request from anonymous user!')
        return redirect('login')

    if request.user.is_staff and request.method == 'PUT':  # Update category. Usable for only admins.
        try:
            _category = get_object_or_404(Category, id=id)
            _body = json.loads(request.body)
            _category.name = _body['name']
            _category.save()
            logger.info("Category '{}' updated.".format(_category.name))
        except Exception as e:
            logger.error("Failure to update category. Error: '{}'".format(e))
            return HttpResponse('{}'.format(e), status=400)

        return HttpResponse('{}', status=200)

    elif request.user.is_staff and request.method == 'DELETE':  # Delete category. Usable for only admins.
        try:
            _category = get_object_or_404(Category, id=id)
            _category.delete()
            logger.info("Category '{}' deleted.".format(_category.name))
        except Exception as e:
            logger.error("Failure to delete category. Error: '{}'".format(e))
            return HttpResponse('{}'.format(e), status=400)

        return HttpResponse('{}', status=200)

    logger.critical('Unauthorized category request!')
    return HttpResponse('Unauthorized', status=401)


def categorized_ihas_view(request, category):
    if request.user.is_anonymous:
        logger.critical('Categorized IHAs request from anonymous user!')
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
        logger.critical('IHAs request from anonymous user!')
        return redirect('login')

    if request.method == 'POST':  # Add IHA. Usage for only admins.
        if not request.user.is_staff:
            logger.critical('Unauthorized IHA request!')
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
            logger.info("IHA '{}' added.".format(_iha.serial_number))
        except Exception as e:
            logger.error("Failure to add IHA. Error: '{}'".format(e))
            return HttpResponse('{}'.format(e), status=400)

        return HttpResponse('{}', status=200)

    else:  # List IHAs.
        _ihas = Iha.objects.all()
        if not _ihas.exists():
            _ihas = []

        _categories = Category.objects.all()
        if not _categories.exists():
            _categories = []

        return render(request, 'ihas_list.html', {'ihas': _ihas, 'categories': _categories})


def iha_view(request, id):
    if request.user.is_anonymous:
        logger.critical('IHA request from anonymous user!')
        return redirect('login')

    _iha = get_object_or_404(Iha, id=id)

    if request.method == 'DELETE':  # Delete IHA. Usable for only admins.
        if not request.user.is_staff:
            logger.critical('Unauthorized IHA request!')
            return HttpResponse('Unauthorized', status=401)
        try:
            _iha.delete()
            logger.info("IHA '{}' deleted.".format(_iha.serial_number))
            return HttpResponse('{}', status=200)
        except Exception as e:
            logger.error("Failure to delete IHA. Error: '{}'".format(e))
            return HttpResponse('{}'.format(e), status=400)

    elif request.method == 'PUT':  # Update IHA. Usable for only admins.
        if not request.user.is_staff:
            logger.critical('Unauthorized IHA request!')
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
            logger.info("IHA '{}' updated.".format(_iha.serial_number))
        except Exception as e:
            logger.error("Failure to update IHA. Error: '{}'".format(e))
            return HttpResponse('{}'.format(e), status=400)

        return HttpResponse('{}', status=200)

    return redirect('ihas')
