from odoo import fields, models, api

class Purchase(models.Model):
    # _name = 'project.modified'
    _inherit = 'purchase.order'
    _description = 'This will modify the project'

    project_id = fields.Many2one('project.project',help="Holds the project that this RFQ includes.")
