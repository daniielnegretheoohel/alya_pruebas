{
    'name': 'Asistente de Desarrollo Personal',
    'version': '18.0',
    'summary': 'Módulo inteligente para seguimiento de metas y desarrollo personal',
    'author': 'Oohel Technologies S.A. de C.V.',
    'maintainer': 'Geovani  Nolasco N. <geovani.negrete@oohel.net>',
    'contributors': [
        'Geovani  Nolasco N. <geovani.negrete@oohel.net>',
    ],
    'category': 'Productivity/Personal Development',
    'description': """
        Módulo para la gestión y seguimiento de metas personales.
        Funcionalidades:
        - Seguimiento de progreso de metas
        - Recomendaciones inteligentes basadas en actividad
        - Registro de actividades realizadas
        - Integración con contactos (res.partner)
        - Reportes PDF personalizados
    """,
    'website': 'https://oohel.net',
    'depends': [
        'base',
        'mail',
        'contacts',
        'web',
    ],
    'data': [
        'security/alya_grupos_seguridad.xml',
        'security/ir.model.access.csv',
        'report/meta_personal_report.xml',
        'report/meta_personal_report_template.xml',
        'views/res_partner_views.xml',
        'views/alya_metas_personales_views.xml',
        'views/alya_recomendacion_inteligente_views.xml',
        'views/alya_seguimiento_actividades_views.xml',
        'views/alya_menu_principal.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
