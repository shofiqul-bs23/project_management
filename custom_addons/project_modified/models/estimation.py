from odoo import fields, models, api


class Estimation(models.Model):
    _name = 'estimation.line'
    _description = 'Simply an estimation line'

    product_id = fields.Many2one('product.template')
    quantity = fields.Integer(default=1)
    price = fields.Float(default=1)
    total_price = fields.Float(compute="cal_total_price")

    project_id = fields.Many2one('project.project')

    @api.depends('quantity','price')
    def cal_total_price(self):
        for rec in self:
            rec.total_price = rec.price * rec.quantity
