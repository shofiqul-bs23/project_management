from odoo import fields, models, api


class Project(models.Model):
    # _name = 'project.modified'
    _inherit = 'project.project'
    _description = 'This will modify the project'

    test = fields.Char()
    rfq_ids = fields.Many2one('purchase.order')

    def requisitions(self):
        print("Hello World")
        return {
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref("purchase.purchase_order_form").id
        }

    # return {
    #     'name': _('Create invoice/bill'),
    #     'type': 'ir.actions.act_window',
    #     'view_mode': 'form',
    #     'res_model': 'account.move',
    #     'view_id': self.env.ref('account.view_move_form').id,
    #     'context': ctx,
    # }

