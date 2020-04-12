$(function () {
    $("#captcha-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var email = $("input[name='email']").val();
        if (!email) {
            myalert.alertInfoToast("请输入邮箱");
            return;
        }
        myajax.get({
            'url': '/email_captcha/',
            'data': {
                'email': email,
                'forget':1
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    myalert.alertSuccessToast("邮件发送成功！请注意查收！");
                    self.attr('disabled', 'disabled');
                    var timeCount = 60;
                    var timer = setInterval(function () {
                        timeCount--;
                        self.text(timeCount + "s");
                        if (timeCount <= 0) {
                            self.removeAttr('disabled');
                            clearInterval(timer);
                            self.text("发送验证码");
                        }
                    }, 1000);
                } else {
                    myalert.alertError(data['message']);
                }
            },
            'fail': function (error) {
                myalert.alertNetworkError();
            }
        });
    });
});

$(function () {
    $("#next").click(function (event) {
        event.preventDefault();
        var emailE = $("input[name='email']");
        var captchaE = $("input[name='captcha']");

        var email = emailE.val();
        var captcha = captchaE.val();

        myajax.post({
            'url': '/forgetpwd_chekemail/',
            'data': {
                'email': email,
                'captcha': captcha
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    myalert.alertSuccessToast("邮箱验证成功！");
                //  跳转到修改密码界面
                    var user_id = data['data']['user_id'];
                    window.location = "/findpwd/"+user_id+"/";
                } else {
                    myalert.alertInfo(data['message']);
                }

            },
            'fail': function (error) {
                myalert.alertNetworkError();
            }
        })

    });
});