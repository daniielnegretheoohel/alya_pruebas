"""
@author: Geovani Daniel Nolasco Negrete <geovani.negrete@oohel.net>
@date: 05/12/2026
"""

from datetime import date
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

CATEGORIA_META = [
    ("profesional", "Desarrollo Profesional"),
    ("personal", "Desarrollo Personal"),
    ("financiero", "Metas Financieras"),
    ("salud", "Salud y Bienestar"),
    ("aprendizaje", "Aprendizaje"),
]
ESTADO_META = [
    ("borrador", "Borrador"),
    ("en_progreso", "En Progreso"),
    ("en_pausa", "En Pausa"),
    ("completado", "Completado"),
    ("no_logrado", "No Logrado"),
]
PRIORIDAD_META = [
    ("baja", "Baja"),
    ("media", "Media"),
    ("alta", "Alta"),
]

class MetaPersonal(models.Model):
    _name = "alya.meta.personal"
    _description = "Metas de Desarrollo Personal"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "prioridad desc, fecha_limite asc"

    name = fields.Char(
        string="Nombre de la Meta",
        required=True,
        tracking=True,
    )
    descripcion = fields.Text(
        string= "Descripcion",
        tracking=True,
    )
    category = fields.Selection(
        selection = categoria_meta,
        string="Categoria",
        required=True,
    )
    state = fields.Selection(
        selection = ESTADO_META,
        string="Estado",
        default="borrador",
        tracking=True,
    )
    prioridad = fields.Selection(
        selection = PRIORIDAD_META,
        string="Prioridad",
        default="media",
        tracking=True,
    )
    fecha_limite = fields.Date(
        string="Fecha limite",
        tracking=True,
    )
    etiqueta_ids = fields.Many2many(
        comodel_name="alya.etiqueta.meta.personal",
        string="Etiquetas",
    )
    recomendacion_ids = fields.One2many(
        comodel_name ="alya.recomendacion.inteligente",
        inverse_name="meta_id",
        string="Recomendaciones",
    )
    actividad_ids = fields.One2many(
        comodel_name="alya.seguimiento.actividad",
        inverse_name="meta_id",
        string="Actividades",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Contacto",
        help="Contacto asociado a esta meta.",
    )
    actividad_count = fields.Integer(
        string="Numero de Actividades",
        compute="_compute_actividad_count",
        store=True,
    )
    recomendacion_count = fields.Integer(
        string="Numero de Recomendaciones",
        compute="_compute_recomendacion_count",
        store=True,
    )
    dias_restantes = fields.Integer(
        string="Dios Restantes",
        compute="_compute_dias_restantes",
        store=True,
    )
    show_boton_completado = fields.Boolean(
        string="Mostrar boton completado",
        compute="_compute_show_boton_completado",
    )
    _sql_constraints = [
        (
            "unique_nombre_meta",
            "unique(name)",
            "Ya existe una meta con ese name.",
        )
    ]

    @api.model
    def default_get(self, fields_list):
        """Establece valores predeterminados al crear una meta personal.
        :return: Valores predeterminados.
        :rtype: dict
        """
        vals = super().default_get(fields_list)
        vals.setdefault("prioridad", "1")
        return vals

    @api.depends("state")
    def _compute_show_boton_completado(self):
        """Define si se debe mostrar el botón de completar la meta.
        :return:None
        :rtype:None
        """
        for meta in self:
            meta.show_boton_completado = meta.state != "completado"

    @api.depends("actividad_ids")
    def _compute_actividad_count(self):
        """Calcula el número de actividades asociadas a la meta.
        :return:None
        :rtype:None
        """
        for meta in self:
            meta.actividad_count = len(meta.actividad_ids)

    @api.depends("recomendacion_ids")
    def _compute_recomendacion_count(self):
        """Calcula el número de recomendaciones asociadas a la meta.
        :return:None
        :rtype:None
        """
        for meta in self:
            meta.recomendacion_count = len(meta.recomendacion_ids)

    @api.depends("fecha_limite")
    def _compute_dias_restantes(self):
        """Calcula la cantidad de días restantes hasta la fecha límite.
        :return:None
        :rtype:None
        """
        today = date.today()
        for meta in self:
            if meta.fecha_limite:
                meta.dias_restantes = (meta.fecha_limite - today).days
            else:
                meta.dias_restantes = 0

    @api.constrains("fecha_limite")
    def _check_fecha_limite(self):
        """Valida que la fecha límite no esté en el pasado.
        :return:None
        :rtype:None
        """
        today = fields.Date.today()
        for meta in self:
            if meta.fecha_limite and meta.fecha_limite < today:
                raise ValidationError(
                    "La fecha límite no puede ser en el pasado."
                )

    @api.constrains("state", "actividad_ids")
    def _check_actividades_para_completar(self):
        """Evita marcar metas como completadas sin actividades registradas.
        :return:None
        :rtype:None
        """
        for meta in self:
            if meta.state == "completado" and not meta.actividad_ids:
                raise ValidationError(
                    "No puedes marcar una meta como completada "
                    "sin registrar al menos una actividad."
                )

    def unlink(self):
        """Evita eliminar metas que ya han sido completadas.
        :return: Resultado de la eliminacion
        :rtype: bool
        """
        for meta in self:
            if meta.state == "completado":
                raise UserError("No puedes eliminar metas completadas.")
        return super(MetaPersonal, self).unlink()

    def action_avanzar(self):
        """Avanza la meta al siguiente state del flujo.
        :return: True si la operación se realizó.
        :rtype: bool
        """
        for meta in self:
            if meta.state == "borrador":
                meta.state = "en_progreso"
            elif meta.state == "en_progreso":
                meta.state = "en_pausa"
            elif meta.state == "en_pausa":
                meta.state = "completado"

    def action_retroceder(self):
        """Retrocede la meta al state anterior del flujo.
        :return: True si la operación se realizó.
        :rtype: bool
        """
        for meta in self:
            if meta.state == "completado":
                meta.state = "en_pausa"
            elif meta.state == "en_pausa":
                meta.state = "en_progreso"
            elif meta.state == "en_progreso":
                meta.state = "borrador"
            elif meta.state == "no_logrado":
                meta.state = "en_progreso"

    def action_marcar_completado(self):
        """Marca una meta como completada.
        :return: True si la operación se realizó.
        :rtype: bool
        """
        for meta in self:
            if meta.state != "completado":
                meta.state = "completado"

    def action_meta_personal_report(self):
        """Lanza el reporte PDF de meta personal.
        :return: Accion del reporte
        :rtype: dict
        """
        return self.env.ref("alya.action_report_meta_personal").report_action(
            self
        )

    def open_actividades(self):
        """Genera el reporte PDF correspondiente a la meta personal.
        :return: Acción de ventana con el dominio aplicado.
        :rtype: dict
        """
        return {
            "type": "ir.actions.act_window",
            "name": "Actividades",
            "res_model": "alya.seguimiento.actividad",
            "view_mode": "list,form",
            "domain": [("meta_id", "=", self.id)],
            "context": {"default_meta_id": self.id},
        }

    def open_recomendaciones(self):
        """Abre la vista de actividades relacionadas con la meta.
        :return: Acción de ventana con el dominio aplicado.
        :rtype: dict
        """
        action = self.env.ref("alya.action_alya_meta_recomendaciones").read()[0]
        action["domain"] = [("meta_id", "in", self.ids)]
        action["context"] = {"default_meta_id": self.id}

        return action