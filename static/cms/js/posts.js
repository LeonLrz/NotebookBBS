$(function () {
    $(".highlight-htn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        var highlight = parseInt(tr.attr("data-highlight"));
        var url = "";
        if (highlight){
            url = '/cms/uhpost/';
            var msg = '取消加精成功！';
        } else {
            url = '/cms/hpost/';
            var msg = '加精成功！';
        }
        myajax.post({
            'url':url,
            'data':{
                'post_id':post_id
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

$(function () {
    $(".remove-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        var remove = parseInt(tr.attr("data-remove"));
        var url = "";
        if (remove){
            url = '/cms/urmpost/';
            var msg = '帖子恢复成功！';
        } else {
            url = '/cms/rmpost/';
            var msg = '帖子删除成功！';
        }
        myajax.post({
            'url':url,
            'data':{
                'post_id':post_id
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