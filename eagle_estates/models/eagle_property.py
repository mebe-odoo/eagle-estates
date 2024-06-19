from odoo import models, fields


class EagleProperty(models.Model):
    _name = "eagle.property"
    _description = "Eagle Property"

    name = fields.Char(string="Property Name", required=True)
    construction_date = fields.Date("Construction Date", required=True, default=fields.Date.today)
    surface = fields.Float("Surface", default=0.0)
