$(function () {
    var ue = UE.getEditor('editor', {
        'serverUrl': '/ueditor/upload/',
        "toolbars": [
            [
                'undo', //撤销
                'redo', //重做
                'bold', //加粗
                'italic', //斜体
                'source', //源代码
                'blockquote', //引用
                'selectall', //全选
                'insertcode', //代码语言
                'fontfamily', //字体
                'fontsize', //字号
                'simpleupload', //单图上传
                'emotion' //表情
            ]
        ]
    });
    window.ue = ue;
});


$(function () {
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var post_id = $(this).attr('data-post-id');
        var content = window.ue.getContent();
        var origin_comment_id = $(".origin-comment-group").attr('data-comment-id');

        myajax.post({
            'url': '/acomment/',
            'data': {
                'post_id': post_id,
                'content': content,
                'origin_comment_id': origin_comment_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    myalert.alertSuccessToast('恭喜！回复成功！');
                    setTimeout(function () {
                        window.location = '/p/'+post_id+'/';
                    },500);
                }else{
                    myalert.alertInfo(data['message']);
                }
            }
        })
    });
});
