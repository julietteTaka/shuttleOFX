$('select#pageSize').change(function(){
    var size = $('select#pageSize').val();
    $.get('/plugin/count?count='+size, function(data) {
        var plugins = data;
        var grid = $("#plugins ul.surveys");
        grid.html("");
        $.each(plugins.plugins, function(key, val) {
            var id = val.pluginId;
            var name = val.label;
            var description = "No plugin description";
            var prop = val.properties;
            if("OfxPropPluginDescription" in val.properties)
                description = val.properties.OfxPropPluginDescription.value
            grid.append('<li class="col-md-3"><div class="panel panel-primary"> <a href="/plugin/'+id+'"><div class="plugins-titles"><img src="static/images/logoPad.png" alt="" class="img-responsive plugin-thumbnail"><h3 class="panel-title">'+name+'</h3></div></a><div class="plugins-infos"><p>'+description+'</p></div></div></li>');
        });
    });
});
var skip = 0;
if (skip <= 0) {
    $('#previous').addClass('disabled');
};
$('#next a').click(function(){
    $('#previous').removeClass('disabled');
    var size = $('select#pageSize').val();
    skip = skip + parseInt(size); 
    // console.log("skip "+ skip);
    // console.log("size "+ size);
    $.get('/plugin/count?count='+size+'&skip='+skip, function(data) {
        var plugins = data;
        var grid = $("#plugins ul.surveys");
        grid.html("");
        $.each(plugins.plugins, function(key, val) {
            var id = val.pluginId;
            var name = val.label;
            var description = "No plugin description";
            var prop = val.properties;
                if("OfxPropPluginDescription" in val.properties)
                        description = val.properties.OfxPropPluginDescription.value
            grid.append('<li class="col-md-3"><div class="panel panel-primary"> <a href="/plugin/'+id+'"><div class="plugins-titles"><img src="static/images/logoPad.png" alt="" class="img-responsive plugin-thumbnail"><h3 class="panel-title">'+name+'</h3></div></a><div class="plugins-infos"><p>'+description+'</p></div></div></li>');
        });
    });
});
$('#previous a').click(function(){
    var size = $('select#pageSize').val();
    skip = skip - parseInt(size); 
    if (skip <= 0) {
        skip=0;
        $('#previous').addClass('disabled');
    };
    // console.log("skip "+ skip);
    // console.log("size "+ size);
    $.get('/plugin/count?count='+size+'&skip='+skip, function(data) {
        var plugins = data;
        var grid = $("#plugins ul.surveys");
        grid.html("");
        $.each(plugins.plugins, function(key, val) {
            var id = val.pluginId;
            var name = val.label;
            var description = "No plugin description";
            var prop = val.properties;
            if("OfxPropPluginDescription" in val.properties)
                description = val.properties.OfxPropPluginDescription.value
            grid.append('<li class="col-md-3"><div class="panel panel-primary"> <a href="/plugin/'+id+'"><div class="plugins-titles"><img src="static/images/logoPad.png" alt="" class="img-responsive plugin-thumbnail"><h3 class="panel-title">'+name+'</h3></div></a><div class="plugins-infos"><p>'+description+'</p></div></div></li>');
        });
    });
});
