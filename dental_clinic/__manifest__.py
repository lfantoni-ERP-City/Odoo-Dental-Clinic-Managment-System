# -*- coding: utf-8 -*-
{
    "name": "Clínica Dental Ecuador",
    "summary": "Historia clínica odontológica, citas y prescripciones para Ecuador",
    "version": "19.0.1.0.0",
    "category": "Services/Healthcare",
    "author": "ERP City S.A.S.",
    "license": "LGPL-3",
    "depends": ["mail", "product", "l10n_ec"],
    "data": [
        "security/dental_clinic_security.xml",
        "security/ir.model.access.csv",
        "data/dental_clinic_data.xml",
        "views/dental_clinic_views.xml",
    ],
    "application": True,
    "installable": True,
}
