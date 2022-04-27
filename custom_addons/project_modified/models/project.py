from odoo import fields, models, api


class Project(models.Model):
    # _name = 'project.modified'
    _inherit = 'project.project'
    _description = 'This will modify the project'

    test = fields.Char()
    rfq_ids = fields.One2many('purchase.order', 'project_id', help="Holds the RFQs ")
    rfc_count = fields.Integer(default=0, compute = '_count_rfc')

    estimation_line_ids = fields.One2many('estimation.line', 'project_id')
    total_estimated_cost = fields.Float(compute = 'cal_total_estimated_cost')


    def requisitions(self):

        # lines = list()
        # line = self.estimation_line_ids[0]
        # 1

        # vals = {
        #     "product_id": line.product_id.id,
        #     "name" : line.product_id.name,
        #     "product_qty" : line.quantity,
        #     "price_unit" : line.price,
        #     # "order_id" : 1
        # }
        #
        # t = self.env['purchase.order.line'].create(vals)
        # lines.append(t.id)


        return {
            'res_model': 'purchase.order',
            # 'res_id' : 1,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            # 'view_id': self.env.ref("purchase.purchase_order_form").id,
            'context': {'default_project_id': self.id,
                        'default_order_line': [(0,0,{"product_id": line.product_id.id, "name": line.product_id.name, "product_qty" : line.quantity, "price_unit" : line.price,'product_uom':line.product_id.uom_id.id })
                                               for line in self.estimation_line_ids
                                               ],
                        }
        }

        # lines = list()
        # for line in self.estimation_line_ids:
        #
        #     # search_ids = self.env['purchase.order'].search([]).ids
        #     # last_id = search_ids and max(search_ids)
        #
        #     vals = {
        #         "product_id": line.product_id.id,
        #         "name" : line.product_id.name,
        #         "product_qty" : line.quantity,
        #         "price_unit" : line.price,
        #         # "order_id" : 1
        #     }
        #
        #     t = self.env['purchase.order.line'].create(vals)
        #     lines.append(t.id)
        #
        #
        # return {
        #     'res_model': 'purchase.order',
        #     # 'res_id' : 1,
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     # 'view_id': self.env.ref("purchase.purchase_order_form").id,
        #     'context': {'default_project_id': self.id,
        #                 'default_order_line': lines,
        #                 'default_partner_id':1
        #                 }
        # }



    def show_rfqs(self):
        self.ensure_one()

        return {
            'name': "RFQ form",
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [('project_id', '=', self.id)]
            # 'view_id': self.env.ref('purchase.purchase_order_kpis_tree').id
        }

    @api.depends('rfq_ids')
    def _count_rfc(self):
        self.rfc_count= len(self.rfq_ids.ids)

    # return {
    #     'name': _('Create invoice/bill'),
    #     'type': 'ir.actions.act_window',
    #     'view_mode': 'form',
    #     'res_model': 'account.move',
    #     'view_id': self.env.ref('account.view_move_form').id,
    #     'context': ctx,
    # }

    def cal_total_estimated_cost(self):
        for rec in self:
            temp = 0
            for x in rec.estimation_line_ids:
                temp += x.total_price
            rec.total_estimated_cost = temp