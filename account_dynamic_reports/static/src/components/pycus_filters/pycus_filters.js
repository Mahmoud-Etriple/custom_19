/** @odoo-module **/

import { registry } from '@web/core/registry';
import { loadJS } from "@web/core/assets"
import { PycusDropdown } from "../pycus_dropdown/pycus_dropdown";
import { useBus, useService,  } from "@web/core/utils/hooks";
import { DateTimeInput } from "@web/core/datetime/datetime_input";
import { SelectMenu } from "@web/core/select_menu/select_menu";
const { DateTime } = luxon;
import {
    Component,
    EventBus,
    onWillStart,
    onMounted,
    status,
    useEffect,
    useExternalListener,
    useRef,
    useState,
    useChildSubEnv,
} from "@odoo/owl";

export class PycusFilters extends Component {
    setup() {
        this.ormService = useService("orm");
        this.state = useState({
            defaultAccountValues: this.props.filterValues.defaultAccountValues, // [{value:5, label:'XYZ'}]
            defaultJournalValues: this.props.filterValues.defaultJournalValues,
            defaultPartnerValues: this.props.filterValues.defaultPartnerValues,
            defaultAccountTagValues: this.props.filterValues.defaultAccountTagValues,
            account_ids: [],
            journal_ids: [],
            partner_ids: [],
            account_tag_ids: [],
            date_from: luxon.DateTime.fromISO(this.props.filterValues.date_from),
            date_to: luxon.DateTime.fromISO(this.props.filterValues.date_to),
            date_range: {
                choices: [],
                selectedValue: {}
            },
        })

        onWillStart(async () => {

        });

        onMounted(() => {
            this.state.date_from = luxon.DateTime.fromISO(this.props.filterValues.date_from)
            this.state.date_to = luxon.DateTime.fromISO(this.props.filterValues.date_to)

            this.state.date_range = this.props.filterValues.date_range

        });

        this.handleDateRangeSelect = async (val) => {
            this.state.date_range.selectedValue.value = val
            this.props.updateValues(this)
        }

    }

    selectedAccounts(vals) {
        this.state.account_ids = vals
        this.props.updateValues(this)
    }

    selectedJournals(vals) {
        this.state.journal_ids = vals
        this.props.updateValues(this)
    }

    selectedPartners(vals) {
        this.state.partner_ids = vals
        this.props.updateValues(this)
    }

    selectedAccountTags(vals) {
        this.state.account_tag_ids = vals
        this.props.updateValues(this)
    }

    markDateRangeCustom() {
        // Picking a date by hand switches the range to Custom. Without this the
        // server recomputes date_from/date_to from the named range on Apply and
        // the hand-picked dates are silently discarded.
        if (this.state.date_range && this.state.date_range.selectedValue) {
            this.state.date_range.selectedValue.value = 'custom';
        }
    }

    onDateFromChanged(dateFrom) {
        this.state.date_from = dateFrom
        this.markDateRangeCustom()
        this.props.updateValues(this)
    }

    onDateToChanged(dateTo) {
        this.state.date_to = dateTo
        this.markDateRangeCustom()
        this.props.updateValues(this)
    }

}
// Define the template for the dropdown component
PycusFilters.props = { updateValues: Function, filterValues: {}}
PycusFilters.template = 'account_dynamic_reports.PycusFilters';
PycusFilters.components = { PycusDropdown, DateTimeInput, SelectMenu };