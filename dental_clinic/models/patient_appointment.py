from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DentalAppointment(models.Model):
    _name = "dental.appointment"
    _description = "Cita odontológica"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "appointment_serial"
    _order = "start desc, id desc"

    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, index=True)
    appointment_serial = fields.Char(string="Número de cita", required=True, copy=False, readonly=True, index=True, default=lambda self: _("Nuevo"))
    patient_id = fields.Many2one("dental.patient", string="Paciente", required=True, tracking=True, check_company=True)
    contact_number = fields.Char(related="patient_id.contact_number", string="Teléfono", readonly=True)
    state = fields.Selection(
        [("draft", "Borrador"), ("confirmed", "Confirmada"), ("in_exam", "En atención"), ("done", "Finalizada"), ("cancelled", "Cancelada")],
        string="Estado", default="draft", required=True, tracking=True,
    )
    appointment_type = fields.Selection(
        [("reserved", "Agendada"), ("walk_in", "Sin cita previa")], string="Tipo de cita", default="reserved", required=True, tracking=True,
    )
    doctor_id = fields.Many2one("dental.doctor", string="Odontólogo", required=True, tracking=True, check_company=True)
    assistant_id = fields.Many2one("res.users", string="Asistente", default=lambda self: self.env.user, check_company=True)
    start = fields.Datetime(string="Inicio", required=True, default=fields.Datetime.now, tracking=True, index=True)
    stop = fields.Datetime(string="Fin", required=True, default=lambda self: fields.Datetime.now() + timedelta(minutes=30), tracking=True)
    duration = fields.Float(string="Duración (horas)", compute="_compute_duration", store=True)
    chief_complaints = fields.Text(string="Motivo de consulta")
    procedure_line_ids = fields.One2many("dental.procedure.line", "appointment_id", string="Procedimientos")
    attachment_line_ids = fields.One2many("dental.attachment.line", "appointment_id", string="Adjuntos")
    prescription_ids = fields.One2many("dental.prescription", "appointment_id", string="Prescripciones")

    @api.depends("start", "stop")
    def _compute_duration(self):
        for appointment in self:
            appointment.duration = 0.0
            if appointment.start and appointment.stop:
                appointment.duration = max((appointment.stop - appointment.start).total_seconds() / 3600, 0.0)

    @api.constrains("start", "stop", "doctor_id", "state")
    def _check_schedule(self):
        for appointment in self:
            if appointment.start and appointment.stop and appointment.stop <= appointment.start:
                raise ValidationError(_("La hora de fin debe ser posterior a la hora de inicio."))
            if appointment.state != "cancelled" and appointment.doctor_id and appointment.start and appointment.stop:
                domain = [("id", "!=", appointment.id), ("company_id", "=", appointment.company_id.id), ("doctor_id", "=", appointment.doctor_id.id), ("state", "!=", "cancelled"), ("start", "<", appointment.stop), ("stop", ">", appointment.start)]
                if self.search_count(domain):
                    raise ValidationError(_("El odontólogo ya tiene una cita en ese horario."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("appointment_serial", _("Nuevo")) == _("Nuevo"):
                vals["appointment_serial"] = self.env["ir.sequence"].next_by_code("dental.appointment") or _("Nuevo")
        return super().create(vals_list)

    def action_confirm(self):
        self.filtered(lambda record: record.state == "draft").write({"state": "confirmed"})

    def action_start_exam(self):
        self.filtered(lambda record: record.state == "confirmed").write({"state": "in_exam"})

    def action_done(self):
        self.filtered(lambda record: record.state == "in_exam").write({"state": "done"})

    def action_cancel(self):
        self.filtered(lambda record: record.state not in ("done", "cancelled")).write({"state": "cancelled"})

    def action_reset_draft(self):
        self.filtered(lambda record: record.state == "cancelled").write({"state": "draft"})
