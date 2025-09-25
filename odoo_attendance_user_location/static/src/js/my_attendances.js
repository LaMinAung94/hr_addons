/** @odoo-module **/

import { MyAttendances } from "@hr_attendance/js/my_attendances";
import { KioskConfirm } from "@hr_attendance/js/kiosk_confirm";
import { Dialog } from "@web/core/dialog/dialog";
import { session } from "@web/session";
import { _t } from "@web/core/l10n/translation";

/**
 * Show a consistent error dialog when geolocation fails
 */
function showLocationError(error) {
    const dialog = new Dialog(null, {
        title: error?.name || _t("Geolocation Error"),
        size: "medium",
        $content: $("<main/>", {
            role: "alert",
            text: (error?.message || _t("Location access denied.")) +
                  " " + _t("Also check your site connection is secured!"),
        }),
        buttons: [
            {
                text: _t("OK"),
                classes: "btn-primary",
                click: function () {
                    dialog.close();
                },
            },
        ],
    });
    dialog.open();
}

/**
 * Utility to get geolocation and extend session context
 */
function getGeolocationContext(successCallback, errorCallback) {
    if (!navigator.geolocation) {
        errorCallback({ name: "Geolocation Unsupported", message: _t("Your browser does not support geolocation.") });
        return;
    }

    navigator.geolocation.getCurrentPosition(
        function (position) {
            const ctx = Object.assign({}, session.user_context, {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
            });
            successCallback(ctx);
        },
        function (error) {
            errorCallback(error);
        }
    );
}

/**
 * Extend MyAttendances to include location
 */
MyAttendances.include({
    update_attendance() {
        const self = this;
        getGeolocationContext(
            function (ctx) {
                self._rpc({
                    model: "hr.employee",
                    method: "attendance_manual",
                    args: [[self.employee.id], "hr_attendance.hr_attendance_action_my_attendances"],
                    context: ctx,
                }).then((result) => {
                    if (result.action) {
                        self.do_action(result.action);
                    } else if (result.warning) {
                        self.displayNotification({
                            title: result.warning,
                            type: "danger",
                        });
                    }
                });
            },
            showLocationError
        );
    },
});

/**
 * Extend KioskConfirm (for both icon and PIN check-ins)
 */
KioskConfirm.include({
    events: Object.assign({}, KioskConfirm.prototype.events, {
        "click .o_hr_attendance_sign_in_out_icon": _.debounce(function () {
            const self = this;
            getGeolocationContext(
                function (ctx) {
                    self._rpc({
                        model: "hr.employee",
                        method: "attendance_manual",
                        args: [[self.employee_id], self.next_action],
                        context: ctx,
                    }).then((result) => {
                        if (result.action) {
                            self.do_action(result.action);
                        } else if (result.warning) {
                            self.displayNotification({
                                title: result.warning,
                                type: "danger",
                            });
                        }
                    });
                },
                showLocationError
            );
        }, 200, true),

        "click .o_hr_attendance_pin_pad_button_ok": _.debounce(function () {
            const self = this;
            this.pin_pad = true;
            const pin = self.$(".o_hr_attendance_PINbox").val();

            getGeolocationContext(
                function (ctx) {
                    self._rpc({
                        model: "hr.employee",
                        method: "attendance_manual",
                        args: [[self.employee_id], self.next_action, pin],
                        context: ctx,
                    }).then((result) => {
                        if (result.action) {
                            self.do_action(result.action);
                        } else if (result.warning) {
                            self.displayNotification({
                                title: result.warning,
                                type: "danger",
                            });
                            self.$(".o_hr_attendance_PINbox").val("");
                            setTimeout(() => {
                                self.$(".o_hr_attendance_pin_pad_button_ok").removeAttr("disabled");
                            }, 500);
                        }
                    });
                },
                showLocationError
            );
        }, 200, true),
    }),
});
