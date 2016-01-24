/********************************************
    Categories tree view :
      - Ajax call to get data
      - Generate HTML from data
      - Handle events to expand/minimize
********************************************/
$(document).ready(function() {
    $("#left-nav li#categories a").on('click', function(){
        $(this).toggleClass('active');
        $("#left-nav ul li#categories > ul").slideToggle(300);
    });
    $("#left-nav ul li#categories").on('click', ' ul li i',function(){
        $(this).next('ul').slideToggle(300);
        $(this).toggleClass('fa-minus', 'fa-plus');
    });
});

$.ajax({
    url: '/plugins',
    type: 'GET',
})
.done(function(data) {
    var categoryTree = [];
    var object = {};

    for (var i = 0; i < data.plugins.length; i++) {
        if (data.plugins[i].properties.OfxImageEffectPluginPropGrouping) {
            var group = data.plugins[i].properties.OfxImageEffectPluginPropGrouping.value;
            var splittedPath = group.split("/");

            splittedPath.reduce(function(o, s){
                return o[s] = [];
            }, object);

            // Merge all arrays to create one
            $.extend(true, categoryTree, object);
        }
    }

    var depth = 0;
    var html = generateHtmlFromCategoriesTree(categoryTree, '', depth);
    $('#categories').append(html);
});

function generateHtmlFromCategoriesTree(object, previous, depth){
    var html = '<ul>';

    for (var i = 0; i < Object.keys(object).length; i++) {
        // Do not add a / if it's the root element
        if (depth === 0) {
            previous += '/category?search=' + Object.keys(object)[i];
        } else {
            previous += '/' + Object.keys(object)[i];
        }

        if ($.isEmptyObject(object[Object.keys(object)[i]])) {
            html += '<li><a href="'+ previous + '">' + Object.keys(object)[i];
        } else {
            html += '<li><a href="'+ previous + '">' + Object.keys(object)[i] + '</a> <i class="fa fa-plus"></i>';
            depth++;
            html += generateHtmlFromCategoriesTree(object[Object.keys(object)[i]], previous, depth);
        }

        previous = previous.substring(0, previous.length - Object.keys(object)[i].length - 1);
        html += '</li>';
    }
    html += '</ul>';
    return html;
}
