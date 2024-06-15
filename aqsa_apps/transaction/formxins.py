# Author of Aqsa: Yulay Musin
from django.utils.translation import gettext_lazy as _


# is_nnt - Is not NoneType?
def is_nnt(val):
    if isinstance(val, type(None)):
        return False
    return True


def is_num(val):
    try:
        float(val)
        return True
    except (ValueError, TypeError):
        return False


def add_errors_to_fields(add_error_func, fields, err_message):
    for field in fields:
        add_error_func(field, err_message)


# <ONLY FOR INCOME/EXPENSE
# If value and value_in_curr is different, but currency and currency of wallet is the same.
def value_and_value_in_curr_is_diff_but_curr_and_curr_of_wall_is_same(
        value, value_in_curr, wallet, currency,
        add_error_func, error_in_fields=('value_in_curr', 'currency'),
        err_msg=_('"Value" and "Value in currency" is different, '
                  'but selected currency and currency of selected wallet is the same. '
                  'Fill right "Value in currency" or leave empty that field, or select right "Currency".')
):
    if is_num(value) and is_num(value_in_curr) and is_nnt(wallet) \
            and value != value_in_curr \
            and wallet.currency == currency:
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# If user fill a value_in_curr (different from value), but forget to select a currency.
def user_fill_value_in_curr_but_diff_from_value_and_forget_to_select_currency(
        value, value_in_curr, currency,
        add_error_func, error_in_fields=('currency',),
        err_msg=_('If you fill "Value in currency" (different from the "Value"), then choose a currency.')
):
    if is_num(value) and is_num(value_in_curr) and not is_num(currency) \
            and value_in_curr != value:
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# If value and value_in_curr not both positive or both negative.
def value_and_value_in_curr_not_both_positive_or_both_negative(
        value, value_in_curr,
        add_error_func, error_in_fields=('value_in_curr', 'value'),
        err_msg=_('Value and Value in currency, both, '
                  'should be positive (your income) or negative (your expense).')
):
    if is_num(value_in_curr) and is_num(value) \
            and (value_in_curr > 0 > value
                 or value_in_curr < 0 < value):
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# If one of value (value or value_in_curr) is positive or negative, but another is 0.
def one_of_value_is_positive_or_negative_but_another_is_0(
        value, value_in_curr,
        add_error_func, error_in_fields=('value_in_curr', 'value'),
        err_msg=_('Value and Value in currency, both, should be positive (your income) or negative (your expense) '
                  'or both equal to 0.')
):
    if is_num(value_in_curr) and is_num(value) \
            and ((value_in_curr == 0 and value != 0) or
                 (value_in_curr != 0 and value == 0)):
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# If user select a currency (different from currency of wallet), but forget to fill a value_in_curr.
def user_select_curr_but_forget_to_fill_value_in_curr(
        value_in_curr, currency, wallet,
        add_error_func, error_in_fields=('value_in_curr',),
        err_msg=_('If currency of your transaction and currency of selected wallet is different, '
                  'then provide a value in selected currency.')
):
    if not is_num(value_in_curr) and is_num(currency) \
            and is_nnt(wallet) \
            and currency != wallet.currency:
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# Auto fill. If currency of selected wallet and currency is the same.
def auto_fill_value_in_curr_by_value_if_currency_of_wallet_and_currency_is_same(
        value, value_in_curr, wallet, currency
):
    if is_num(value) and is_nnt(wallet) \
            and not is_num(value_in_curr) \
            and (not is_num(currency)
                 or currency == wallet.currency):
        return value
    return value_in_curr


# Auto fill. If user did not choose any currency, use currency of selected wallet.
def auto_fill_curr_by_curr_of_wallet_if_user_did_not_choose_curr(wallet, currency):
    if is_nnt(wallet) and not is_num(currency):
        return wallet.currency
    return currency


# Call all of above which is for income/expense
def clean_for_income_expense_form(cd, add_error, with_auto_fill=True):
    # If value and value_in_curr is different, but currency and currency of wallet is the same.
    value_and_value_in_curr_is_diff_but_curr_and_curr_of_wall_is_same(
        cd.get('value'), cd.get('value_in_curr'), cd.get('wallet'), cd.get('currency'), add_error)

    # If user fill a value_in_curr (different from value), but forget to select a currency.
    user_fill_value_in_curr_but_diff_from_value_and_forget_to_select_currency(
        cd.get('value'), cd.get('value_in_curr'), cd.get('currency'), add_error)

    # If value and value_in_curr not both positive or both negative.
    value_and_value_in_curr_not_both_positive_or_both_negative(
        cd.get('value'), cd.get('value_in_curr'), add_error)

    # If one of value (value or value_in_curr) is positive or negative, but another is 0.
    one_of_value_is_positive_or_negative_but_another_is_0(
        cd.get('value'), cd.get('value_in_curr'), add_error)

    # If user select a currency (different from currency of wallet), but forget to fill a value_in_curr.
    user_select_curr_but_forget_to_fill_value_in_curr(
        cd.get('value_in_curr'), cd.get('currency'), cd.get('wallet'), add_error)

    if with_auto_fill:
        # Auto fill. If currency of selected wallet and currency is the same.
        cd['value_in_curr'] = auto_fill_value_in_curr_by_value_if_currency_of_wallet_and_currency_is_same(
            cd.get('value'), cd.get('value_in_curr'), cd.get('wallet'), cd.get('currency'))

        # Auto fill. If user did not choose any currency, use currency of selected wallet.
        cd['currency'] = auto_fill_curr_by_curr_of_wallet_if_user_did_not_choose_curr(
            cd.get('wallet'), cd.get('currency'))

    return cd
# </ONLY FOR INCOME/EXPENSE


# <ONLY FOR TRANSFER TRANSACTIONS
# If wallets in different currencies, but user did not fill "value2"
def if_wallets_in_different_currency_but_user_did_not_fill_value2(
        value2, wallet1, wallet2,
        add_error_func, error_in_fields=('value2',),
        err_msg=_('Required if wallets in different currencies. '
                  'How much money spend (goes from) the sending wallet? Fill a negative value.')
):
    if not is_num(value2) and is_nnt(wallet1) and is_nnt(wallet2) \
            and wallet1.currency != wallet2.currency:
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# If wallets in different currency, but user did not fill "Currency"
def if_wallets_in_different_currency_but_user_did_not_fill_currency(
        wallet1, wallet2, currency,
        add_error_func, error_in_fields=('currency',),
        err_msg=_('Required if wallets in different currencies. Select "Currency".')
):
    if is_nnt(wallet1) and is_nnt(wallet2) and not is_num(currency) \
            and wallet1.currency != wallet2.currency:
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# If wallets in different currency, but user did not fill "Value in currency"
def if_wallets_in_different_currency_but_user_did_not_fill_value_in_currency(
    wallet1, wallet2, value_in_curr,
    add_error_func, error_in_fields=('value_in_curr',),
    err_msg=_('Required if wallets in different currencies. Fill "Value in currency".')
):
    if is_nnt(wallet1) and is_nnt(wallet2) and not is_num(value_in_curr) \
            and wallet1.currency != wallet2.currency:
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# If value1 <= 0
def value1_less_or_equal_0(
        value1,
        add_error_func, error_in_fields=('value_in_curr',),
        err_msg=_('#1 - should be positive value (bigger than 0).')
):
    if is_num(value1) and value1 <= 0:
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# If value2 >= 0
def value2_bigger_or_equal_0(
        value2,
        add_error_func, error_in_fields=('value2',),
        err_msg=_('#2 - should be negative value (less than 0).')
):
    if is_num(value2) and value2 >= 0:
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# If value_in_curr <= 0
def value_in_curr_less_or_equal_0(
        value_in_curr,
        add_error_func, error_in_fields=('value_in_curr',),
        err_msg=_('Should be positive (bigger than 0).')
):
    if is_num(value_in_curr) and value_in_curr <= 0:
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# If user transfer from and to the same wallet
def user_transfer_from_and_to_the_same_wallet(
        wallet1, wallet2,
        add_error_func, error_in_fields=('wallet1', 'wallet2'),
        err_msg=_('Do not transfer from and to the same wallet.')
):
    if wallet1 and wallet2 \
            and wallet1 == wallet2:
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# If sum of values (value1 and value2) not equal to 0, but wallets in the same currency
def sum_of_values_not_equal_to_0_but_wallets_in_the_same_currency(
        value1, value2, wallet1, wallet2,
        add_error_func, error_in_fields=('value1', 'value2'),
        err_msg=_('When you transfer money between wallets in the same currency, sum of "Value #1" and "Value #2" '
                  'should be equal to 0 ("Value #2" should be same with "Value #1", except that "Value #1" is positive '
                  'and "Value #2" is negative). If you have a bank commission for transfer money, '
                  'then make a "New Income or Expense" transaction for record that.')
):
    if is_nnt(wallet1) and is_nnt(wallet2) \
            and is_num(value1) and is_num(value2) \
            and wallet1.currency == wallet2.currency \
            and value1 + value2 != 0:
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# If value1 and value_in_curr is different, but wallets in the same currency
def wallets_in_the_same_currency_but_value1_and_value_in_curr_not_same(
        value1, wallet1, wallet2, value_in_curr,
        add_error_func, error_in_fields=('value_in_curr',),
        err_msg=_('When you transfer money between wallets in the same currency, "Value #1" and "Value in currency" '
                  'should be the same. If you have a bank commission for transfer money, '
                  'then make a "New Income or Expense" transaction for record that.')
):
    if is_nnt(wallet1) and is_nnt(wallet2) \
            and is_num(value1) and is_num(value_in_curr) \
            and wallet1.currency == wallet2.currency \
            and value1 != value_in_curr:
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# If user select currency (different from currency of wallets)
def user_select_different_currency_while_wallets_in_the_same_currency(
        wallet1, wallet2, currency,
        add_error_func, error_in_fields=('currency',),
        err_msg=_('When you transfer money between wallets in the same currency, "Currency" should be the same.')
):
    if is_nnt(wallet1) and is_nnt(wallet2) \
            and wallet1.currency == wallet2.currency \
            and is_num(currency) and wallet1.currency != int(currency):
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# If value1 != value_in_curr, but currency of wallet1 same with selected currency
def if_value1_not_equal_to_value_in_curr_but_currency_of_wallet1_same_with_currency(
        value1, wallet1, currency, value_in_curr,
        add_error_func, error_in_fields=('value1', 'value_in_curr'),
        err_msg=_('"Value #1" not equal to "Value in currency" even currency of "Wallet #1" same with '
                  'selected "Currency". If you have a bank commission for transfer money, '
                  'then make a "New Income or Expense" transaction for record that.')
):
    if is_num(value1) and is_nnt(wallet1) and is_num(value_in_curr) \
            and value1 != value_in_curr \
            and is_num(currency) and wallet1.currency == int(currency):
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# If value2 + value_in_curr != 0, but currency of wallet2 same with selected currency
def if_sum_of_value2_and_value_in_curr_not_equal_to_0_but_curr_of_wallet1_same_with_currency(
        value2, wallet2, currency, value_in_curr,
        add_error_func, error_in_fields=('value2', 'value_in_curr'),
        err_msg=_('Sum of "Value #2" and "Value in currency" not equal to 0 even currency of "Wallet #2" same with '
                  'selected "Currency". If you have a bank commission for transfer money, '
                  'then make a "New Income or Expense" transaction for record that.')
):
    if is_num(value2) and is_nnt(wallet2) and is_num(value_in_curr) \
            and value2 + value_in_curr != 0 \
            and is_num(currency) and wallet2.currency == int(currency):
        add_errors_to_fields(add_error_func, error_in_fields, err_msg)


# Auto fill. If user did not fill value2 and selected wallets in the same currency, use value1 * -1.
def auto_fill_value2_by_negative_value1_if_user_did_not_fill_value2_and_wallets_in_same_curr(
        value1, value2, wallet1, wallet2, currency, value_in_curr
):
    if is_num(value1) and is_nnt(wallet1) and is_nnt(wallet2) \
            and not value2 \
            and wallet1.currency == wallet2.currency \
            and ((is_num(currency) and wallet1.currency == int(currency)) or not is_num(currency)) \
            and ((is_num(value_in_curr) and value_in_curr == value1) or not is_num(value_in_curr)):
        return value1 * -1
    return value2


# Auto fill. If user did not fill currency and selected wallets in the same currency, use currency of wallet1.
def auto_fill_currency_by_curr_of_wallet1_if_user_did_not_fill_curr_and_wallets_in_same_curr(
        value1, value2, wallet1, wallet2, currency, value_in_curr
):
    if is_num(value1) and is_nnt(wallet1) and is_nnt(wallet2) \
            and not currency \
            and wallet1.currency == wallet2.currency \
            and ((is_num(value2) and value1 + value2 == 0) or not is_num(value2)) \
            and ((is_num(value_in_curr) and value1 == value_in_curr) or not is_num(value_in_curr)):
        return wallet1.currency
    return currency


# Auto fill. If user did not fill value_in_curr and selected wallets in the same currency, use value1.
def auto_fill_value_in_curr_by_value1_if_wallets_in_same_curr(
        value1, value2, wallet1, wallet2, currency, value_in_curr
):
    if is_num(value1) and is_nnt(wallet1) and is_nnt(wallet2) \
            and not is_num(value_in_curr) \
            and wallet1.currency == wallet2.currency \
            and ((is_num(currency) and wallet1.currency == int(currency)) or not is_num(currency)) \
            and ((is_num(value2) and value1 + value2 == 0) or not is_num(value2)):
        return value1
    return value_in_curr


# Call all of above which is for transfer transactions
def clean_for_pair_transfer_form(cd, add_error, with_auto_fill=True):
    # If wallets in different currencies, but user did not fill "value2"
    if_wallets_in_different_currency_but_user_did_not_fill_value2(
        cd.get('value2'), cd.get('wallet1'), cd.get('wallet2'), add_error)

    # If wallets in different currency, but user did not fill "Currency"
    if_wallets_in_different_currency_but_user_did_not_fill_currency(
        cd.get('wallet1'), cd.get('wallet2'), cd.get('currency'), add_error)

    # If wallets in different currency, but user did not fill "Value in currency"
    if_wallets_in_different_currency_but_user_did_not_fill_value_in_currency(
        cd.get('wallet1'), cd.get('wallet2'), cd.get('value_in_curr'), add_error)

    # If value1 <= 0
    value1_less_or_equal_0(cd.get('value1'), add_error)

    # If value2 >= 0
    value2_bigger_or_equal_0(cd.get('value2'), add_error)

    # If value_in_curr <= 0
    value_in_curr_less_or_equal_0(cd.get('value_in_curr'), add_error)

    # If user transfer from and to the same wallet
    user_transfer_from_and_to_the_same_wallet(cd.get('wallet1'), cd.get('wallet2'), add_error)

    # If sum of values (value1 and value2) not equal to 0, but wallets in the same currency
    sum_of_values_not_equal_to_0_but_wallets_in_the_same_currency(
        cd.get('value1'), cd.get('value2'), cd.get('wallet1'), cd.get('wallet2'), add_error)

    # If value1 and value_in_curr is different, but wallets in the same currency
    wallets_in_the_same_currency_but_value1_and_value_in_curr_not_same(
        cd.get('value1'), cd.get('wallet1'), cd.get('wallet2'), cd.get('value_in_curr'), add_error)

    # If wallets in the same currency, but user select different currency
    user_select_different_currency_while_wallets_in_the_same_currency(
        cd.get('wallet1'), cd.get('wallet2'), cd.get('currency'), add_error)

    # If value1 != value_in_curr, but currency of wallet1 same with selected currency
    if_value1_not_equal_to_value_in_curr_but_currency_of_wallet1_same_with_currency(
        cd.get('value1'), cd.get('wallet1'), cd.get('currency'), cd.get('value_in_curr'), add_error)

    # If value2 + value_in_curr != 0, but currency of wallet2 same with selected currency
    if_sum_of_value2_and_value_in_curr_not_equal_to_0_but_curr_of_wallet1_same_with_currency(
        cd.get('value2'), cd.get('wallet2'), cd.get('currency'), cd.get('value_in_curr'), add_error)

    if with_auto_fill:
        # Auto fill. If user did not fill value2 and selected wallets in the same currency, use value1 * -1.
        cd['value2'] = auto_fill_value2_by_negative_value1_if_user_did_not_fill_value2_and_wallets_in_same_curr(
            cd.get('value1'), cd.get('value2'), cd.get('wallet1'), cd.get('wallet2'),
            cd.get('currency'), cd.get('value_in_curr'))

        # Auto fill. If user did not fill currency and selected wallets in the same currency, use currency of wallet1.
        cd['currency'] = auto_fill_currency_by_curr_of_wallet1_if_user_did_not_fill_curr_and_wallets_in_same_curr(
            cd.get('value1'), cd.get('value2'), cd.get('wallet1'), cd.get('wallet2'),
            cd.get('currency'), cd.get('value_in_curr'))

        # Auto fill. If user did not fill value_in_curr and selected wallets in the same currencies, use value1.
        cd['value_in_curr'] = auto_fill_value_in_curr_by_value1_if_wallets_in_same_curr(
            cd.get('value1'), cd.get('value2'), cd.get('wallet1'), cd.get('wallet2'),
            cd.get('currency'), cd.get('value_in_curr'))

    return cd
# </ONLY FOR TRANSFER TRANSACTIONS
