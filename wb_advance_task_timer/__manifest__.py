{
    'name': 'Task Timer',
    'summary': 'Task Timer',
    'author': "Add Value For Consulting",
    'company': 'Add Value For Consulting',
    'version': '1.0',
    'license': 'AGPL-3',
    'description': 'Advanced task time tracking with popup-based timer and real-time visibility.',
    'depends': [
        'web',
        'project',
        'hr_timesheet',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/kanban_view_task.xml',
        'wizard/timer_wizard_view.xml',
        'wizard/end_timer_wizard_view.xml',
    ],
    # 'post_init_hook': 'post_init_hook',
    'assets': {
        'web.assets_backend': [
            'wb_advance_task_timer/static/src/xml/timer_button_popup.xml',
            'wb_advance_task_timer/static/src/js/timer_button_popup.js',
            'wb_advance_task_timer/static/src/js/kanban_view.js',
        ],
    },
    'images': [
        'static/description/Task Timer - 19.png',   # App Store banner
        'static/description/icon.png',     # App icon
    ],
}
