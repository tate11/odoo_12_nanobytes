odoo.define('perso_signature_pin.signature_pin_form', function (require){
    "use strict";
    require('web_editor.ready');
    require('web.dom_ready');

    var ajax = require('web.ajax');
    var base = require('web_editor.base');
    var core = require('web.core');
    var Widget = require("web.Widget");
    var rpc = require("web.rpc");
    var config = require('web.config');
    var website = require('website.website');
    var _t = core._t; 

    var qweb = core.qweb;

    var emailSent = 0;

    var SignaturePinForm = Widget.extend({
        template: 'perso_signature_pin.portal_signature_pin',
        events: {
            'click #boton_submit': 'submitForm2',
        },

        init: function(parent, options) {
            this._super.apply(this, arguments);
            this.options = _.extend(options || {}, {
                csrf_token: odoo.csrf_token,
            });
        },

        willStart: function() {
            return this._loadTemplates();
        },

        start: function() {
            this.initSign();
        },

        // Signature
        initSign: function () {
            console.log("INIT");
        },

        clickTest: function () {
            console.log("SUBMIT");
        },

        submitForm2: function(ev){
            // extract data
            var self = this;
            var $confirm_btn = self.$el.find('button[type="submit"]');


            //var href = self.$el.find('form').attr("action");
            var href = window.location.href;
            if (href) {
                //var action = href.match(/orders\/([a-z]+)/)[1];
                var action = 'accept';
                var order_id = parseInt(href.match(/orders\/([0-9]+)/)[1]);
                //var token = href.match(/token=(.*)&/)[1];
                var token = href.match(/access_token=(.*)&/);
                if (token != null){
                    token = token[1];
                }
                else{
                    token = href.match(/access_token=(.*)/)[1];
                }
            }
            else {
                var action = 'accept';
                var order_id = self.$el.find('form').data("order-id");
                var token = self.$el.find('form').data("token");
            }

            if (action == 'accept') {
                ev.preventDefault();
                // process : display errors, or submit
                //var signer_name = self.$("#name").val();
                var signer_name = document.getElementById("name").value;
                //var signer_pin = parseInt(self.$("#pin").val(),0);
                var signer_pin = parseInt(document.getElementById("pin").value);

                var active_more_fields = self.$("#bool_active_more_fields").val();
                var fiscal_name, comercial_name, frontis, enterprise_name, adress, apartado_correos, city, postal_code, province, phone, phone2, fax, email, web_site, activity, responsable, order_payment_type, productos_expone = "";

                if(active_more_fields){
                    fiscal_name = self.$("#fiscal_name").val();
                    comercial_name = self.$("#comercial_name").val();
                    frontis = self.$("#frontis").val();
                    //enterprise_name = self.$("#enterprise_name").val();
                    adress = self.$("#adress").val();
                    apartado_correos = self.$("#apartado_correos").val();
                    city = self.$("#city").val();
                    postal_code = self.$("#postal_code").val();
                    province = self.$("#province").val();
                    phone = self.$("#phone").val();
                    phone2 = self.$("#phone2").val();
                    fax = self.$("#fax").val();
                    email = self.$("#email").val();
                    web_site = self.$("#web_site").val();
                    activity = self.$("#activity").val();
                    responsable = self.$("#responsable").val();
                    order_payment_type = self.$("#order_payment_type").val();
                    productos_expone = self.$("#productos_expone").val();

                    self.$('#signer_fiscal_name').toggleClass('has-error', !fiscal_name);
                    self.$('#signer_comercial_name').toggleClass('has-error', !comercial_name);
                    //self.$('#signer_frontis').toggleClass('has-error', !frontis);
                    //self.$('#signer_enterprise_name').toggleClass('has-error', !enterprise_name);

                    self.$('#signer_adress').toggleClass('has-error', !adress);
                    //self.$('#signer_apartado_correos').toggleClass('has-error', !apartado_correos);
                    self.$('#signer_city').toggleClass('has-error', !city);
                    self.$('#signer_postal_code').toggleClass('has-error', !postal_code);
                    self.$('#signer_province').toggleClass('has-error', !province);

                    self.$('#signer_phone').toggleClass('has-error', !phone);
                    //self.$('#signer_phone2').toggleClass('has-error', !phone2);

                    self.$('#signer_email').toggleClass('has-error', !email);
                    self.$('#signer_activity').toggleClass('has-error', !activity);
                    self.$('#signer_responsable').toggleClass('has-error', !responsable);

                    self.$('#signer_productos_expone').toggleClass('has-error', !productos_expone);
                }
                self.$('#signer').toggleClass('has-error', !signer_name);
                self.$('#signer_pin').toggleClass('has-error', !signer_pin);
                if(!signer_pin || ! signer_name || (active_more_fields && (!fiscal_name || !comercial_name || !email || !phone || !adress 
                    || !city || !postal_code || !province || !activity || !responsable || !productos_expone))){
                    setTimeout(function () {
                        //$('button[type="submit"], a.a-submit').removeAttr('data-loading-text').button('reset');
                        $('button[type="submit"], a.a-submit').button('reset');
                    },1000);
                    return false;
                }
                $confirm_btn.prepend('<i class="fa fa-spinner fa-spin"></i> ');
                $confirm_btn.attr('disabled', true);
                ajax.jsonRpc("/perso_signature_pin/accept/", 'call', {
                    'order_id': order_id,
                    'token': token,
                    'signer': signer_name,
                    'signer_pin': signer_pin,
                    'fiscal_name': fiscal_name,
                    'comercial_name': comercial_name,
                    'frontis': frontis,
                    //'enterprise_name': enterprise_name,
                    'adress': adress,
                    'apartado_correos': apartado_correos,
                    'city': city,
                    'postal_code': postal_code,
                    'province': province,
                    'web_site': web_site,
                    'email': email,
                    'phone': phone,
                    'phone2': phone2,
                    'fax': fax,
                    'activity': activity,
                    'responsable': responsable,
                    'productos_expone': productos_expone,
                }).then(function (data) {   
                    console.log("---------_DATA_____________"+data)                 
                    if(data == -1){
                        var message_id = 4;
                        //self.$el.modal('hide');
                        window.location.href = '/my/orders/'+order_id.toString()+'?access_token='+token+'&message='+message_id;
                    }else if(data == -2){
                        //var message_id = _t('The PIN is wrong, please insert the correct PIN or click up to resent it again');
                        var message_id = _t('PIN incorrecto, por favor inserta el PIN adecuado o usa la opción de reenviar PIN de nuevo');
                        var error = document.getElementById("error_pin");
                        if( error == null){
                            $(".warningmes").after('<p id="error_pin" style="color: red; background-color: #E0E0E0; padding: 10px; border-radius: 5px; margin-top: 10px; margin-bottom: 10px;"><b>'+message_id+'</b></p>');
                        }
                        setTimeout(function () {
                            $confirm_btn.attr('disabled', false);
                            $('#pin').val("");
                            $('i.fa-spinner').remove();
                        }, 1000);
                        return false;                   
                    }else if(data == 2){
                        $('#modalconfirm').hide();
                        window.location.href = '/my/orders/'+order_id.toString()+'?access_token='+token+'&message=2';
                        $('#modalaccept').show();
                    }else{
                        var message_id = 3;
                        self.$el.modal('hide');
                        window.location.href = '/my/orders/'+order_id.toString()+'?access_token='+token+'&message='+message_id;
                    }                  
                });
                return false;
            }
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         * @returns {Deferred}
         */
        _loadTemplates: function () {
            return ajax.loadXML('/perso_signature_pin/static/src/xml/portal_signature_pin.xml', qweb);
        },
    });

    var SignaturePinButton = Widget.extend({
        template: 'perso_signature_pin.boton_email',
        events: {
            'click #boton_pin': 'initProcess',
        },

        init: function(parent, options) {
            this._super.apply(this, arguments);
            this.options = _.extend(options || {}, {
                csrf_token: odoo.csrf_token,
            });
        },

        willStart: function() {
            return this._loadTemplates();
        },

        start: function() {
            this.initSign();
        },

        // Signature
        initSign: function () {
            console.log("INIT EMAIL");
        },
        initProcess: function(ev){
            if(emailSent == 0){
                var self = this;
                //var href = this.$el.attr("href");
                var href = window.location.href;
                if (href) {
                    //var action = href.match(/orders\/([a-z]+)/)[1];
                    var order_id = parseInt(href.match(/orders\/([0-9]+)/)[1]);
                    //var token = href.match(/token=(.*)&/)[1];
                    var token = href.match(/access_token=(.*)&/);
                    if (token != null){
                        token = token[1];
                    }
                    else{
                        token = href.match(/access_token=(.*)/)[1];
                    }
                }
                else {
                    var action = 'accept';
                    var order_id = self.$el.find('form').data("order-id");
                    var token = self.$el.find('form').data("token");
                }
                ajax.jsonRpc("/perso_signature_pin/generate_signature_pin/", 'call', {
                    'order_id': order_id,
                    'token': token,
                }).then(function (data) {
                    emailSent = 9999999;
                });
            }            
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         * @returns {Deferred}
         */
        _loadTemplates: function () {
            return ajax.loadXML('/perso_signature_pin/static/src/xml/portal_signature_pin.xml', qweb);
        },
    });

    var SignaturePinResentEmail = Widget.extend({
        template: 'perso_signature_pin.resent_email',
        events: {
            'click #resent': 'resent_email',
        },

        init: function(parent, options) {
            this._super.apply(this, arguments);
            this.options = _.extend(options || {}, {
                csrf_token: odoo.csrf_token,
            });
        },

        willStart: function() {
            return this._loadTemplates();
        },

        start: function() {
            this.initSign();
        },

        // Signature
        initSign: function () {
            console.log("RESENT EMAIL");
        },
        resent_email: function(ev){
            var self = this;
            var href = window.location.href;
            if (href) {
                //var action = href.match(/orders\/([a-z]+)/)[1];
                var order_id = parseInt(href.match(/orders\/([0-9]+)/)[1]);
                //var token = href.match(/token=(.*)&/)[1];
                var token = href.match(/access_token=(.*)&/);
                if (token != null){
                    token = token[1];
                }
                else{
                    token = href.match(/access_token=(.*)/)[1];
                }
            }
            else {
                var action = 'accept';
                var order_id = self.$el.find('form').data("order-id");
                var token = self.$el.find('form').data("token");
            }
            ajax.jsonRpc("/perso_signature_pin/generate_signature_pin/", 'call', {
                'order_id': order_id,
                'token': token,
            }).then(function (data) {
                $("#warmess").after("<span style='color: green;'> <b>Email enviado</b></span>");
            });
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         * @returns {Deferred}
         */
        _loadTemplates: function () {
            return ajax.loadXML('/perso_signature_pin/static/src/xml/portal_signature_pin.xml', qweb);
        },
    });

    base.ready().then(function () {
        $('#modalconfirm').each(function () {
            var $elem = $(this);
            var form = new SignaturePinForm(null, $elem.data());
            $elem.html("");
            form.appendTo($elem);
        });

    });

    base.ready().then(function () {
        $('#boton_pin').each(function () {
            var $elem = $(this);
            var button = new SignaturePinButton(null, $elem.data());
            button.insertAfter($elem);
            $elem.hide();
        });

    });

    base.ready().then(function () {
        $('#resent').each(function () {
            var $elem = $(this);
            var resent = new SignaturePinResentEmail(null, $elem.data());
            resent.insertAfter($elem);
            $elem.hide();
        });

    });

    return {
        SignaturePinForm: SignaturePinForm,
        SignaturePinButton: SignaturePinButton,
        SignaturePinResentEmail: SignaturePinResentEmail,
    };
});
