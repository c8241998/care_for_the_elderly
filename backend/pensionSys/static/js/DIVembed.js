function loadPage (containerId , filePath , cb) {
    if(typeof window.$ === 'undefined' || window.$ == null) throw "请先引入jq";
    $.ajax({
        url: filePath ,
        type:'GET',
        dataType:'html',
        success:function (data) {
            $(containerId).html(data);
            if(cb) {cb();}
        }
    })
}