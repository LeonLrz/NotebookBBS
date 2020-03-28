
$(function () {
    $("#submit").click(function (event) {
        // 是为了阻止默认的表单提交事件
        event.preventDefault();

        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        //  1.要在模板的meta标签中渲染一个csrf-token
        //  2.在ajax请求的投不中设置X-CSRFtoken
        myajax.post({
            'url':'/cms/resetpwd/',
            'data':{
                'oldpwd':oldpwd,
                'newpwd':newpwd,
                'newpwd2':newpwd2
            },
            'success':function (data) {
            //    code == 200
                if(data['code'] == 200){
                    myalert.alertSuccessToast("恭喜！密码修改成功！");
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwd2E.val("");
                }else{
                    var message = data['message'];
                    myalert.alertInfo(message);
                }
            //    code != 200
            },
            'fail':function (error) {
                myalert.alertNetworkError();
            }
        });
    });
});