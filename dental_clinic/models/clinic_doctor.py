from odoo import fields, models


class DentalDoctor(models.Model):
    _name = "dental.doctor"
    _description = "Odontólogo"
    _rec_name = "name"
    _order = "name"

    active = fields.Boolean(default=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, index=True)
    name = fields.Char(string="Nombre", required=True)
    user_id = fields.Many2one("res.users", string="Usuario de Odoo", check_company=True)
    professional_registration = fields.Char(string="Registro profesional")
    phone = fields.Char(string="Teléfono")
    email = fields.Char()
    appointment_ids = fields.One2many("dental.appointment", "doctor_id", string="Citas")
