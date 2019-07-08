odoo.define('module_passwords.passwords', function (require) {
"use strict";


var core = require('web.core');
//var Model = require('web.DataModel'); For odoo v10
var rpc = require('web.rpc'); // For odoo v11

var QWeb = core.qweb;
var _t = core._t;
var out = 1; 

function checkHandler()
{
    if($('.password_class').hasClass( 'o_form_readonly' ))
    {
        if(out == 1)
        {
            $('.password_class input.compute_key_editable').val("");
            $('.password_class span.compute_password').empty();
            out = 0; 
        }
        if($('.password_class input.compute_key_editable').length == false)
        {
            $('<input class="compute_key_editable o_form_input o_form_field" type="text" id="compute_password">').insertAfter('.password_class span.compute_key');
            $('.password_class input.compute_key_editable').change(function()
            {
                var key = $('.password_class input.compute_key_editable').val();
                var val = $('.password_class span.password').text();
                /*
                For odoo v10
                new Model("res.partner.passwords")
                .call( "decrypt_aes", ['1', key, val])
                    .then(function (result) {
                        // do something with result   
                        //console.log(result);
                        $('.password_class span.compute_password').html(result);                        
                        $('.password_class span.compute_password').removeClass("o_form_field_empty");
                    });
                */
                // For odoo v11
                rpc.query({
                    model: 'res.partner.passwords',
                    method: 'decrypt_aes',
                    args: ['1',key,val]
                }).then(function (result) {
                        // do something with result
                        $('.password_class span.compute_password').html(result);                        
                        //$('.password_class span.compute_password').removeClass("o_field_empty");
                        $('.password_class span.clipboard_password').html('<span class="copy_text">'+result+'</span><button class="btn btn-sm btn-primary o_clipboard_button o_btn_char_copy" data-original-title="" title=""><span class="fa fa-clipboard"></span><span> Copiar texto</span></button>');                        
                        $('.password_class span.clipboard_password').removeClass("o_field_empty");

                        $('.o_clipboard_button').click(function(){
                            var $temp = $("<input>");
                            $("body").append($temp);
                            $temp.val($('.password_class span.clipboard_password .copy_text').text()).select();
                            document.execCommand("copy");
                            $temp.remove();
                        });
                    });
            });
        }
    }else if($('.password_class').hasClass('o_form_editable'))
    {
        if(out == 1)
        {
            $('.password_class input.compute_key_editable').val("");
            $('.password_class span.compute_password').empty();
            out = 0; 
        }
       if($('.password_class input.compute_key_editable').length)
        {
            $('.password_class input.compute_key_editable').remove();
        }
        if($('.password_class input.compute_key').val().length > 0)
        {
            $('.password_class input.compute_password').prop("disabled", false);
        }else
        {
            $('.password_class input.compute_password').prop("disabled", true);
        }
    }else
    {
        if(out == 0) {out = 1};       
    }
}

setInterval(function()
{
    if($('.password_class') !== undefined)
    {
        checkHandler();
    }
    
}, 100); 

});
