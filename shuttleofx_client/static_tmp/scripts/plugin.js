$(document).ready(function () {

    // Display an example image in full size
    function changeFullSizeDisplay (pluginId, imageId) {
        $("#fullSizeDisplay").attr("src", "/plugin/" + pluginId + "/image/" + imageId);
    }

    $(".gallery-preview-img").click(function(event) {

        var pluginId = $(this).parent().find("img").attr("src").split("/plugin/")[1].split("/thumbnail/")[0];
        var imageId = $(this).parent().find("img").attr("src").split("/thumbnail/")[1];

        changeFullSizeDisplay(pluginId, imageId);
    });


    // Set an example image as the default image for the plugin
    function setDefaultImage (pluginId, imageId) {

        $.ajax({
                type: "POST",
                url: "/plugin/" + pluginId + "/defaultImage/" + imageId,
                async: false //avoid an empty data when result is returned.
            }).done(function(){
                // TODO : desactiver le bouton
            })
    }

    // TODO : creer le bouton permettant de changer l image
    $(".set-default-img").click(function(event) {

        var pluginId = $(this).parent().find("img").attr("src").split("/plugin/")[1].split("/thumbnail/")[0];
        var imageId = $(this).parent().find("img").attr("src").split("/thumbnail/")[1];

        setDefaultImage(pluginId, imageId);
    });

});
