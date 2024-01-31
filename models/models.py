# -*- coding: utf-8 -*-

import base64
import csv
import io
from odoo import models, fields, api


# class forecast(models.Model):
#     _name = 'forecast.forecast'
#     _description = 'forecast.forecast'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class Forecast(models.Model):
    _name = "import_forecast.forecast"
    _description = "อัพโหลดข้อมูล Forecast"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(size=50, string="Customer Name",
                       tracking=True, readonly=True)
    partner_id = fields.Many2one(
        'res.partner', string="Customer", required=True, tracking=True)
    on_month = fields.Date(string="On Month", required=True,
                           tracking=True, default=lambda self: fields.datetime.now())
    revise_level = fields.Selection([('0', 'Revise 0'), ('1', 'Revise 1'), ('2', 'Revise 2'), (
        '3', 'Revise 3')], string="Revise Level", tracking=True, required=True)
    file_forecast_name = fields.Char(
        size=50, string="File Name", tracking=True)
    file_forecast = fields.Binary(
        string="Import Forecast", required=True, tracking=True)
    img_partner = fields.Image(
        compute="_value_partner_image", store=True, readonly=True)
    line_ids = fields.One2many("import_forecast.forecast_detail", "forecast_id",
                               string="Forecast Detail", required=True, tracking=True)
    item = fields.Integer(string="Item", tracking=True,
                          readonly=True, default="0")
    qty = fields.Float(string="Qty", tracking=True, readonly=True, default="0")
    _on_month = fields.Char(size=8, compute="_value_on_month",
                            string="On Month", store=True, tracking=True)
    partner_street = fields.Char(
        size=255, string="street", store=True, readonly=True)
    partner_zip = fields.Char(size=255, string="zip",
                              store=True, readonly=True)
    partner_city = fields.Char(
        size=255, string="city", store=True, readonly=True)
    partner_country_id = fields.Char(
        size=255, string="country_id", store=True, readonly=True)
    partner_phone = fields.Char(
        size=255, string="phone", store=True, readonly=True)
    partner_mobile = fields.Char(
        size=255, string="mobile", store=True, readonly=True)
    partner_email = fields.Char(
        size=255, string="email", store=True, readonly=True)
    partner_website = fields.Char(
        size=255, string="website", store=True, readonly=True)

    @api.depends('on_month')
    def _value_on_month(self):
        for r in self:
            r._on_month = r.on_month.strftime("%m/%Y")

    @api.depends('partner_id')
    def _value_partner_image(self):
        for r in self:
            r.img_partner = r.partner_id.image_1920
            r.name = r.partner_id.name
            r.partner_street = r.partner_id.street
            r.partner_zip = r.partner_id.zip
            r.partner_city = r.partner_id.city
            r.partner_country_id = r.partner_id.country_id.name
            r.partner_phone = r.partner_id.phone
            r.partner_mobile = r.partner_id.mobile
            r.partner_email = r.partner_id.email
            r.partner_website = r.partner_id.website

    @api.model_create_multi
    def create(self, obj):
        req = super().create(obj)
        if req.file_forecast:
            csv_data = base64.b64decode(req.file_forecast)
            data_file = io.StringIO(csv_data.decode("utf-8"))
            data_file.seek(0)
            file_reader = []
            csv_reader = csv.reader(data_file, delimiter=',')
            file_reader.extend(csv_reader)
            seq = 0
            # print(f"Start Sequence:{seq}")
            for r in file_reader:
                # print(r)
                if seq > 0:
                    if seq > 0:
                        partCode = str(r[0]).strip()
                        # partName = str(r[1]).strip()
                        # partPrice = float(str(r[2]))
                        partN = float(str(r[3]))
                        partN1 = float(str(r[4]))
                        partN2 = float(str(r[5]))
                        partN3 = float(str(r[6]))
                        # print(f"partCode: {partCode} partN: {partN}")
                        # Get Product Data
                        prodID = self.env['product.product'].search(
                            [('default_code', '=', partCode)], limit=1)
                        # print(f"prodID: {prodID}")
                        self.env["import_forecast.forecast_detail"].create({
                            "seq": seq,
                            "forecast_id": req.id,
                            "part_id": prodID.id,
                            "qty": partN,
                            "month_1": partN1,
                            "month_2": partN2,
                            "month_3": partN3,
                        })
                        # print(f"Insert ID: {req.id}")
                seq += 1
            # print(f"Total: {seq}")

        return req

    @api.onchange('file_forecast')
    def upload_forecast_detail(self):
        if self.file_forecast:
            csv_data = base64.b64decode(self.file_forecast)
            data_file = io.StringIO(csv_data.decode("utf-8"))
            data_file.seek(0)
            file_reader = []
            csv_reader = csv.reader(data_file, delimiter=',')
            file_reader.extend(csv_reader)
            seq = 0
            # print(f"ID: {self.id}")
            for r in file_reader:
                if seq > 0:
                    partCode = str(r[0]).strip()
                    partName = str(r[1]).strip()
                    partPrice = float(str(r[2]))
                    # partN = float(str(r[3]))
                    # partN1 = float(str(r[4]))
                    # partN2 = float(str(r[5]))
                    # partN3 = float(str(r[6]))

                    prodID = self.env['product.product'].search(
                        [('default_code', '=', partCode)])
                    if len(prodID) == 0:
                        self.env['product.product'].create({
                            'name': partName,
                            'standard_price': partPrice,
                            'list_price': partPrice,
                            'weight': 0,
                            'default_code': partCode,
                            'description_sale': partName,
                            'detailed_type': 'consu',
                        })

                seq += 1
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'title': "ข้อความแจ้งเตือน!",
                'message': "อัพโหลดเอกสารเรียบร้อยแล้ว",
                'sticky': False,
                'fadeout': 'slow',
                'next': {
                    'type': 'ir.actions.act_window_close',
                }
            }
        }


class ForecastDetail(models.Model):
    _name = "import_forecast.forecast_detail"
    _description = "รายละเอียด Forecast Detail"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    seq = fields.Integer(string="Seq", default="1")
    name = fields.Char(size=50, string="Forecast No.",
                       compute="_value_forecast_name", tracking=True, readonly=True)
    forecast_id = fields.Many2one(
        'import_forecast.forecast', string='Forecast No', required=True, tracking=True)
    part_id = fields.Many2one(
        'product.product', string="Part No", tracking=True)
    part_name = fields.Char(size=255, string="Part Name",
                            compute="_value_part_name", tracking=True, readonly=True)
    qty = fields.Float(string="N", required=True, tracking=True)
    month_1 = fields.Float(string="N+1", tracking=True, default="0")
    month_2 = fields.Float(string="N+2", tracking=True, default="0")
    month_3 = fields.Float(string="N+3", tracking=True, default="0")

    @api.depends('forecast_id')
    def _value_forecast_name(self):
        for r in self:
            r.name = r.forecast_id.name

    @api.depends('part_id')
    def _value_part_name(self):
        for r in self:
            r.part_name = r.part_id.name
