$(function () {
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this)
        var dialog = $("#banner-dialog");
        var nameInput = $("input[name='name']");
        var imageInput = $("input[name='image_url']");
        var linkInput = $("input[name='link_url']");
        var priorityInput = $("input[name='priority']");
        var submitType = self.attr('data-type');
        var bannerId = self.attr('data-id');


        var name = nameInput.val();
        var image_url = imageInput.val();
        var link_url = linkInput.val();
        var priority = priorityInput.val();

        if (!name || !image_url || !link_url || !priority) {
            myalert.alertInfoToast("请输入完整的轮播图数据！");
            return;
        }

        var url = '';
        if (submitType == 'update') {
            url = '/cms/ubanner/';
        } else {
            url = '/cms/abanner/';
        }

        myajax.post({
            'url': url,
            'data': {
                'name': name,
                'image_url': image_url,
                'link_url': link_url,
                'priority': priority,
                'banner_id': bannerId
            },
            'success': function (data) {
                dialog.modal("hide");
                if (data['code'] == 200) {
                    //重新加载页面
                    window.location.reload();
                } else {
                    myalert.alertInfo(data['message']);
                }
            },
            'fail': function () {
                myalert.alertErrorToast("网络错误！")
            }
        });
    });
});

$(function () {
    $(".edit-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal("show");

        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var image_url = tr.attr('data-image');
        var link_url = tr.attr('data-link');
        var priority = tr.attr('data-priority');

        var nameInput = dialog.find("input[name='name']");
        var imageInput = dialog.find("input[name='image_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='priority']");
        var saveBtn = dialog.find("#save-banner-btn");


        nameInput.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);
        saveBtn.attr("data-type", 'update');
        saveBtn.attr("data-id", tr.attr('data-id'))

    });
});

$(function () {
    $(".delete-banner-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr('data-id');
        myalert.alertConfirm({
            "msg": "您确定要删除这个轮播图吗？",
            "confirmCallback": function () {
                myajax.post({
                    'url': '/cms/dbanner/',
                    'data': {
                        'banner_id': banner_id
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            myalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        });
    });
});

$(function () {
    myqiniu.setUp({
        'domain': 'http://q7ng4sydq.bkt.clouddn.com/',
        'browse_btn': 'upload-btn',
        'uptoken_url': '/c/uptoken/',
        'success': function (up, file, info) {
            var imageInput = $("input[name='image_url']");
            imageInput.val(file.name);
        }
    });
});