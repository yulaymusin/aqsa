# Author of Aqsa: Yulay Musin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from . import models as m
from . import viewxins_check_csv_backup as vxccb
from . import forms as f
from django.shortcuts import render
from django.utils.translation import gettext as _
import os
from django.conf import settings
from aqsa_apps.wallet_tag_etc import models as wte_m


@login_required
def check_csv_wallets(request, pk):
    import_from_file = get_object_or_404(m.ImportFromFile, owner=request.user, pk=pk, variety=2)

    if not import_from_file.checked or import_from_file.no_error is None:
        no_error, ___, ___ = vxccb.csv_checker_of_wallet_tag_etc(import_from_file.file.path, f.Wallet)

        import_from_file.mark_as_checked(no_error)

    return render(request=request, template_name='import_from_file/check_file_show_error_or_ok.html', context={
        'title': _('CSV with wallets have been checked'),
        'import_from_file': import_from_file,
        'submit_btn': _('Confirm to import wallets'),
        'links': (m.ImportFromFile.links['list'],),
    })


@login_required
def check_csv_categories(request, pk):
    import_from_file = get_object_or_404(m.ImportFromFile, owner=request.user, pk=pk, variety=3)

    if not import_from_file.checked or import_from_file.no_error is None:
        no_error, ___, ___ = vxccb.csv_checker_of_wallet_tag_etc(import_from_file.file.path, f.Category)

        import_from_file.mark_as_checked(no_error)

    return render(request=request, template_name='import_from_file/check_file_show_error_or_ok.html', context={
        'title': _('CSV with categories have been checked'),
        'import_from_file': import_from_file,
        'submit_btn': _('Confirm to import categories'),
        'links': (m.ImportFromFile.links['list'],),
    })


@login_required
def check_csv_tags(request, pk):
    import_from_file = get_object_or_404(m.ImportFromFile, owner=request.user, pk=pk, variety=4)

    if not import_from_file.checked or import_from_file.no_error is None:
        no_error, ___, ___ = vxccb.csv_checker_of_wallet_tag_etc(import_from_file.file.path, f.Tag)

        import_from_file.mark_as_checked(no_error)

    return render(request=request, template_name='import_from_file/check_file_show_error_or_ok.html', context={
        'title': _('CSV with tags have been checked'),
        'import_from_file': import_from_file,
        'submit_btn': _('Confirm to import tags'),
        'links': (m.ImportFromFile.links['list'],),
    })


@login_required
def check_csv_contacts(request, pk):
    import_from_file = get_object_or_404(m.ImportFromFile, owner=request.user, pk=pk, variety=5)

    if not import_from_file.checked or import_from_file.no_error is None:
        no_error, ___, ___ = vxccb.csv_checker_of_wallet_tag_etc(import_from_file.file.path, f.Contact)

        import_from_file.mark_as_checked(no_error)

    return render(request=request, template_name='import_from_file/check_file_show_error_or_ok.html', context={
        'title': _('CSV with contacts have been checked'),
        'import_from_file': import_from_file,
        'submit_btn': _('Confirm to import contacts'),
        'links': (m.ImportFromFile.links['list'],),
    })


@login_required
def check_csv_transactions(request, pk):
    import_from_file = get_object_or_404(m.ImportFromFile, owner=request.user, pk=pk, variety=6)

    if not import_from_file.checked or import_from_file.no_error is None:
        wallets = wte_m.Wallet.objects.filter(owner=request.user).values_list('name', 'currency')
        names_and_currencies_of_wallets = dict((x, y) for x, y in wallets)
        names_of_categories = wte_m.Category.objects.filter(owner=request.user).values_list('name', flat=True)
        names_of_tags = wte_m.Tag.objects.filter(owner=request.user).values_list('name', flat=True)
        names_of_contacts = wte_m.Contact.objects.filter(owner=request.user).values_list('name', flat=True)

        no_error = vxccb.csv_checker_of_transaction(
            import_from_file.file.path,
            names_and_currencies_of_wallets, names_of_categories, names_of_tags, names_of_contacts
        )

        import_from_file.mark_as_checked(no_error)

    return render(request=request, template_name='import_from_file/check_file_show_error_or_ok.html', context={
        'title': _('CSV with transactions have been checked'),
        'import_from_file': import_from_file,
        'submit_btn': _('Confirm to import transactions'),
        'links': (m.ImportFromFile.links['list'],),
    })


@login_required
def check_aqsa_backup(request, pk):
    import_from_file = get_object_or_404(m.ImportFromFile, owner=request.user, pk=pk, variety=7)

    if not import_from_file.checked or import_from_file.no_error is None:
        unzipped_csv_path = os.path.join(settings.MEDIA_ROOT, os.path.join('import_from_file', pk))

        no_error, ___, names_and_currencies_of_wallets = vxccb.csv_checker_of_wallet_tag_etc(
            os.path.join(unzipped_csv_path, 'wallets.csv'), f.Wallet
        )
        if no_error:
            no_error, names_of_categories, ___ = vxccb.csv_checker_of_wallet_tag_etc(
                os.path.join(unzipped_csv_path, 'categories.csv'), f.Category
            )
        if no_error:
            no_error, names_of_tags, ___ = vxccb.csv_checker_of_wallet_tag_etc(
                os.path.join(unzipped_csv_path, 'tags.csv'), f.Tag
            )
        if no_error:
            no_error, names_of_contacts, ___ = vxccb.csv_checker_of_wallet_tag_etc(
                os.path.join(unzipped_csv_path, 'contacts.csv'), f.Contact
            )
        if no_error:
            # Here we will not do DB queries and check what kind of "wallet_tag_etc" user have. We will think uploaded
            # ZIP was made by "export_to_file" app and CSV-files of "wallet_tag_etc" of ZIP have everything what needs.
            no_error = vxccb.csv_checker_of_transaction(
                os.path.join(unzipped_csv_path, 'transactions.csv'),
                names_and_currencies_of_wallets, names_of_categories, names_of_tags, names_of_contacts
            )

        import_from_file.mark_as_checked(no_error)

    return render(request=request, template_name='import_from_file/check_file_show_error_or_ok.html', context={
        'title': _('Aqsa-Backup have been checked'),
        'import_from_file': import_from_file,
        'submit_btn': _('Confirm to import data from Aqsa-Backup'),
        'links': (m.ImportFromFile.links['list'],),
    })
