{
    'name': 'project_modified',
    'version': '1.0',
    'summary': 'project_modified summary',
    'description': 'A project based proqurement process',
    'category': 'project',
    'author': 'shofiqul',
    'depends': [
        'base',
        'project',
        'purchase'
    ],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'application': True,

    'data': [
        'security/ir.model.access.csv',

        'views/project_project_modified.xml',
        'views/purchase_order_inherited.xml'

    ]
}
