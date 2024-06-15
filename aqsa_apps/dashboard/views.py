# Author of Aqsa: Yulay Musin
from django.contrib.auth.decorators import login_required
from aqsa_apps.wallet_tag_etc import models as wte_m
from aqsa_apps import sql_custom as sql
from aqsa_apps.transaction import models as ta_m
from aqsa_apps.wallet_tag_etc import currencies
from django.shortcuts import render
from django.utils.translation import gettext as _


@login_required
def home(request):
    # <BALANCE OF EVERY WALLET.
    # <QuerySet [(5, 'My Another Bank Card'), (9, 'My Bank Card TRY'), (8, 'My Cash KRW')]>
    wallets_of_user = wte_m.Wallet.objects.filter(owner=request.user).values_list('id', 'name')

    # <Making a query string.
    query = []
    for wallet in wallets_of_user:
        q = 'SELECT SUM("transaction"."value") AS "balance" FROM "transaction" WHERE "transaction"."owner_id" = ' + \
            str(request.user.id) + ' AND "transaction"."wallet_id" = ' + str(int(wallet[0]))
        query.append(q)
    query = ' UNION ALL '.join(query)
    # </Making a query string.

    balance_of_every_wallet = []
    if query:
        query += ';'
        # [{'balance': None}, {'balance': Decimal('-4.00')}, {'balance': Decimal('3.00')}]
        balance_of_every_wallet = sql.sql(query=query)
        for key, totals in enumerate(balance_of_every_wallet):
            wallet_title = wallets_of_user[key][1]
            totals.update({'wallet': wallet_title})
    # </BALANCE OF EVERY WALLET.

    # <TOTALS BY WALLET.
    active_wallets_of_user = 'SELECT "wallet"."id", "wallet"."name" FROM "wallet" WHERE "wallet"."id" IN (SELECT ' \
                             'DISTINCT ON ("transaction"."wallet_id") "transaction"."wallet_id" FROM "transaction" ' \
                             'WHERE "transaction"."owner_id" = ' + str(request.user.id) + \
                             ' AND "transaction"."transfer" = false ORDER BY "transaction"."wallet_id" ASC)' \
                             ' AND "wallet"."owner_id" = ' + str(request.user.id) + ';'
    # [(9, 'My Bank Card TRY'), (8, 'My Cash KRW')]
    active_wallets_of_user = sql.sql(query=active_wallets_of_user, get_tuple=True)

    # <Making a query string.
    query = []
    for wallet in active_wallets_of_user:
        q_income = 'SELECT SUM("transaction"."value") AS "sum_of_income" FROM "transaction" WHERE ' \
                   '"transaction"."owner_id" = ' + str(request.user.id) + ' AND "transaction"."transfer" = false' \
                   ' AND "transaction"."not_ignore" = true AND "transaction"."wallet_id" = ' + str(int(wallet[0])) + \
                   ' AND "transaction"."value" > 0'
        q_expense = q_income.replace('AS "sum_of_income"', 'AS "sum_of_expense"').replace('"value" > 0', '"value" < 0')
        q = 'SELECT * FROM (' + q_income + ') as "sum_of_income" CROSS JOIN (' + q_expense + ') as "sum_of_expense"'
        query.append(q)
    query = ' UNION ALL '.join(query)
    # </Making a query string.

    totals_by_wallet = []
    if query:
        query += ';'
        # [{'sum_of_income': None, 'sum_of_expense': Decimal('-4.00')},
        # {'sum_of_income': Decimal('5.00'), 'sum_of_expense': Decimal('-2.00')}]
        totals_by_wallet = sql.sql(query=query)
        for key, totals in enumerate(totals_by_wallet):
            wallet_title = active_wallets_of_user[key][1]
            totals.update({'wallet': wallet_title})
    # </TOTALS BY WALLET.

    # <TOTALS BY CURRENCY.
    # <QuerySet [410, 840, 949]>
    active_currencies_of_user = ta_m.Transaction.objects.filter(owner=request.user, transfer=False, not_ignore=True)\
        .values_list('currency', flat=True).order_by('currency').distinct('currency')

    # <Making a query string.
    query = []
    for currency in active_currencies_of_user:
        q_income = 'SELECT SUM("transaction"."value_in_curr") AS "sum_of_income" FROM "transaction" WHERE ' \
                   '"transaction"."owner_id" = ' + str(request.user.id) + ' AND "transaction"."transfer" = false' \
                   ' AND "transaction"."not_ignore" = true AND "transaction"."currency" = ' + str(int(currency)) + \
                   ' AND "transaction"."value_in_curr" > 0'
        q_expense = q_income.replace('AS "sum_of_income"', 'AS "sum_of_expense"')\
            .replace('"value_in_curr" > 0', '"value_in_curr" < 0')
        q = 'SELECT * FROM (' + q_income + ') as "sum_of_income" CROSS JOIN (' + q_expense + ') as "sum_of_expense"'
        query.append(q)
    query = ' UNION ALL '.join(query)
    # </Making a query string.

    totals_by_currency = []
    if query:
        query += ';'
        # [{'sum_of_income': Decimal('5.00'), 'sum_of_expense': Decimal('-2.00')}, {'sum_of_income': None,
        # 'sum_of_expense': Decimal('-1.00')}, {'sum_of_income': None, 'sum_of_expense': Decimal('-1.00')}]
        totals_by_currency = sql.sql(query=query)
        for key, totals in enumerate(totals_by_currency):
            curr_title = currencies.get_currency_title(active_currencies_of_user[key])
            totals.update({'currency': curr_title})
    # <TOTALS BY CURRENCY.

    return render(request, 'dashboard/dashboard.html', {
        'title': _('Dashboard'),
        'totals_by_currency': totals_by_currency or None,
        'totals_by_wallet': totals_by_wallet or None,
        'balance_of_every_wallet': balance_of_every_wallet or None,
        'dashboard': True,
    })
