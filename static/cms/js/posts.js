$(function () {
    $(".highlight-htn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        var highlight = parseInt(tr.attr("data-highlight"));
        var url = "";
        if (highlight){
            url = '/cms/uhpost/';
        } else {
            url = '/cms/hpost/';
        }
        myajax.post({
            'url':url,
            'data':{
                'post_id':post_id
            },
            'success':function (data) {
                if(data['code']==200){
                    myalert.alertSuccess("操作成功");
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