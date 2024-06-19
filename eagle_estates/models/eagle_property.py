from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import relativedelta
from odoo.osv.expression import AND


class EagleProperty(models.Model):
    _name = "eagle.property"
    _description = "Eagle Property"
    _order = 'construction_date DESC, id'
    # There is no need to explicitly set _rec_name to name in this case,
    # as that is the default value.
    _rec_name = 'name'

    name = fields.Char(string="Property Name", required=True)
    construction_date = fields.Date("Construction Date", required=True, default=fields.Date.today)
    surface = fields.Float("Surface", compute='_compute_surface')

    tag_ids = fields.Many2many('eagle.tag', string="Tags")
    room_ids = fields.One2many('eagle.property.room', 'property_id', string="Rooms")

    # Address fields
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    age = fields.Integer("Age", compute="_compute_age", inverse="_inverse_age", readonly=False)

    parent_id = fields.Many2one('eagle.property', string="Parent Property")
    child_ids = fields.One2many('eagle.property', 'parent_id', string="Child Properties")

    room_count = fields.Integer(compute="_compute_room_count")

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Property name must be unique'),
    ]

    @api.depends("room_ids")
    def _compute_room_count(self):
        for record in self:
            record.room_count = len(record.room_ids)

    def action_view_rooms(self):
        action = self.env.ref("eagle_estates.eagle_property_rooms_action").read()[0]
        action["domain"] = [("property_id", "=", self.id)]
        return action

    def action_create_room(self):
        action = self.env.ref("eagle_estates.eagle_property_rooms_action").read()[0]
        action["context"] = {"default_property_id": self.id}
        action["views"] = [(False, 'form')]
        return action

    @api.constrains('construction_date')
    def _constrain_construction_date(self):
        for record in self:
            if record.construction_date > fields.Date.today():
                raise ValidationError("Construction date can't be in the future")

    @api.depends('room_ids')
    def _compute_surface(self):
        for record in self:
            record.surface = sum(record.room_ids.mapped('surface') or [0.0])

    @api.depends('construction_date')
    def _compute_age(self):
        for property_id in self:
            property_id.age = (property_id.construction_date and relativedelta(
                fields.Date.today(), property_id.construction_date).years) or 0

    def _inverse_age(self):
        for property_id in self:
            property_id.construction_date = fields.Date.today() - relativedelta(years=property_id.age)

    @api.depends('construction_date')
    def _compute_display_name(self):
        for record in self:
            name = record.name
            if record.construction_date:
                name += " | " + str(record.construction_date)
            record.display_name = name

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        if name:
            domain = AND([domain, ['|', ('name', 'ilike', name), ('construction_date', 'ilike', name)]])
        return self._search(domain, limit=limit, order=order)
