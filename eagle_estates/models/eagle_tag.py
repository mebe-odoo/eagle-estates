from odoo import models, fields


class EagleTag(models.Model):
    _name = 'eagle.tag'
    _description = 'Eagle Tag'

    name = fields.Char(required=True)
