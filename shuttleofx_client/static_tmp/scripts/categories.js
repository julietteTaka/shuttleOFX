/********************************************
    Categories tree view :
      - Ajax call to get data
      - Generate HTML from data
      - Handle events to expand/minimize
********************************************/
$(document).ready(function() {
    $("#left-nav ul li#categories").on('click', 'ul li i',function(){
        var category = $(this).next('a').text(); // get category name

        $(this).parent().children('ul').slideToggle(300, function(){
            // If the category has been opened
            if($(this).is(':visible')){
                // Update list of opened category
                addOpenCategory(category);
            } else {
                removeOpenCategory(category);
            }
        });

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
    // When all categories are loaded and append,
    // re-open the ones that were opened on the previous page
    autoOpenCategories();
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
            html += '<li><a href="'+ previous + '">' + Object.keys(object)[i] + '</a>';
        } else {
            html += '<li><i class="fa fa-plus"></i><a href="'+ previous + '">' + Object.keys(object)[i] + '</a>';
            depth++;
            html += generateHtmlFromCategoriesTree(object[Object.keys(object)[i]], previous, depth);
        }

        previous = previous.substring(0, previous.length - Object.keys(object)[i].length - 1);
        html += '</li>';
    }
    html += '</ul>';
    return html;
}

function addOpenCategory(categoryName){
    if (!Cookies.get("open_categories")) {
        Cookies.set("open_categories", categoryName, { expires: 1, path: "/" });
    } else {
        Cookies.set("open_categories", Cookies.get("open_categories") + "," + categoryName);
    }
}

function autoOpenCategories(){
    if (Cookies.get("open_categories")) {
        var openedCategories = Cookies.get("open_categories").split(",");
        // Loop through each category and open it, if it's in the array of opened categories
        $("#left-nav ul li#categories ul li").each(function(index) {
            if ( openedCategories.indexOf( $(this).children('a').text() ) > -1) {
                $(this).children('ul').show();
                $(this).children('i').toggleClass('fa-minus', 'fa-plus');
            };
        });
    }
}

function removeOpenCategory(categoryName){
    var openedCategories = Cookies.get("open_categories").split(",");
    var index = openedCategories.indexOf(categoryName);
    if (index > -1) {
        openedCategories.splice(index, 1);
        openedCategories.join()
        Cookies.set("open_categories", openedCategories.join());
    };
}
