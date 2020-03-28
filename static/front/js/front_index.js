function getQueryVariable(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return(false);
}

$(function () {
    var a1 = $("#new");
    var a2 = $("#highlight");
    var a3 = $("#thumb");
    var a4 = $("#comment");

    var st = getQueryVariable("st");
    if(st == 2){
        a2.parent().addClass("active");
    }else if(st == 3){
        a3.parent().addClass("active");
    }else if(st == 4){
        a4.parent().addClass("active");
    }else{
        a1.parent().addClass("active");
    }
});