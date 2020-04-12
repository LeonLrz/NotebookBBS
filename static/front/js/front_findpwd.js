$(function () {
    $("#submit").click(function (event) {
        // 是为了阻止默认的表单提交事件
        event.preventDefault();

        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");
        var user_id = $("#submit").attr("user-id");

        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();


        //  1.要在模板的meta标签中渲染一个csrf-token
        //  2.在ajax请求的投不用设置X-CSRFtoken
        myajax.post({
            'url':'/findpwd/'+user_id+"/",
            'data':{
                'newpwd':newpwd,
                'newpwd2':newpwd2
            },
            'success':function (data) {
            //    code == 200
                if(data['code'] == 200){
                    myalert.alertSuccess(
                        "密码修改成功！请牢记新密码！",
                        function () {
                            window.location = "/";
                    });
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