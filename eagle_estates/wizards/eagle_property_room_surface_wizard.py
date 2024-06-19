from odoo import api, fields, models


class EaglePropertyRoomSurfaceWizard(models.TransientModel):
    _name = "eagle.property.room.surface.wizard"
    _description = "Compute Property Room Surface"

    room_id = fields.Many2one("eagle.property.room", string="Room", required=True)
    length = fields.Float()
    width = fields.Float()
    surface = fields.Float(compute="_compute_surface")

    @api.depends('length', 'width')
    def _compute_surface(self):
        for record in self:
            record.surface = record.length * record.width

    def action_confirm(self):
        self.room_id.surface = self.surface
        return {'type': 'ir.actions.act_window_close'}
