"""
@author: Geovani Daniel Nolasco Negrete <geovani.negrete@oohel.net>
@date: 05/12/2026
"""

from odoo import models, fields


class EtiquetaMetaPersonal(models.Model):
    """
    Modelo para definir etiquetas utilizadas en las metas personales.
    Cada etiqueta incluye un name y un color para clasificación visual
    """
    _name = "alya.etiqueta.meta.personal"
    _description = "Etiquetas para Metas Personales"

    name = fields.Char(
        string="Nombre",
        required=True,
    )
    color = fields.Integer(
        string="Color",
    )
