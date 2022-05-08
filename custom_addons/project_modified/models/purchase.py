from odoo import fields, models, api


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    estimation_line = fields.Many2one('estimation.line', 'purchase_lines')

    # def create(self, vals_list):
    #     print(vals_list)
    #     return super(PurchaseOrderLine, self).create(vals_list)


class Purchase(models.Model):
    # _name = 'project.modified'
    _inherit = 'purchase.order'
    _description = 'This will modify the project'

    project_id = fields.Many2one('project.project', help="Holds the project that this RFQ includes.")



    def request_internal_transfer(self):
        lines = self.order_line

        # res = list()
        # self.button_approve()
        # for line in lines:
        #     vals = {'product_id': line.product_id.ids[0] ,'product_uom_qty' : line.product_uom_qty,'name':line.product_id.display_name,'product_uom':line.product_uom.id,
        #             'location_id':1, 'location_dest_id':1}
        #     t = self.env['stock.move'].create(vals)
        #     res.append(t.id)

        li = lines[0]

        res = [(0, 0, {'product_id': line.product_id.ids[0], 'product_uom_qty': line.product_uom_qty,
                       'name': line.product_id.display_name, 'product_uom': line.product_uom.id})
               for line in lines
               ]

        return {
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            # 'view_id': self.env.ref("purchase.purchase_order_form").id,
            'context': {'default_picking_type_id': self.fetch_it_id(),
                        'default_move_ids_without_package':res,
                        'default_partner_id':self.read()[0]['company_id'][0],
                        # 'order':self
                        }
        }

    # it == internal transfer
    def fetch_it_id(self):
        # return 5
        picking_types = self.env['stock.picking.type'].search([])
        for x in picking_types:
            if x.name == 'Internal Transfers':
                return x.id
        return True

