

{
    'name': 'Firm Customize',
    'summary': 'Firm Customize',
    'author': "Add Value For Consulting",
    'company': 'Add Value For Consulting',
    'version': '1.0',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'sale',
        'crm',
        'stock',
        'project',
        'hr_expense',
        'sale_project',
        'mail',
        'industry_code',
    ],
    'data': [
        #'security/security.xml',
        'security/ir.model.access.csv',
        # 'report/',
        #'wizard/',
        'views/firm_contract.xml',
        'views/hr_expense.xml',
        'views/account_move.xml',
        'views/project.xml',
        'views/sale_order.xml',
        'views/crm_lead.xml',
        #'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
}

