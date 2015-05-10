//search
$("#searchtrigger").click(function(e){
    var keyword = $("#searchquery").val();    
    if (keyword) {
        e.preventDefault();
        $.get('/plugin/search?keyWord='+keyword, function(data) {
            var plugins = data;
            var grid = $("#plugins ul.surveys");
            grid.html("");
            if (plugins.plugins.length == 0) {
                grid.append('<li class="col-md-12"><div class="panel panel-primary no-plugins"><h3>No plugins found</h3></div></li>');
            }else{
                $.each(plugins, function() {
                    var id = $(this)[0].pluginId;
                    var name = $(this)[0].name;
                    var version = $(this)[0].version.major+"."+$(this)[0].version.minor;
                    var description = "No plugin description";
                    var prop = $(this)[0].properties;
                    $.each(prop, function() {
                        var nameProp = $(this)[0].name;
                        if (nameProp == "OfxPropPluginDescription") {
                            var descProp = $(this)[0].value[0];
                            description = descProp;
                        };
                    });
                    grid.append('<li class="col-md-3"><div class="panel panel-primary"> <a href="/plugin/'+id+'"><div class="plugins-titles"><img src="static/images/logoPad.png" alt="" class="img-responsive plugin-thumbnail"><h3 class="panel-title">'+name+' '+version+'</h3></div></a><div class="plugins-infos"><p>'+description+'</p></div></div></li>');
                });
            };
        });
    };
    
});