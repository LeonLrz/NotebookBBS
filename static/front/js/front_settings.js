$(function () {
    myqiniu.setUp({
        'domain': 'http://q7ng4sydq.bkt.clouddn.com/',
        'browse_btn': 'avatar-img',
        'uptoken_url': '/c/uptoken/',
        'success': function (up, file, info) {
            var imgTag = $('#avatar-img');
            imgTag.attr('src',file.name);
        }
    });
});

$(function () {
    var gender_id = $("#gender").attr('user-gender');
    $("#gender").find("option[value="+gender_id+"]").prop("selected",true);
    $("#submit-btn").click(function (evnet) {
        event.preventDefault();
        var username = $('input[name=username]').val();
        var realname = $('input[name=realname]').val();
        var qq = $('input[name=qq]').val();
        var signature = $('#signature-area').val();
        var avatar = $('#avatar-img').attr('src');
        var gender = $("#gender option:selected").val();

        myajax.post({
            'url': '/settings/',
            'data':{
                'username': username,
                'realname': realname,
                'qq': qq,
                'signature': signature,
                'avatar':avatar,
                'gender':gender
            },
            'success': function (data) {
                if(data['code'] == 200){
                    myalert.alertSuccessToast('恭喜！修改成功！');
                }else{
                    myalert.alertInfoToast(data['message']);
                }
            }
        })
    });
});

$(function () {
  $('[data-toggle="change_avatar"]').tooltip();
});