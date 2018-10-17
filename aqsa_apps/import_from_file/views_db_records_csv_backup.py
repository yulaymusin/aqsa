# Author of Aqsa: Yulay Musin
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from . import models as m
from django.shortcuts import redirect
from . import viewxins_record_csv_backup as vxrcb
from . import forms as f
from aqsa_apps.wallet_tag_etc import models as wte_m
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy

import os
from django.conf import settings


success_msg = _('Data from your file was imported.')


@require_POST
@login_required
def db_records_csv_wallets(request, pk):
    import_from_file = get_object_or_404(m.ImportFromFile, owner=request.user, pk=pk, variety=2)

    if not import_from_file.checked:
        return redirect(import_from_file.get_check_url())

    if import_from_file.checked and import_from_file.no_error and not import_from_file.success:
        vxrcb.db_recorder_of_csv_of_wallet_tag_etc(import_from_file.file.path, request.user, f.Wallet, wte_m.Wallet)
        import_from_file.mark_as_finished()

    messages.success(request, success_msg)
    return redirect(reverse_lazy('import_from_file:list'))


@require_POST
@login_required
def db_records_csv_categories(request, pk):
    import_from_file = get_object_or_404(m.ImportFromFile, owner=request.user, pk=pk, variety=3)

    if not import_from_file.checked:
        return redirect(import_from_file.get_check_url())

    if import_from_file.checked and import_from_file.no_error and not import_from_file.success:
        vxrcb.db_recorder_of_csv_of_wallet_tag_etc(import_from_file.file.path, request.user, f.Category, wte_m.Category)
        import_from_file.mark_as_finished()

    messages.success(request, success_msg)
    return redirect(reverse_lazy('import_from_file:list'))


@require_POST
@login_required
def db_records_csv_tags(request, pk):
    import_from_file = get_object_or_404(m.ImportFromFile, owner=request.user, pk=pk, variety=4)

    if not import_from_file.checked:
        return redirect(import_from_file.get_check_url())

    if import_from_file.checked and import_from_file.no_error and not import_from_file.success:
        vxrcb.db_recorder_of_csv_of_wallet_tag_etc(import_from_file.file.path, request.user, f.Tag, wte_m.Tag)
        import_from_file.mark_as_finished()

    messages.success(request, success_msg)
    return redirect(reverse_lazy('import_from_file:list'))


@require_POST
@login_required
def db_records_csv_contacts(request, pk):
    import_from_file = get_object_or_404(m.ImportFromFile, owner=request.user, pk=pk, variety=5)

    if not import_from_file.checked:
        return redirect(import_from_file.get_check_url())

    if import_from_file.checked and import_from_file.no_error and not import_from_file.success:
        vxrcb.db_recorder_of_csv_of_wallet_tag_etc(import_from_file.file.path, request.user, f.Contact, wte_m.Contact)
        import_from_file.mark_as_finished()

    messages.success(request, success_msg)
    return redirect(reverse_lazy('import_from_file:list'))


@require_POST
@login_required
def db_records_csv_transactions(request, pk):
    import_from_file = get_object_or_404(m.ImportFromFile, owner=request.user, pk=pk, variety=6)

    if not import_from_file.checked:
        return redirect(import_from_file.get_check_url())

    if import_from_file.checked and import_from_file.no_error and not import_from_file.success:
        wallet_objects = wte_m.Wallet.objects.filter(owner=request.user)
        dict_with_wallets = dict((x.name, x) for x in wallet_objects)

        category_objects = wte_m.Category.objects.filter(owner=request.user)
        dict_with_categories = dict((x.name, x) for x in category_objects)

        tag_objects = wte_m.Tag.objects.filter(owner=request.user)
        dict_with_tags = dict((x.name, x) for x in tag_objects)

        contact_objects = wte_m.Contact.objects.filter(owner=request.user)
        dict_with_contacts = dict((x.name, x) for x in contact_objects)

        vxrcb.db_recorder_of_transaction(
            import_from_file.file.path, import_from_file, request.user,
            dict_with_wallets, dict_with_categories, dict_with_tags, dict_with_contacts
        )

        import_from_file.mark_as_finished()

    messages.success(request, success_msg)
    return redirect(reverse_lazy('import_from_file:list'))


@require_POST
@login_required
def db_records_aqsa_backup(request, pk):
    import_from_file = get_object_or_404(m.ImportFromFile, owner=request.user, pk=pk, variety=7)

    if not import_from_file.checked:
        return redirect(import_from_file.get_check_url())

    if import_from_file.checked and import_from_file.no_error and not import_from_file.success:
        unzipped_csv_path = os.path.join(settings.MEDIA_ROOT, os.path.join('import_from_file', pk))

        names_of_wallets_in_csv = vxrcb.db_recorder_of_csv_of_wallet_tag_etc(
            os.path.join(unzipped_csv_path, 'wallets.csv'), request.user, f.Wallet, wte_m.Wallet)
        names_of_categories_in_csv = vxrcb.db_recorder_of_csv_of_wallet_tag_etc(
            os.path.join(unzipped_csv_path, 'categories.csv'), request.user, f.Category, wte_m.Category)
        names_of_tags_in_csv = vxrcb.db_recorder_of_csv_of_wallet_tag_etc(
            os.path.join(unzipped_csv_path, 'tags.csv'), request.user, f.Tag, wte_m.Tag)
        names_of_contacts_in_csv = vxrcb.db_recorder_of_csv_of_wallet_tag_etc(
            os.path.join(unzipped_csv_path, 'contacts.csv'), request.user, f.Contact, wte_m.Contact)

        wallet_objects = wte_m.Wallet.objects.filter(owner=request.user, name__in=names_of_wallets_in_csv)
        dict_with_wallets = dict((x.name, x) for x in wallet_objects)

        category_objects = wte_m.Category.objects.filter(owner=request.user, name__in=names_of_categories_in_csv)
        dict_with_categories = dict((x.name, x) for x in category_objects)

        tag_objects = wte_m.Tag.objects.filter(owner=request.user, name__in=names_of_tags_in_csv)
        dict_with_tags = dict((x.name, x) for x in tag_objects)

        contact_objects = wte_m.Contact.objects.filter(owner=request.user, name__in=names_of_contacts_in_csv)
        dict_with_contacts = dict((x.name, x) for x in contact_objects)

        vxrcb.db_recorder_of_transaction(
            os.path.join(unzipped_csv_path, 'transactions.csv'), import_from_file, request.user,
            dict_with_wallets, dict_with_categories, dict_with_tags, dict_with_contacts
        )

        import_from_file.mark_as_finished()

    messages.success(request, success_msg)
    return redirect(reverse_lazy('import_from_file:list'))
