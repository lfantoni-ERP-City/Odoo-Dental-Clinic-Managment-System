/** @odoo-module **/

import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";

class DentalToothChart extends Component {
    static template = "dental_clinic.DentalToothChart";
    static props = { ...standardWidgetProps };

    setup() {
        this.notification = useService("notification");
    }

    get upperRight() {
        return [18, 17, 16, 15, 14, 13, 12, 11];
    }

    get upperLeft() {
        return [21, 22, 23, 24, 25, 26, 27, 28];
    }

    get lowerRight() {
        return [48, 47, 46, 45, 44, 43, 42, 41];
    }

    get lowerLeft() {
        return [31, 32, 33, 34, 35, 36, 37, 38];
    }

    get procedureLines() {
        return this.props.record.data.procedure_line_ids?.records || [];
    }

    hasProcedure(tooth) {
        return this.procedureLines.some((line) => line.data.tooth_no === String(tooth));
    }

    toothClass(tooth) {
        return this.hasProcedure(tooth)
            ? "o_dental_tooth o_dental_tooth--treated"
            : "o_dental_tooth";
    }

    toothTitle(tooth) {
        return this.hasProcedure(tooth)
            ? _t("Diente %s: tiene procedimientos registrados", tooth)
            : _t("Añadir procedimiento para el diente %s", tooth);
    }

    async addProcedure(tooth) {
        if (this.props.readonly) {
            return;
        }
        const procedures = this.props.record.data.procedure_line_ids;
        if (!procedures?.addNewRecord) {
            this.notification.add(_t("No se pudo preparar la línea de procedimiento."), { type: "danger" });
            return;
        }
        await procedures.addNewRecord({
            context: { default_tooth_no: String(tooth) },
            position: "bottom",
        });
        this.notification.add(_t("Selecciona el procedimiento para el diente %s.", tooth), { type: "info" });
    }
}

const dentalToothChart = {
    component: DentalToothChart,
    fieldDependencies: [
        {
            name: "procedure_line_ids",
            type: "one2many",
            relation: "dental.procedure.line",
            relationField: "appointment_id",
        },
    ],
};

registry.category("view_widgets").add("dental_tooth_chart", dentalToothChart);
