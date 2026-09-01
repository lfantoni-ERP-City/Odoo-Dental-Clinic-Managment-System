from datetime import timedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestDentalClinic(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.doctor = cls.env["dental.doctor"].create({"name": "Dra. Prueba"})
        cls.patient = cls.env["dental.patient"].create({
            "patient_name": "Paciente Prueba",
            "identification_type": "cedula",
            "identification": "0102030405",
        })

    def test_patient_history_is_generated(self):
        self.assertNotEqual(self.patient.patient_serial, "Nuevo")

    def test_overlapping_appointments_are_rejected(self):
        start = fields.Datetime.now().replace(minute=0, second=0, microsecond=0)
        self.env["dental.appointment"].create({
            "patient_id": self.patient.id,
            "doctor_id": self.doctor.id,
            "start": start,
            "stop": start + timedelta(hours=1),
        })
        with self.assertRaises(ValidationError):
            self.env["dental.appointment"].create({
                "patient_id": self.patient.id,
                "doctor_id": self.doctor.id,
                "start": start + timedelta(minutes=30),
                "stop": start + timedelta(hours=2),
            })
