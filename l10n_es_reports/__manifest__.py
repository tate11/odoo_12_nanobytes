# Copyright 2018 Ionel Lazar <ilazar@nanobytes.es>

{
    "name": "Spanish - Accounting Nanobytes",
    "summary": "Accounting modifications for Spain by Nanobytes",
    "version": "12.0.1.0.0",
    "category": "Accounting & Finance",
    "website": "https://nanobytes.es",
    "author": "Nanobytes Informatica y Telecomunicaciones S.L.",
    "application": True,
    "installable": True,
    "depends": [
        "base",
        "account",
        "account_asset",
        "account_reports",
        "account_accountant",
        "l10n_es",
    ],
    "data": [
        "views/account_financial_report_views.xml",
        "views/tax_report_views.xml",
        "views/account_report_views.xml",
        "views/modelo_operaciones_report_view.xml",
        "wizard/aeat_tax_reports_wizards_views.xml",
        "data/account_tags_data.xml",
        "data/full_balance_sheet_report_data.xml",
        "data/assoc_balance_sheet_report_data.xml",
        "data/pymes_balance_sheet_report_data.xml",
        "data/mod111_data.xml",
        "data/mod115_data.xml",
        "data/mod303_data.xml",
        "data/mod390_data.xml",
        "data/mod200_data.xml",
        "data/profit_and_loss_data.xml",
    ],

    "demo": [
        "data/product_demo.xml",
        "data/invoice_customer_demo.xml",
        "data/invoice_supplier_demo.xml",
        "data/journal_entry_demo.xml",
    ],
}
