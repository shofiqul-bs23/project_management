from odoo import fields, models, api


class Purchase(models.Model):
    # _name = 'project.modified'
    _inherit = 'purchase.order'
    _description = 'This will modify the project'

    project_id = fields.Many2one('project.project', help="Holds the project that this RFQ includes.")

    def request_internal_transfer(self):
        return {
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            # 'view_id': self.env.ref("purchase.purchase_order_form").id,
            'context': {'default_picking_type_id': self.fetch_it_id()}
        }

    def fetch_it_id(self):
        # return 5
        picking_types = self.env['stock.picking.type'].search([])
        for x in picking_types:
            if x.name == 'Internal Transfers':
                return x.id
        return True