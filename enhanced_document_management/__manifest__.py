# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2025-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Mruthul Raj(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{

    'name': 'Create Expense From Task',
    'summary': 'Create Expense From Task',
    'author': "Add Value For Consulting",
    'company': 'Add Value For Consulting',
    'version': '1.0',
    'license': 'AGPL-3',
    'depends': ['mail', 'website', 'hr'],
    'data': [
        'security/enhanced_document_management_groups.xml',
        'security/ir.model.access.csv',
        'data/document_data.xml',
        'data/ir_cron_data.xml',
        'views/document_tag_views.xml',
        'views/document_request_views.xml',
        'views/document_request_template_views.xml',
        'views/document_delete_trash_views.xml',
        'views/document_lock_views.xml',
        'views/document_workspace_views.xml',
        'views/document_file_views.xml',
        'views/document_portal_templates.xml',
        'views/document_request_wizard_view.xml',
        'views/outgoing_request_document_view.xml',
        'views/portal_document_templates.xml',
        'views/document_trash_views.xml',
        'views/document_request_portal_templates.xml',
        'views/document_request_portal_form.xml',
        'views/document_template_request_portal_templates.xml',
        'wizards/document_request_accept_view.xml',
        'wizards/document_request_reject_view.xml',
        'views/incoming_request_document_views.xml',
        'views/res_config_settings_views.xml',
        'views/enhanced_document_management_menu.xml',
        'reports/document_download.xml',
        'wizards/document_url_view.xml',
        'wizards/document_share_view.xml',
        'wizards/work_space_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'enhanced_document_management/static/src/css/kanban.css',
            'enhanced_document_management/static/src/css/style.css',
            'enhanced_document_management/static/src/xml/KanbanController.xml',
            'enhanced_document_management/static/src/xml/document_preview_template.xml',
            'enhanced_document_management/static/src/js/kanban_record.js',
            'enhanced_document_management/static/src/js/kanban_renderer.js',
            'enhanced_document_management/static/src/js/kanbancontroller.js',
            'enhanced_document_management/static/src/js/document_preview_action.js',
            'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js',
            'https://cdn.jsdelivr.net/npm/@fancyapps/fancybox@3.5.6/dist/jquery.fancybox.min.css',
            'https://cdn.jsdelivr.net/npm/@fancyapps/fancybox@3.5.6/dist/jquery.fancybox.min.js'
        ],
        'web.assets_frontend': [
        'enhanced_document_management/static/src/js/portal.js',
        ]
    },
    'external_dependencies': {
        'python': ['bs4']
    },
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
