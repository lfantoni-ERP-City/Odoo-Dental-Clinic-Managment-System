# Clínica Dental Ecuador — Odoo 19

Módulo para administrar pacientes, odontólogos, agenda, procedimientos, prescripciones y adjuntos clínicos en Odoo 19 Enterprise sobre Odoo.sh.

## Alcance ecuatoriano

- Dependencia de `l10n_ec`; la compañía debe tener configurado Ecuador, USD y sus datos tributarios en Odoo.
- Identificación de paciente para cédula, RUC, pasaporte u otro documento.
- Interfaz y documentos de operación en español.
- Datos clínicos y agenda separados por compañía mediante ACL y reglas de registro.

La emisión electrónica de comprobantes del SRI no se genera desde este módulo. Debe configurarse con la localización ecuatoriana y Facturación de Odoo; esta separación evita duplicar lógica tributaria certificada.

## Instalación en Odoo.sh

1. Agrega este repositorio o el directorio `dental_clinic` al repositorio conectado a Odoo.sh.
2. Crea una rama de desarrollo y confirma que el build usa Odoo 19.
3. En Apps, actualiza la lista de aplicaciones e instala **Clínica Dental Ecuador**.
4. Asigna a cada usuario el rol **Usuario de clínica** o **Administrador de clínica** y valida el acceso con una compañía de prueba.
5. Convierte la rama en staging y prueba con una copia anonimizada de los datos de producción antes de fusionar a producción.

## API REST

La API no acepta contraseñas ni crea tokens propios. Usa una API key nativa de Odoo 19 con el rol de clínica correspondiente:

```http
Authorization: Bearer <api-key-de-odoo>
Content-Type: application/json
```

| Método | Ruta | Uso |
| --- | --- | --- |
| `GET` | `/dental_clinic/api/v1/appointments?limit=50` | Consulta de citas accesibles al usuario. |
| `POST` | `/dental_clinic/api/v1/appointments` | Creación de una cita. |

Ejemplo de creación:

```json
{
  "patient_id": 12,
  "doctor_id": 4,
  "start": "2026-09-02 09:00:00",
  "stop": "2026-09-02 09:30:00",
  "appointment_type": "reserved",
  "chief_complaints": "Control odontológico"
}
```

Las llamadas se ejecutan con los permisos y las reglas multi-compañía del usuario de la clave. Nunca incluyas API keys en el repositorio ni en parámetros de configuración versionados.
