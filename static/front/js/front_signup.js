$(function () {
    $("#captcha-img").click(function (event) {
       var self = $(this);
       var src = self.attr('src');
       var newsrc = myparam.setParam(src,'xx',Math.random());
       self.attr('src',newsrc);
    });
});

// $(function () {
//     $("#sms-captcha-btn").click(function (event) {
//         event.preventDefault();
//         var self = $(this);
//         var telephone = $("input[name='telephone']").val();
//         if(!(/^1[345789]\d{9}$/.test(telephone))){
//             myalert.alertInfoToast("请输入正确的手机号码");
//             return;
//         };
//         var timestamp = (new Date).getTime();
//         var salt =  'suibiangei!@#$asdzx132%';
//         var sign = md5(timestamp+telephone+salt);
//
//         myajax.post({
//            'url':'/c/sms_captcha/',
//             'data':{
//                 'telephone':telephone,
//                 'timestamp':timestamp,
//                 'sign':sign
//             },
//            'success':function (data) {
//                if (data['code'] ==200){
//                    myalert.alertSuccessToast("验证码发送成功！");
//                    self.attr('disabled','disabled');
//                    var timeCount = 60;
//                    var timer = setInterval(function () {
//                        timeCount--;
//                        self.text(timeCount+"s");
//                        if(timeCount <=0){
//                            self.removeAttr('disabled');
//                            clearInterval(timer);
//                            self.text("发送验证码");
//                        }
//                    },1000);
//                }else {
//                    myalert.alertError(data['message']);
//                }
//            }
//         });
//     });
// });

$(function () {
;var encode_version = 'sojson.v5', ezbla = '__0x758c2',  __0x758c2=['B8O7wpI=','LV1YbMOCI8KOwok=','woQVNVVG','wqMKOTLCrQ==','WcK2fm1kw7jCvsKtw4YU','XGtywrU=','I8OFw7IGwp9+MsKYwrjCg8ObVjzDv8KnwrLCog==','6aik6KyO56Kc5Y+x6YCm5oi85YuW7723','WXYDwo4=','w7jDtsO1wqI+','ZMO8w5hpVg==','5Y2r6YGe6aqo6K2X56GP','wpbDucOxw6fDtA==','wp4Mw53CkxE=','w5nDkcOBwqc9wqdNFSEV','VsKcw54l','wrQyHMK7R8OTKMKYccKA','UMKpw5IQEQ==','w5zDiUFIKTnCtQ==','SDjDh2fChw==','OsO9w40=','woPDoMKh','w6LCp8Kpwo4pZUtlw7bDlX8TwpjCpA==','6K2f6Lyy5YWz5q2Z56Ka55uh5oqi5p6V5Yyy56CJ','Q8Obw7l3','w5A8MDhX','wqAWIFFA','XcOOw4nDpC7CpHNKwpfCkcKTw71IwpLCoMKWwo3DljF1wrkmVA==','wrvCrxg=','w47DglF5Jj3CvhzCnw==','woPDkMKlScKg','5Li86IO15YmU6ZmNasOTRsK3AzXCtcKUw44=','AcKKw4sicWlfQDxaQMKjw63CuhZ3','B8OCwrR/G8Ohw51AQkA2IVkyU0DDvQ==','wrzDj8KKbgkdOzvCrlo5Y2kqwp0=','NlQOZBo1w4nDn8KqCX4hw4s0wqPCqMO0NMOkK8K5T0g=','5Y+z6YO46aiq6K6Q56Gd','QFEwSlg=','w7YXAQl2I2nCi8Knw6LCng0ZLA==','w6jDu8OV'];(function(_0x231fd0,_0x4f680a){var _0x5b4826=function(_0x4a3682){while(--_0x4a3682){_0x231fd0['push'](_0x231fd0['shift']());}};_0x5b4826(++_0x4f680a);}(__0x758c2,0x188));var _0x2136=function(_0x1b5f37,_0x3043ff){_0x1b5f37=_0x1b5f37-0x0;var _0x9cbf9b=__0x758c2[_0x1b5f37];if(_0x2136['initialized']===undefined){(function(){var _0x536c65=typeof window!=='undefined'?window:typeof process==='object'&&typeof require==='function'&&typeof global==='object'?global:this;var _0x1a5b8f='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';_0x536c65['atob']||(_0x536c65['atob']=function(_0x5b3a83){var _0x14a71a=String(_0x5b3a83)['replace'](/=+$/,'');for(var _0x45d7e9=0x0,_0x408681,_0x4c050b,_0xe74253=0x0,_0x5e77f8='';_0x4c050b=_0x14a71a['charAt'](_0xe74253++);~_0x4c050b&&(_0x408681=_0x45d7e9%0x4?_0x408681*0x40+_0x4c050b:_0x4c050b,_0x45d7e9++%0x4)?_0x5e77f8+=String['fromCharCode'](0xff&_0x408681>>(-0x2*_0x45d7e9&0x6)):0x0){_0x4c050b=_0x1a5b8f['indexOf'](_0x4c050b);}return _0x5e77f8;});}());var _0x41e81c=function(_0x2312ef,_0x28f682){var _0x4522fc=[],_0x45cfba=0x0,_0x243bb5,_0xe66655='',_0x53a692='';_0x2312ef=atob(_0x2312ef);for(var _0x5a9577=0x0,_0x40ca2c=_0x2312ef['length'];_0x5a9577<_0x40ca2c;_0x5a9577++){_0x53a692+='%'+('00'+_0x2312ef['charCodeAt'](_0x5a9577)['toString'](0x10))['slice'](-0x2);}_0x2312ef=decodeURIComponent(_0x53a692);for(var _0x295106=0x0;_0x295106<0x100;_0x295106++){_0x4522fc[_0x295106]=_0x295106;}for(_0x295106=0x0;_0x295106<0x100;_0x295106++){_0x45cfba=(_0x45cfba+_0x4522fc[_0x295106]+_0x28f682['charCodeAt'](_0x295106%_0x28f682['length']))%0x100;_0x243bb5=_0x4522fc[_0x295106];_0x4522fc[_0x295106]=_0x4522fc[_0x45cfba];_0x4522fc[_0x45cfba]=_0x243bb5;}_0x295106=0x0;_0x45cfba=0x0;for(var _0x539026=0x0;_0x539026<_0x2312ef['length'];_0x539026++){_0x295106=(_0x295106+0x1)%0x100;_0x45cfba=(_0x45cfba+_0x4522fc[_0x295106])%0x100;_0x243bb5=_0x4522fc[_0x295106];_0x4522fc[_0x295106]=_0x4522fc[_0x45cfba];_0x4522fc[_0x45cfba]=_0x243bb5;_0xe66655+=String['fromCharCode'](_0x2312ef['charCodeAt'](_0x539026)^_0x4522fc[(_0x4522fc[_0x295106]+_0x4522fc[_0x45cfba])%0x100]);}return _0xe66655;};_0x2136['rc4']=_0x41e81c;_0x2136['data']={};_0x2136['initialized']=!![];}var _0x14fd02=_0x2136['data'][_0x1b5f37];if(_0x14fd02===undefined){if(_0x2136['once']===undefined){_0x2136['once']=!![];}_0x9cbf9b=_0x2136['rc4'](_0x9cbf9b,_0x3043ff);_0x2136['data'][_0x1b5f37]=_0x9cbf9b;}else{_0x9cbf9b=_0x14fd02;}return _0x9cbf9b;};$(_0x2136('0x0','gHrn'))['click'](function(_0x52e170){var _0x28c87f={'qYDcA':_0x2136('0x1','^5DI'),'Ccgtk':_0x2136('0x2','A22W'),'WjiZz':_0x2136('0x3','MM$X'),'lLKCn':function _0x2d2604(_0x337a3b,_0x4546d2){return _0x337a3b(_0x4546d2);},'GfgIV':function _0x731495(_0x14faef,_0x248da9){return _0x14faef(_0x248da9);},'lvAsQ':function _0x4dd389(_0x51da0f,_0x1db165){return _0x51da0f+_0x1db165;},'sMmKD':'disabled','FkTKs':function _0x33bf9f(_0x5b93d1,_0xfbdb16){return _0x5b93d1(_0xfbdb16);},'VYTGD':_0x2136('0x4','gHrn')};var _0x39b92a=_0x28c87f[_0x2136('0x5','uYxO')]['split']('|'),_0x21f09f=0x0;while(!![]){switch(_0x39b92a[_0x21f09f++]){case'0':_0x52e170[_0x2136('0x6','K$32')]();continue;case'1':myajax['post']({'url':_0x28c87f['Ccgtk'],'data':{'telephone':_0x48463e,'timestamp':_0x37b136,'sign':_0xe6bb9b},'success':function(_0x117431){var _0x1ae4f9={'bhAOu':_0x2136('0x7','(V68'),'vYZPV':_0x2136('0x8','m6^$'),'rPtAM':'message','SBYju':_0x2136('0x9','YLj#'),'SCiNM':function _0x5561e4(_0x2df87e,_0x57baf6,_0x44e584){return _0x2df87e(_0x57baf6,_0x44e584);}};if(_0x1ae4f9[_0x2136('0xa','rtqq')]===_0x1ae4f9[_0x2136('0xb','c]k4')]){myalert[_0x2136('0xc','qAG&')](_0x117431[_0x1ae4f9['rPtAM']]);}else{if(_0x117431[_0x2136('0xd','Gs*@')]==0xc8){myalert[_0x2136('0xe','TD^j')](_0x2136('0xf','[sca'));_0x2bec0f[_0x2136('0x10','8J#3')](_0x1ae4f9[_0x2136('0x11','(V68')],_0x1ae4f9[_0x2136('0x12','^5DI')]);var _0x183e47=0x3c;var _0x155975=_0x1ae4f9['SCiNM'](setInterval,function(){var _0x5649d0={'xlMUd':function _0x270a9d(_0x3d0a51,_0x442352){return _0x3d0a51+_0x442352;},'AdpsC':function _0x50e1be(_0x355ae2,_0x481cc4){return _0x355ae2<=_0x481cc4;},'rxRJq':_0x2136('0x13','96IV')};_0x183e47--;_0x2bec0f['text'](_0x5649d0[_0x2136('0x14','AP7)')](_0x183e47,'s'));if(_0x5649d0[_0x2136('0x15','OufD')](_0x183e47,0x0)){_0x2bec0f[_0x2136('0x16','(V68')]('disabled');clearInterval(_0x155975);_0x2bec0f[_0x2136('0x17','gHrn')](_0x5649d0['rxRJq']);}},0x3e8);}else{myalert[_0x2136('0x18','f1tc')](_0x117431[_0x1ae4f9[_0x2136('0x19','gHrn')]]);}}}});continue;case'2':var _0x37b136=new Date()[_0x2136('0x1a','xSP)')]();continue;case'3':;continue;case'4':var _0x2103b8=_0x28c87f['WjiZz'];continue;case'5':var _0x2bec0f=_0x28c87f['lLKCn']($,this);continue;case'6':var _0xe6bb9b=_0x28c87f[_0x2136('0x1b','D$L^')](md5,_0x28c87f['lvAsQ'](_0x37b136+_0x48463e,_0x2103b8));continue;case'7':if(!/^1[345789]\d{9}$/['test'](_0x48463e)){if(_0x2136('0x1c','TD^j')===_0x2136('0x1d','pXFW')){myalert[_0x2136('0x1e','vv2J')](_0x2136('0x1f','GVB3'));return;}else{_0x2bec0f['removeAttr'](_0x28c87f['sMmKD']);_0x28c87f['FkTKs'](clearInterval,timer);_0x2bec0f[_0x2136('0x20','^5DI')](_0x28c87f[_0x2136('0x21','K$32')]);}}continue;case'8':var _0x48463e=_0x28c87f[_0x2136('0x22','rtqq')]($,_0x2136('0x23','(ynv'))[_0x2136('0x24','win1')]();continue;}break;}});;if(!(typeof encode_version!==_0x2136('0x25','xSP)')&&encode_version==='sojson.v5')){window[_0x2136('0x26','CGmA')](_0x2136('0x27','uYxO'));};encode_version = 'sojson.v5';
});

$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var telephone_input = $("input[name='telephone']");
        var sms_captcha_input = $("input[name='sms_captcha']");
        var username_input = $("input[name='username']");
        var password1_input = $("input[name='password1']");
        var password2_input = $("input[name='password2']");
        var graph_captcha_input = $("input[name='graph_captcha']");

        var telephone = telephone_input.val();
        var sms_captcha = sms_captcha_input.val();
        var username = username_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();
        var graph_captcha = graph_captcha_input.val();

        myajax.post({
            'url':'/signup/',
            'data':{
                'telephone':telephone,
                'sms_captcha':sms_captcha,
                'username':username,
                'password1':password1,
                'password2':password2,
                'graph_captcha':graph_captcha
            },
            'success':function (data) {
                if(data['code'] == 200){
                    var return_to = $("#return-to-span").text();
                    if (return_to) {
                        window.location = return_to;
                    }else {
                        window.location='/';
                    }
                }else {
                    myalert.alertInfo(data['message']);
                }
            },
            'fail':function () {
                myalert.alertNetworkError();
            }
        })
    });
});

$(function () {
  $('[data-toggle="re_captcha"]').tooltip();
  $('[data-toggle="send_captcha"]').tooltip();
});