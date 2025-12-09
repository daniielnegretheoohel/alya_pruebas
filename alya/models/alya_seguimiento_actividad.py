"""
@author: Geovani Nolasco N. <geovani.negrete@oohel.net>
@date: 05/12/2026
"""

from odoo import fields, models


TIPO_ACTIVIDAD = [
    ("actualizacion_progreso", "Actualización de Progreso"),
    ("aprendizaje", "Actividad de Aprendizaje"),
    ("hito", "Hito Alcanzado"),
    ("desafio", "Desafío Encontrado"),
]


class Seguimiento_Actividad(models.Model):
    """
    Representa una actividad registrada durante el seguimiento
    del avance de una meta personal.
    """
    _name = "alya.seguimiento.actividad"
    _description = "Seguimiento de Actividades para Logro de Metas"

    meta_id = fields.Many2one(
        comodel_name="alya.meta.personal",
        string="Meta Relacionada",
        required=True,
    )
    fecha = fields.Datetime(
        string="Fecha y Hora",
        default=fields.Datetime.now,
    )
    tipo_actividad = fields.Selection(
        selection=TIPO_ACTIVIDAD,
        string="Tipo de Actividad",
    )
    descripcion = fields.Text(
        string="Descripción",
    )
