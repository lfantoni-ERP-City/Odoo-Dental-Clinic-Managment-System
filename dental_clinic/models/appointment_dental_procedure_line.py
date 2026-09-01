from odoo import fields, models


class DentalProcedureLine(models.Model):
    _name = "dental.procedure.line"
    _description = "Procedimiento odontológico"
    _order = "appointment_id, tooth_no, id"

    appointment_id = fields.Many2one("dental.appointment", required=True, ondelete="cascade", index=True, check_company=True)
    company_id = fields.Many2one(related="appointment_id.company_id", store=True, index=True)
    patient_id = fields.Many2one(related="appointment_id.patient_id", store=True, index=True)
    tooth_no = fields.Selection(
        [(str(number), str(number)) for number in (18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28, 38, 37, 36, 35, 34, 33, 32, 31, 41, 42, 43, 44, 45, 46, 47, 48)],
        string="Diente (FDI)", required=True,
    )
    service_item_id = fields.Many2one("product.product", string="Procedimiento", required=True, domain=[("sale_ok", "=", True)])
    currency_id = fields.Many2one(related="company_id.currency_id")
    cost = fields.Monetary(related="service_item_id.lst_price", string="Precio referencial", currency_field="currency_id", readonly=True)
