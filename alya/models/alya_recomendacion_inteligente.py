"""
@author: Geovani Daniel Nolasco Negrete <geovani.negrete@oohel.net>
@date: 05/12/2026
"""

from odoo import fields, models

TIPO_RECOMENDACION = [
    ("estrategia", "Estrategia"),
    ("recurso", "Recurso"),
    ("aprendizaje", "Aprendizaje"),
    ("motivacion", "Motivación"),
]

class recomendacion_Inteligente(models.Model):
    """
    Representa una recomendación generada (manual o automáticamente)
    asociada a una meta personal.
    """
    _name = "alya.recomendacion.inteligente"
    _description = "Recomendaciones Inteligentes para Metas"
    meta_id = fields.Many2one(
        comodel_name= "alya.meta.personal",
        string="Meta Relacionada",
        required=True,
        ondelete="cascade",
    )
    fecha = fields.Datetime(
        string="Fecha y Hora",
        default=fields.Datetime.now,
    )
    tipo_recomendacion = fields.Selection(
        selection=TIPO_RECOMENDACION,
        string="Tipo de Recomendación",
    )
    descripcion = fields.Text(
        string="Descripción",
    )
