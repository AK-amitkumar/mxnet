# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
import xlrd,base64,datetime


class ImportWizard(models.TransientModel):
    _inherit = 'import.wizard'

    # 数据导入
    @api.multi
    def import_excel(self):
        if self.data:
            excel_obj = xlrd.open_workbook(file_contents=base64.decodestring(self.data))
            sheets = excel_obj.sheets()
            upc_obj = self.env['b2b.upc.list']
            product_obj = self.env['product.product']
            for sh in sheets:
                for row in range(1, sh.nrows):
                    code = sh.cell(row, 0).value
                    code = code.replace(' ', '')
                    if type(code) is not unicode:
                        raise UserError(u'%s 编码必须为文本类型，不能为数字格式' % code)
                    result = upc_obj.sudo().search([('name', '=', code)])
                    if result:
                        continue
                    product = product_obj.sudo().search([('barcode', '=', code)])
                    if product:
                        continue
                    upc_obj.create({'name':code})
                    # code.assign_upc_codes()
        return {'name': u'UPC码',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'b2b.upc.list',
                'context': {'create': False},
                }


