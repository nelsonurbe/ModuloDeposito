{
    'name': 'Gestión de Depósitos e Items',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Módulo para gestionar depósitos e items asignados a empleados',
    'description': 'Permite registrar depósitos, catalogar items y asignarlos a empleados.',
    'author': 'Nelson',
    'depends': ['base', 'hr', 'mail'],  # ✅ Incluye 'mail' para el chatter
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',  # ✅ Reglas de acceso
        'views/deposito_item.xml',       # ✅ Vistas de depósitos
        'views/deposito_menus.xml',
        'views/deposito_actions.xml',
],
    'application': True,  # ✅ Esto activa el ícono en el cajón de apps
    'installable': True,
    'license': 'LGPL-3',
}
