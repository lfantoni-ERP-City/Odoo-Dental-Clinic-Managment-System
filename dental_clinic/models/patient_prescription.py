from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DentalPrescription(models.Model):
    _name = "dental.prescription"
    _description = "Prescripción odontológica"
    _rec_name = "prescription_serial"
    _order = "prescription_date desc, id desc"

    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, index=True)
    prescription_serial = fields.Char(string="Número", required=True, copy=False, readonly=True, index=True, default=lambda self: _("Nuevo"))
    prescription_date = fields.Date(string="Fecha", default=fields.Date.context_today, required=True)
    patient_id = fields.Many2one("dental.patient", string="Paciente", required=True, check_company=True, index=True)
    appointment_id = fields.Many2one("dental.appointment", string="Cita", ondelete="set null", check_company=True)
    line_ids = fields.One2many("dental.prescription.line", "prescription_id", string="Medicamentos")
    notes = fields.Text(string="Indicaciones")

    @api.onchange("appointment_id")
    def _onchange_appointment_id(self):
        if self.appointment_id:
            self.patient_id = self.appointment_id.patient_id

    @api.constrains("appointment_id", "patient_id", "company_id")
    def _check_appointment_patient(self):
        for prescription in self:
            if prescription.appointment_id and prescription.appointment_id.patient_id != prescription.patient_id:
                raise ValidationError(_("El paciente de la prescripción debe coincidir con el de la cita."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("prescription_serial", _("Nuevo")) == _("Nuevo"):
                vals["prescription_serial"] = self.env["ir.sequence"].next_by_code("dental.prescription") or _("Nuevo")
        return super().create(vals_list)


class DentalPrescriptionLine(models.Model):
    _name = "dental.prescription.line"
    _description = "Detalle de prescripción odontológica"

    prescription_id = fields.Many2one("dental.prescription", required=True, ondelete="cascade", index=True, check_company=True)
    company_id = fields.Many2one(related="prescription_id.company_id", store=True, index=True)
    medicine_trade_name = fields.Char(string="Medicamento", required=True)
    therapeutic_regimen = fields.Char(string="Posología", required=True)
