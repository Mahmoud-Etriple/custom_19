# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
{
    'name': 'Create Expense From Task',
    'summary': 'Create Expense From Task',
    'author': "Add Value For Consulting",
    'company': 'Add Value For Consulting',
    'version': '1.0',
    'license': 'AGPL-3',

    'depends': ['base', 'hr_expense', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_expense_views.xml',
        'views/project_task_views.xml',
        'wizards/expense_amount_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
