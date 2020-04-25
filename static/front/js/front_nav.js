/* nav.js 主要应用于首页右侧导航栏 */

// 从session中取产品列表
if ($.cookie("products_list")){
	var list = JSON.parse($.cookie("products_list"));
}else{
	var list =[];
	console.log(list);
}

$(function () {
	for (var i = 0; i < list.length;i++) {
		$(".tbar-cart-list").append(
		'<div data-id="'+
			list[i].productID+'" class="tbar-cart-item" ><div class="jtc-item-goods"><span class="p-img"><a href="#"><img src="'+
		list[i].productImg+'" height="50px;" width="66px;" /></a></span><div class="p-name"> <a href="#">'+
		list[i].productTitle+'</a> </div> <div class="p-price"><strong>'+
		list[i].productPrice+'</strong></div><a class="p-del J-del">删除</a></div></div>'
		);
		console.log(list[i].productID,list[i].productImg,list[i].productTitle,list[i].productPrice);
	}
	$('.J-total').text(String(list.length));
	if (list.length > 1) {
		$("#compare").removeAttr('disabled');
		$("#compare").css("pointer-events","auto");
	} else {
		$("#compare").attr("disabled",true);
		$("#compare").css("pointer-events","none");
	}
});


$(function(){
	// 鼠标在商品上添加删除按钮
	$('.tbar-cart-item').hover(function (){
			$(this).find('.p-del').show();
		},
		function(){
			$(this).find('.p-del').hide();
		});

	$('.jth-item').hover(
		function (){ $(this).find('.add-cart-button').show();
		},
		function(){ $(this).find('.add-cart-button').hide();
		});

	// 鼠标悬浮在tab上显示文字
	$('.toolbar-tab').hover(function (){
		$(this).find('.tab-text').addClass("tbar-tab-hover");
		$(this).find('.footer-tab-text').addClass("tbar-tab-footer-hover");
		$(this).addClass("tbar-tab-selected");
		},
		function(){
			$(this).find('.tab-text').removeClass("tbar-tab-hover");
			$(this).find('.footer-tab-text').removeClass("tbar-tab-footer-hover");
			$(this).removeClass("tbar-tab-selected");
		});

	// 点击对比栏图标，显示要对比的内容
	$('.tbar-tab-cart').click(function (){
		if($('.toolbar-wrap').hasClass('toolbar-open')){
			if($(this).find('.tab-text').length > 0){
				$(this).addClass('tbar-tab-click-selected');
				$(this).find('.tab-text').remove();
				$('.tbar-panel-cart').css({'visibility':"visible","z-index":"1"});

			}else{
				var info = "<em class='tab-text '>对比栏</em>";
				$('.toolbar-wrap').removeClass('toolbar-open');
				$(this).append(info);
				$(this).removeClass('tbar-tab-click-selected');
				$('.tbar-panel-cart').css({'visibility':"hidden","z-index":"-1"});
			}
		}else{
			$(this).addClass('tbar-tab-click-selected');
			$(this).find('.tab-text').remove();
			$('.tbar-panel-cart').css({'visibility':"visible","z-index":"1"});
			$('.toolbar-wrap').addClass('toolbar-open');
		}
	});

	// 关闭对比栏
	$(".close-panel").click(function () {
		$('.toolbar-wrap').removeClass('toolbar-open');
	});

	// 添加到对比栏
	$(".add-to-compare").click(function (event) {
		event.preventDefault();
		var product = $(this).parents(".product--item");
		var productID = product.attr("data-id");
		//判断是否已经在列表中
		var inArray = -1;
		for (var i = 0; i < list.length;i++) {
			if (list[i].productID == productID){
				inArray = 1;
				myalert.alertInfoToast("该产品已在对比栏~")
			}
		}
		if(inArray < 0){
			// 最多对比5个
			if(list.length > 7){
				myalert.alertInfoToast("最多可对比8个产品~")
			}
			if(list.length < 8){
				var productImg = product.attr("data-img");
				var productTitle = product.attr("data-title");
				var productPrice = product.attr("data-price");
				var product = {
					"productID":productID,
					"productImg":productImg,
					"productTitle":productTitle,
					"productPrice":productPrice
				};
				$(".tbar-cart-list").append(
					'<div data-id="'+
					productID+'"class="tbar-cart-item" ><div class="jtc-item-goods"><span class="p-img"><a href="#"><img src="'+
					productImg+'" height="50px;" width="66px;" /></a></span><div class="p-name"> <a href="">'+
					productTitle+'</a> </div> <div class="p-price"><strong>'+
					productPrice+'</strong></div><a class="p-del J-del">删除</a></div></div>'
				);
				list.push(product);
				$.cookie(
                    "products_list",
                    JSON.stringify(list),
					{path: '/' }
                    );
                    //将数组转换为Json字符串保存在cookie中
				$('.J-total').text(String(list.length));
			}

		}

		// 对比按钮
        if (list.length > 1) {
            $("#compare").removeAttr('disabled');
            $("#compare").css("pointer-events","auto");
        } else {
            $("#compare").attr("disabled",true);
            $("#compare").css("pointer-events","none");
        }
		$('.tbar-tab-cart').find('.tab-text').remove();
		$('.tbar-panel-cart').css({'visibility':"visible","z-index":"1"});
		$('.toolbar-wrap').addClass('toolbar-open');
	});


});

$(function () {
    //	从对比栏移除
    $(".p-del").click(function (event){
        var product = $(this).parents(".tbar-cart-item");
        var pid = product.attr("data-id");
        console.log(product,pid);
        product.remove();
        for (var i = 0; i < list.length;i++){
            console.log(list[i].productID,pid);
            if( list[i].productID == pid ){
                list.splice(i,1);
            }
        }
        $.cookie(
            "products_list",
            JSON.stringify(list),
            {path: '/' }
            );
            //将数组转换为Json字符串保存在cookie中
        $('.J-total').text(String(list.length));
            // 对比按钮
        if (list.length > 1) {
            $("#compare").removeAttr('disabled');
            $("#compare").css("pointer-events","auto");
        } else {
            $("#compare").attr("disabled",true);
            $("#compare").css("pointer-events","none");
        }
    });
});