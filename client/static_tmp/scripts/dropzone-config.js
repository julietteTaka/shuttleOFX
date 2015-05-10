
Dropzone.autoDiscover = false;

var bundleId = undefined;
var myDropzone = undefined;

$("#droparea").hide();
$('#fileSubmit').hide();

$(function(){
    var wofxDropzone = new Dropzone("#droparea", {
        url: "undefinedUrl",
        acceptedFiles: "application/zip, application/x-tar, application/gzip, application/x-gzip",
        maxFilesize: 1024,
        paramName: "file"
    });

    wofxDropzone.options.previewTemplate = '\
        <div class="dz-preview dz-file-preview">\
            <div class="dz-details">\
                <div class="dz-filename"><span data-dz-name></span></div>\
                <div class="dz-size" data-dz-size></div>\
                <img data-dz-thumbnail />\
            </div>\
        <div class="dz-progress"><span class="dz-upload" data-dz-uploadprogress></span></div>\
        <div class="dz-error-message"><span data-dz-errormessage></span></div>\
        </div>';

    $('#fileSubmit').click(function(){
        wofxDropzone.options.headers={"Content-Type": wofxDropzone.files[0].type};
         wofxDropzone.processQueue();
    });

    $('#metaBundle').submit(function(event, bundleId){
      
        bundleName = $("#bundleName").val();
        bundleDescription = $("#bundleDescription").val();
        var userId = $("#createBundle").attr("attr-id");

        $.ajax({
            type : 'POST',
            url : '/bundle',
            dataType: 'json',
            data : {'bundleName' : bundleName, 'bundleDescription' : bundleDescription, 'userId' : userId}
        }).done(function(data, bundleId){
            
            $("#droparea").show();
            $('#fileSubmit').show();
            $("#createBundle").hide();

            bundleId = data.bundleId;
            var bundleURI = "/bundle/"+bundleId+"/archive";
            wofxDropzone.options.url = bundleURI;
        });
        event.preventDefault();
    });
});

