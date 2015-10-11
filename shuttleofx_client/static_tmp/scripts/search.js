//search

$(document).ready(function() {
    //console.log("display");
    //display search bar
    $("#searchForm").css({"display":"block"});

    //set image for each plugin

    $( "#plugins ul.surveys li a" ).each(function( index ) {
        var baseUrl = $(this).attr('href');
        var classNames = $($(".plugin-thumbnail").get(index)).attr("class")
        var imagePath = classNames.split(" ")[1]
        if(imagePath != "plugin-thumbnail"){
            $($( ".plugin-thumbnail" ).get(index)).css({
                "background-image": "url("+baseUrl+"/image/" + imagePath + ")",
                "background-size": "cover"
            })
        }
    })
});