from odoo import fields, http
from odoo.exceptions import AccessError, ValidationError
from odoo.http import request

from .common import error_response, json_response


class DentalClinicApiController(http.Controller):
    """REST endpoints authenticated with Odoo 19 native API keys."""

    def _payload(self):
        payload = request.httprequest.get_json(silent=True)
        if not isinstance(payload, dict):
            raise ValidationError("El cuerpo debe ser un objeto JSON.")
        return payload

    @staticmethod
    def _appointment_values(appointment):
        return {
            "id": appointment.id,
            "number": appointment.appointment_serial,
            "patient_id": appointment.patient_id.id,
            "doctor_id": appointment.doctor_id.id,
            "state": appointment.state,
            "start": fields.Datetime.to_string(appointment.start),
            "stop": fields.Datetime.to_string(appointment.stop),
        }

    @http.route(
        "/dental_clinic/api/v1/appointments",
        type="http",
        auth="bearer",
        methods=["GET"],
        csrf=False,
        readonly=True,
    )
    def list_appointments(self, **kwargs):
        try:
            limit = min(max(int(kwargs.get("limit", 50)), 1), 100)
        except (TypeError, ValueError):
            return error_response("limit debe ser un entero entre 1 y 100.")
        appointments = request.env["dental.appointment"].search([], limit=limit, order="start desc")
        return json_response({"data": [self._appointment_values(item) for item in appointments]})

    @http.route(
        "/dental_clinic/api/v1/appointments",
        type="http",
        auth="bearer",
        methods=["POST"],
        csrf=False,
    )
    def create_appointment(self, **kwargs):
        try:
            payload = self._payload()
            required = ("patient_id", "doctor_id", "start", "stop")
            missing = [name for name in required if not payload.get(name)]
            if missing:
                return error_response(f"Campos requeridos: {', '.join(missing)}.")
            values = {
                "patient_id": int(payload["patient_id"]),
                "doctor_id": int(payload["doctor_id"]),
                "start": fields.Datetime.to_datetime(payload["start"]),
                "stop": fields.Datetime.to_datetime(payload["stop"]),
                "appointment_type": payload.get("appointment_type", "reserved"),
                "chief_complaints": payload.get("chief_complaints", ""),
            }
            appointment = request.env["dental.appointment"].create(values)
        except (AccessError, ValidationError) as error:
            return error_response(str(error), 403 if isinstance(error, AccessError) else 422, "validation_error")
        except (TypeError, ValueError):
            return error_response("patient_id, doctor_id, start y stop tienen un formato inválido.")
        return json_response({"data": self._appointment_values(appointment)}, 201)
