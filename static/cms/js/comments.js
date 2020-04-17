$(function () {
    $(".remove-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var comment_id = tr.attr("data-id");
        var remove = parseInt(tr.attr("data-remove"));
        var url = "/cms/manage_comment/";
        if (remove){
            var msg = '评论恢复成功！';
        } else {
            var msg = '评论删除成功！';
        }
        myajax.post({
            'url':url,
            'data':{
                'comment_id':comment_id
            },
            'success':function (data) {
                if(data['code']==200){
                    myalert.alertSuccess(msg);
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else{
                    myalert.alertInfo(data['message']);
                }
            }
        })
    });
});