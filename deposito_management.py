from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

import re
import requests

class DepositoItemAssignWizard(models.TransientModel):
    _name = 'deposito.item.assign.wizard'
    _description = 'Wizard de Asignación de Item'

    item_id = fields.Many2one(
        'deposito.item',
        string='Item a Asignar',
        domain="[('status', '=', 'no_asignado')]",
        required=True
    )
    item_code = fields.Char(string='Código', related='item_id.code', readonly=True)
    item_serial = fields.Char(string='Serial', related='item_id.serial_number', readonly=True)
    item_deposito = fields.Many2one('deposito.bodega', string='Depósito', related='item_id.deposito_id', readonly=True)

    employee_id = fields.Many2one('hr.employee', string='Empleado Asignado', required=True)

    def action_assign(self):
        self.ensure_one()
        item = self.item_id
        if not item.deposito_id:
            raise UserError("El item no tiene depósito registrado. Regístrelo primero en 'Registro de Items'.")
        item.employee_id = self.employee_id
        item.last_assignment_datetime = fields.Datetime.now()
        item.message_post(body=f"Item asignado a {self.employee_id.name}.", subtype_xmlid="mail.mt_note")
        # REGISTRO EN LOG
        self.env['deposito.item.log'].create({
            'item_name': item.name,
            'quien_realizo_accion': self.env.user.name,
            'date': item.last_assignment_datetime,
            'employee_name': self.employee_id.name,
            'action_type': 'asignacion',
        })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Asignación exitosa',
                'message': f"El item {item.name} fue asignado a {self.employee_id.name}.",
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.client', 'tag': 'reload'}
            }
        }

class DepositoItemLog(models.Model):
    _name = 'deposito.item.log'
    _description = 'Log de Movimientos de Items'
    _order = 'date desc'

    item_name = fields.Char('Ítem', required=True)
    quien_realizo_accion = fields.Char('Quién realizó la acción', required=True)
    date = fields.Datetime('Fecha', required=True)
    employee_name = fields.Char('A quién se lo asignó/desasignó', required=True)
    action_type = fields.Selection([
        ('asignacion', 'Asignación'),
        ('desasignacion', 'Desasignación')
    ], string='Tipo', required=True)

class DepositoBodega(models.Model):
    _name = 'deposito.bodega'
    _description = 'Depósito / Bodega'

    name = fields.Char(string='Nombre', required=True)
    location_desc = fields.Text(string='Ubicación (Descripción)')
    latitude = fields.Float(string='Latitud', digits=(10, 7))
    longitude = fields.Float(string='Longitud', digits=(10, 7))
    maps_url = fields.Char(string='URL de Google Maps')

    @api.onchange('maps_url')
    def _onchange_maps_url(self):
        for rec in self:
            if not rec.maps_url:
                rec.latitude = 0.0
                rec.longitude = 0.0
                return

            url = rec.maps_url.strip()
            try:
                response = requests.head(url, allow_redirects=True, timeout=5)
                final_url = response.url
                match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', final_url)
                if match:
                    rec.latitude = float(match.group(1))
                    rec.longitude = float(match.group(2))
                else:
                    rec.latitude = 0.0
                    rec.longitude = 0.0
                    return {
                        'warning': {
                            'title': 'Coordenadas no encontradas',
                            'message': 'El enlace redirigido no contiene coordenadas visibles. Abre el enlace, copia la URL completa con coordenadas y vuelve a pegarla.',
                        }
                    }
            except Exception as e:
                rec.latitude = 0.0
                rec.longitude = 0.0
                return {
                    'warning': {
                        'title': 'Error de red',
                        'message': f'No se pudo acceder al enlace: {str(e)}',
                    }
                }

class DepositoItem(models.Model):
    _name = 'deposito.item'
    _description = 'Item Asignable'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre', required=True, tracking=True)
    code = fields.Char(string='Código', tracking=True)
    serial_number = fields.Char(string='Serial', tracking=True)
    deposito_id = fields.Many2one('deposito.bodega', string='Registra Deposito', required=True, tracking=True)

    assigned_deposito = fields.Many2one(
        'deposito.bodega',
        string='Depósito Asignado',
        related='deposito_id',
        store=True,
        readonly=True,
        tracking=True
    )

    employee_id = fields.Many2one('hr.employee', string='Empleado Asignado', tracking=True)
    description = fields.Text(string='Descripción / Notas', required=True, tracking=True)

    condition = fields.Selection([
        ('excelente', 'Excelente'),
        ('bueno', 'Bueno'),
        ('malo', 'Malo'),
    ], string='Condición del Ítem', required=True, tracking=True)
    assigned_condition = fields.Selection([
        ('excelente', 'Excelente'),
        ('bueno', 'Bueno'),
        ('malo', 'Malo'),
    ], string='Condición al Asignar',
        related='condition', readonly=True, store=True)

    status = fields.Selection(
        selection=[
            ('no_asignado', 'No Asignado'),
            ('asignado', 'Asignado')
        ],
        string='Estatus',
        compute='_compute_status',
        store=True,
        readonly=True
    )

    last_assignment_datetime = fields.Datetime(
        string='Fecha/Hora Última Asignación',
        readonly=True,
        tracking=True,
    )
    last_unassignment_datetime = fields.Datetime(
        string='Fecha/Hora Última Desasignación',
        readonly=True,
        tracking=True,
    )

    _sql_constraints = [
        ('unique_code', 'unique(code)', 'Atención, Código ya registrado. Verifique nuevamente.'),
        ('unique_serial', 'unique(serial_number)', 'Atención, Serial ya registrado. Verifique nuevamente.'),
    ]

    def action_asignar_item(self):
        now = fields.Datetime.now()
        for item in self:
            if item.status == 'asignado':
                raise UserError(
                    f"El item '{item.name}' ya está asignado. Debe desasignarlo antes de asignarlo a otro empleado."
                )
            if not item.employee_id:
                raise UserError(f"El item '{item.name}' no tiene un empleado asignado.")
            item.last_assignment_datetime = now
            item.message_post(
                body=f"Item asignado a {item.employee_id.name}.",
                subtype_xmlid="mail.mt_note"
            )
            # REGISTRO EN LOG
            self.env['deposito.item.log'].create({
                'item_name': item.name,
                'quien_realizo_accion': self.env.user.name,
                'date': now,
                'employee_name': item.employee_id.name,
                'action_type': 'asignacion',
            })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Asignación exitosa',
                'message': f"{len(self)} item(s) han sido asignados.",
                'type': 'success',
                'sticky': False,
            }
        }

    def action_desasignar_item(self):
        desasignados = 0
        now = fields.Datetime.now()
        for item in self:
            if item.employee_id:
                item.last_unassignment_datetime = now
                item.message_post(
                    body=f"Item desasignado de {item.employee_id.name}.",
                    subtype_xmlid="mail.mt_note"
                )
                # REGISTRO EN LOG
                self.env['deposito.item.log'].create({
                    'item_name': item.name,
                    'quien_realizo_accion': self.env.user.name,
                    'date': now,
                    'employee_name': item.employee_id.name,
                    'action_type': 'desasignacion',
                })
                item.employee_id = False
                desasignados += 1
        if desasignados == 0:
            raise UserError("Ninguno de los items seleccionados está asignado a un empleado.")
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Desasignación exitosa',
                'message': f"{desasignados} item(s) han sido desasignados.",
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.client', 'tag': 'reload'}
            }
        }

    @api.constrains('code', 'serial_number')
    def _check_unique_code_serial(self):
        for record in self:
            if record.code and self.search([('code', '=', record.code), ('id', '!=', record.id)], limit=1):
                raise ValidationError("Atención, Código ya registrado. Verifique nuevamente.")
            if record.serial_number and self.search([('serial_number', '=', record.serial_number), ('id', '!=', record.id)], limit=1):
                raise ValidationError("Atención, Serial ya registrado. Verifique nuevamente.")

    @api.depends('employee_id')
    def _compute_status(self):
        for record in self:
            record.status = 'asignado' if record.employee_id else 'no_asignado'

    def write(self, vals):
        """
        Crea log de asignación/desasignación cuando se modifica employee_id,
        ya sea por el formulario o por otro método.
        """
        for rec in self:
            old_employee = rec.employee_id
            new_employee_id = vals.get('employee_id', old_employee.id if old_employee else False)
            if 'employee_id' in vals:
                now = fields.Datetime.now()
                # Asignación
                if vals['employee_id']:
                    if not old_employee or old_employee.id != vals['employee_id']:
                        log_vals = {
                            'item_name': rec.name,
                            'quien_realizo_accion': rec.env.user.name,
                            'date': now,
                            'employee_name': rec.env['hr.employee'].browse(vals['employee_id']).name,
                            'action_type': 'asignacion',
                        }
                        rec.env['deposito.item.log'].create(log_vals)
                        vals['last_assignment_datetime'] = now
                # Desasignación
                else:
                    if old_employee:
                        log_vals = {
                            'item_name': rec.name,
                            'quien_realizo_accion': rec.env.user.name,
                            'date': now,
                            'employee_name': old_employee.name,
                            'action_type': 'desasignacion',
                        }
                        rec.env['deposito.item.log'].create(log_vals)
                        vals['last_unassignment_datetime'] = now
        return super(DepositoItem, self).write(vals)

    @api.model
    def create(self, vals):
        # Si se asigna un empleado al crear, registra la fecha de asignación
        if vals.get('employee_id'):
            vals['last_assignment_datetime'] = fields.Datetime.now()
        return super().create(vals)