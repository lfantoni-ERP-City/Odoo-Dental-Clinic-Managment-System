from odoo import fields, models


class DentalAttachmentLine(models.Model):
    _name = "dental.attachment.line"
    _description = "Adjunto de cita odontológica"

    appointment_id = fields.Many2one("dental.appointment", required=True, ondelete="cascade", index=True, check_company=True)
    company_id = fields.Many2one(related="appointment_id.company_id", store=True, index=True)
    attachment_date = fields.Date(string="Fecha", default=fields.Date.context_today, required=True)
    name = fields.Char(string="Nombre", required=True)
    file = fields.Binary(string="Archivo", required=True, attachment=True)
    file_name = fields.Char(string="Nombre del archivo")
