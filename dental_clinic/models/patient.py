from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DentalPatient(models.Model):
    _name = "dental.patient"
    _description = "Paciente odontológico"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "patient_name"
    _order = "patient_name, id"

    active = fields.Boolean(default=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, index=True)
    patient_serial = fields.Char(string="Historia clínica", required=True, copy=False, readonly=True, index=True, default=lambda self: _("Nuevo"))
    patient_name = fields.Char(string="Nombre completo", required=True, tracking=True, index=True)
    identification_type = fields.Selection(
        [("cedula", "Cédula"), ("ruc", "RUC"), ("passport", "Pasaporte"), ("other", "Otro")],
        string="Tipo de identificación", default="cedula", required=True,
    )
    identification = fields.Char(string="Número de identificación", required=True, index=True)
    email = fields.Char()
    contact_number = fields.Char(string="Teléfono", tracking=True)
    date_of_birth = fields.Date(string="Fecha de nacimiento")
    age = fields.Integer(string="Edad", compute="_compute_age", store=True)
    gender = fields.Selection(
        [("male", "Masculino"), ("female", "Femenino"), ("other", "Otro"), ("not_specified", "No especificado")], string="Género",
    )
    occupation = fields.Char(string="Ocupación")
    marital_status = fields.Selection(
        [("single", "Soltero/a"), ("married", "Casado/a"), ("divorced", "Divorciado/a"), ("widowed", "Viudo/a")], string="Estado civil",
    )
    blood_type = fields.Selection(
        [("a-", "A-"), ("a+", "A+"), ("b-", "B-"), ("b+", "B+"), ("ab-", "AB-"), ("ab+", "AB+"), ("o-", "O-"), ("o+", "O+")], string="Tipo sanguíneo",
    )
    anticoagulants = fields.Boolean(string="Usa anticoagulantes")
    anticoagulants_notes = fields.Char(string="Detalle de anticoagulantes")
    immunological_diseases = fields.Boolean(string="Enfermedades inmunológicas")
    immunological_diseases_notes = fields.Char(string="Detalle de enfermedades")
    medical_alerts = fields.Text(string="Alertas médicas")
    appointment_ids = fields.One2many("dental.appointment", "patient_id", string="Citas")
    prescription_ids = fields.One2many("dental.prescription", "patient_id", string="Prescripciones")

    _sql_constraints = [
        ("dental_patient_identification_company_uniq", "unique(company_id, identification)", "Ya existe un paciente con esta identificación en la compañía."),
    ]

    @api.depends("date_of_birth")
    def _compute_age(self):
        today = fields.Date.context_today(self)
        for patient in self:
            patient.age = 0
            if patient.date_of_birth:
                patient.age = today.year - patient.date_of_birth.year - ((today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day))

    @api.constrains("date_of_birth")
    def _check_date_of_birth(self):
        for patient in self:
            if patient.date_of_birth and patient.date_of_birth > date.today():
                raise ValidationError(_("La fecha de nacimiento no puede estar en el futuro."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("patient_serial", _("Nuevo")) == _("Nuevo"):
                vals["patient_serial"] = self.env["ir.sequence"].next_by_code("dental.patient") or _("Nuevo")
        return super().create(vals_list)
