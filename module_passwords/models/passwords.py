# -*- coding: utf-8 -*-

import time
import logging
from time import mktime
from datetime import timedelta, datetime
from odoo import models, fields, api, exceptions, _
import json
import base64
import random, string
from simplecrypt import encrypt, decrypt
_logger = logging.getLogger(__name__)

class Tag(models.Model):

    _name = "res.partner.passwords.tag"
    _description = "Password Tag"

    name = fields.Char('Tag Name', required=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [('name_uniq', 'unique (name)', "Tag name already exists !"),]

class Password(models.Model):
    _name = 'res.partner.passwords'
    #_inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherit = ['mail.thread']
    _mail_post_access = 'read'
    
    @api.depends('compute_password', 'password', 'level', 'user')
    def _get_clipboard_password(self):
        for r in self:
            r.clipboard_password = r.compute_password

    name = fields.Char(string=_("Name"), track_visibility='onchange', required=True)
    partner_id = fields.Many2one('res.partner', string=_("Client"), required=True)
    date = fields.Datetime(string=_("Create date"), default=fields.Datetime.now, required=True)
    user_id = fields.Many2one('res.users', track_visibility='onchange', string=_("Author"), default=lambda self: self.env.user, required=True)
    ip_server = fields.Char(string=_("Ip / Url"), track_visibility='onchange', required=True)
    level = fields.Selection([('1',_('Level 1')),('2',_('Level 2')),('3',_('Level 3'))], default='1', required=True)
    user = fields.Char(string=_("User"), required=True)
    compute_key = fields.Char(string=_("Key"), compute="get_key", inverse="set_key")
    compute_password = fields.Char(string=_("Password"), compute="get_password", inverse="set_password")
    clipboard_password = fields.Char(string=_("Clipboard password"), compute="_get_clipboard_password")
    password = fields.Char(string=_("Password Original"))
    tag_ids = fields.Many2many('res.partner.passwords.tag', 'password_tags_rel', 'password_id', 'tag_id', string='Tags')
    note = fields.Text(string=_("Note"))
    active = fields.Boolean(default=True)

    def get_password(self):
        for rec in self:
            if rec.compute_key and rec.password:
                return self.decrypt_aes(rec.compute_key, rec.password)
            else:
                return ''

    def set_password(self):

        return False
    
    @api.onchange('compute_key')
    def decryptpasswordbykey(self):
        if self.compute_key and self.password:
            self.compute_password = self.decrypt_aes(self.compute_key, self.password)

    def get_key(self):
        return 'GuW45ayPvrAz1o630f9MrOAv3FnzJJ37'
        
    def set_key(self):
        return False
    
    def encrypt_aes(self, key, val_password):
        #obj = AES.new(key, AES.MODE_CBC, 'GuW45ayPvrAz1o630f9MrOAv3FnzJJ37')
        #ciphertext = obj.encrypt(val_password)
        #return ciphertext
        if key and val_password:
            key = base64.encodestring(key.encode())
            val_password = base64.encodestring(val_password.encode())
            #_logger.info("Encriptando password: b "+str(val_password)+" con clave "+str(key)+" ciphertext...")
            ciphertext = encrypt(key, bytes(val_password)) #cadena encriptada en bytes
            return base64.encodestring(ciphertext).decode()
        else:
            return ''
        
    def decrypt_aes(self, key, val_password):
        #obj = AES.new(key, AES.MODE_CBC, 'GuW45ayPvrAz1o630f9MrOAv3FnzJJ37')
        #return obj.decrypt(val_password)
        if key and val_password:
            key = base64.encodestring(key.encode())
            password_dec = base64.decodestring(val_password.encode())

            try:
                plain_text = decrypt(bytes(key), password_dec)
                plain_text = base64.decodestring(plain_text)
                return plain_text.decode('utf-8');
            except:
                return ''.join(random.choice(string.ascii_lowercase) for i in range(12))
        else:
            return ''
    
    def encode(self, key, clear):
        enc = []
        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc))

    def decode(self, key, enc):
        dec = []
        enc = base64.urlsafe_b64decode(enc)
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)
    
    @api.model
    def create(self, vals):
        if 'compute_key' in vals and 'compute_password' in vals:
            if vals["compute_key"] and vals["compute_password"]:
                vals["password"] = str(self.encrypt_aes(vals["compute_key"], vals["compute_password"]))
        rec = super(Password, self).create(vals)
        return rec

    @api.multi
    def write(self, valsNew, context=None):
        if 'compute_key' in valsNew and 'compute_password' in valsNew:
            if valsNew["compute_key"] and valsNew["compute_password"]:
                valsNew["password"] = str(self.encrypt_aes(valsNew["compute_key"], valsNew["compute_password"]))
        rec = super(Password, self).write(valsNew)
        return rec