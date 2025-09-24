/** @odoo-module **/

import { registry } from "@web/core/registry";
import { download } from "@web/core/network/download";
import { session } from "@web/session";
import { blockUI, unblockUI } from "@web/core/utils/ui";

registry.category("ir.actions.report handlers").add("xlsx", async (action) => {
    if (action && action.report_type === "xlsx") {
        blockUI();
        const def = new Promise((resolve, reject) => {
            session.get_file({
                url: "/xlsx_reports",
                data: action.data,
                success: resolve,
                error: reject,
                complete: unblockUI,
            });
        });
        return def;
    }
});
