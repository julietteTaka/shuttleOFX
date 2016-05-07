$(document).ready(function () {

    function changeFullSizeDisplay (pluginId, imageId) {
        $("#fullSizeDisplay").attr("src", "/plugin/" + pluginId + "/image/" + imageId);
    }

    $(".gallery-preview-img").click(function(event) {

        var pluginId = $(this).attr("pluginId");
        var imageId = $(this).attr("imageId");

        changeFullSizeDisplay(pluginId, imageId);
    });

});
