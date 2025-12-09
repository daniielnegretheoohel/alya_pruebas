"""
@author: Geovani Nolasco N. <geovani.negrete@oohel.net>
@date: 05/12/2026
"""

from odoo import api, fields, models


class ResPartner(models.Model):
    """
    Hereda de res.partner para añadir metas personales asociadas a un contacto.
    """
    _inherit = "res.partner"
    meta_ids = fields.One2many(
        comodel_name="alya.meta.personal",
        inverse_name="partner_id",
        string="Metas personales",
    )
    meta_count = fields.Integer(
        string="Cantidad de metas",
        compute="_compute_meta_count",
        readonly=True,
    )
    @api.depends("meta_ids")
    def _compute_meta_count(self):
        """Calcula la cantidad de metas asociadas al contacto."""
        for partner in self:
            partner.meta_count = len(partner.meta_ids)
