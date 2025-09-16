from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
class HrExpense(models.Model):
    _inherit = 'hr.expense'

    @api.model
    def action_create_and_submit_sheets (self):
        """Create an expense Report."""

        for exp in self:
            if exp.state != 'draft':
                raise ValidationError(_("Selected Expense should be in the 'To Report' status."))
            # 🔎 Duplicate Check: category, amount, date
            duplicate = self.env['hr.expense'].search([
                ('id', '!=', exp.id),
                ('employee_id', '=', exp.employee_id.id),
                ('product_id', '=', exp.product_id.id),   # expense category
                ('total_amount', '=', exp.total_amount),
                ('date', '=', exp.date),
                ('state', '!=', 'cancel'),
            ], limit=1)

            if duplicate:
                raise ValidationError(
                    _("An expense with the same category, amount and date already exists "
                      "for employee %s.") % exp.employee_id.name
                )
            # Create expense sheet
            if exp.state == 'draft':
                sheet = self.env['hr.expense.sheet'].create({
                    'name': exp.name,
                    'employee_id': exp.employee_id.id,
                    'expense_line_ids': [(6, 0, exp.id)],
                })
        return sheet


