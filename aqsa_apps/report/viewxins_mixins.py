# Author of Aqsa: Yulay Musin
from aqsa_apps.wallet_tag_etc import models as wte_m
from aqsa_apps import sql_custom as sql
from . import models as m
from django.contrib.auth.mixins import LoginRequiredMixin
from aqsa_apps import mixins as mix
from django.utils.translation import gettext as _
from django.views.generic.edit import FormView
from django.views.generic import DetailView


def filter_for_sql_query_string(cd, q):
    # cd - form.cleaned_data, q - string for SQL query, which already have "SELECT ... WHERE ..."
    if cd.get('start_date'):
        q += ' AND "transaction"."date" >= \'' + cd.get('start_date').strftime("%Y-%m-%d") + '\'::date'
    if cd.get('finish_date'):
        q += ' AND "transaction"."date" <= \'' + cd.get('finish_date').strftime("%Y-%m-%d") + '\'::date'
    if len(cd.get('wallet')) == 1:
        q += ' AND "transaction"."wallet_id" = ' + str(cd.get('wallet')[0].id)
    elif len(cd.get('wallet')) >= 2:
        wallets = ['"transaction"."wallet_id" = ' + str(w.id) for w in cd.get('wallet')]
        wallets = ' OR '.join(wallets)
        q += ' AND (' + wallets + ')'
    if cd.get('contact'):
        q += ' AND "transaction"."contact_id" = ' + str(cd.get('contact').id)
    if cd.get('exclude_ignored'):
        q += ' AND "transaction"."not_ignore" IS TRUE'
    return q


def save_form(form, request_user, report_variety):
    form.instance.owner = request_user
    form.instance.variety = report_variety
    form.save()
    return form.instance.id


def make_report_balance_of_every_category(request_user, form, report_variety):
    categories_of_user = wte_m.Category.objects.filter(owner=request_user).values_list('id', flat=True)

    cd = form.cleaned_data

    # <Make a query string.
    query = []
    for category in categories_of_user:
        q = 'SELECT SUM("transaction"."value_in_curr") AS "balance" FROM "transaction" WHERE ' \
            '"transaction"."owner_id" = ' + str(request_user.id) + ' AND "transaction"."category_id" = ' \
            + str(category) + ' AND "transaction"."currency" = ' + str(cd.get('currency'))
        q = filter_for_sql_query_string(cd, q)
        query.append(q)
    else:
        # Else get SUM of transactions without (IS NULL) category.
        q = 'SELECT SUM("transaction"."value_in_curr") AS "balance" FROM "transaction" WHERE ' \
            '"transaction"."owner_id" = ' + str(request_user.id) + ' AND "transaction"."category_id" IS NULL' \
            + ' AND "transaction"."currency" = ' + str(cd.get('currency'))
        q = filter_for_sql_query_string(cd, q)
        query.append(q)

    query = ' UNION ALL '.join(query)
    query += ';'
    # </Make a query string.

    report_id = save_form(form, request_user, report_variety)

    # Example of "balance_by_category": [{'balance': None}, {'balance': Decimal('220.00')}]
    balance_of_every_category = sql.sql(query=query)

    new_report_data = []
    for key, category in enumerate(categories_of_user):
        new_report_data.append(m.ReportData(
            report_id=report_id,
            sum_of_values_in_curr=balance_of_every_category[key]['balance'],
            category_id=category,
        ))
    else:
        new_report_data.append(m.ReportData(
            report_id=report_id,
            sum_of_values_in_curr=balance_of_every_category[-1]['balance'],
            category_null=True,
        ))
        m.ReportData.objects.bulk_create(new_report_data)


def make_report_sum_of_income_or_sum_of_expense(request_user, form, report_variety, less_or_greater):
    cd = form.cleaned_data

    # <Making a query string.
    query = []

    q = 'SELECT SUM("transaction"."value") AS "sum" FROM "transaction" WHERE ' \
        '"transaction"."owner_id" = ' + str(request_user.id) + ' AND "transaction"."value" ' + less_or_greater + ' 0'
    q = filter_for_sql_query_string(cd, q)
    query.append(q)

    query = ' UNION ALL '.join(query)
    query += ';'
    # </Making a query string.

    report_id = save_form(form, request_user, report_variety)

    result_from_db = sql.sql(query=query)

    m.ReportData.objects.create(
        report_id=report_id,
        sum_of_values=result_from_db[0]['sum'],
    )


class ListReportMixin(LoginRequiredMixin, mix.OwnerRequired, mix.ListViewContextLabelsPaginated):
    variety = None
    model_labels_and_fields = ('date', 'start_date', 'finish_date', 'wallet', 'contact', 'exclude_ignored')

    template_name = 'common/list.html'
    model = m.Report

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('List of created reports'),
            'links': (self.model.links[self.variety-1]['create'],),
            'msg_empty_object_list': _('You do not have any report of selected variety. '
                                       'Click to "New Report" button for create it!'),
            'report': True,
        })
        return context

    def get_queryset(self):
        return super().get_queryset().filter(variety=self.variety).\
            select_related('contact').prefetch_related('wallet')


class CreateReportMixin(LoginRequiredMixin, mix.ContextForGenericView, mix.RequestUserInGetFormKwargs, FormView):
    template_name = 'common/form.html'

    variety = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('New Report'),
            'links': (m.Report.links[self.variety-1]['list'],),
            'submit_btn': _('Make and show the report!'),
            'datetimepicker': True,
            'description': _('When you create a report, you can specify parameters. Parameters is filters of your '
                             'transactions which should be calculated. For example, "Start Date" is filter which will '
                             'limit calculation result by range of your transactions, which was happens at the "Start '
                             'Date" or later. Transactions with the date, before "Start Date" will be not calculated.'),
        })
        return context

    def form_valid(self, form):
        if self.variety == 1:
            make_report_balance_of_every_category(self.request.user, form, self.variety)
        elif self.variety == 2:
            make_report_sum_of_income_or_sum_of_expense(self.request.user, form, self.variety, less_or_greater='>')
        elif self.variety == 3:
            make_report_sum_of_income_or_sum_of_expense(self.request.user, form, self.variety, less_or_greater='<')

        self.success_url = form.instance.get_read_url()
        return super().form_valid(form)


class ReadReportMixin(LoginRequiredMixin, mix.OwnerRequired, mix.ContextForGenericView,
                      mix.LabelsFieldsOfModelForGenericView, DetailView):

    template_name = 'report/read.html'
    model = m.Report

    model_labels_and_fields = ('date', 'start_date', 'finish_date', 'wallet', 'currency', 'contact', 'exclude_ignored')

    variety = None
    values = ()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report_data = self.object.data.all().values(*self.values)

        context.update({
            'title': m.Report.varieties[self.variety-1][1],
            'data': report_data,
            'links': (self.model.links[self.variety-1]['list'], self.model.links[self.variety-1]['create']),
        })
        return context

    def get_queryset(self):
        return super().get_queryset().filter(variety=self.variety)
