$(document).ready(function(){
    console.log("f");
    Dropzone.autoDiscover = false;
    
    var bundleId = undefined;
    //var bundleId;
    console.log("START : bundleId : "+bundleId);

    var myDropzone = undefined;
    $("#droparea").hide();
    $('#fileSubmit').hide();

    $(function(){
        var wofxDropzone = new Dropzone("#droparea", {
            url: "undefinedUrl",
            acceptedFiles: "application/zip, application/x-tar, application/gzip, application/x-gzip", //This is a comma separated list of mime types or file extensions.Eg.: image/*,application/pdf,.psd.
            maxFilesize: 1024, // in MB
            paramName: "file" // The name that will be used to transfer the file
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
            console.log("upload to :" + wofxDropzone.options.url);
            console.log(wofxDropzone);

            wofxDropzone.options.headers={"Content-Type": wofxDropzone.files[0].type};
            wofxDropzone.processQueue(); //processes the queue
        });

        $('#createBundle').click(function(event, bundleId){
            
            console.log("submit");
            bundleName = $("#bundleName").val();
            bundleDescription = $("#bundleDescription").val();
            console.log(bundleDescription);

            $.ajax({
                type : 'POST',
                url : '/bundle',
                data : {'bundleName' : bundleName, 'bundleDescription' : bundleDescription}
            }).done(function(data, bundleId){
                
                $("#droparea").show();
                console.log("DROPZONE IS READY, BUNDLEID IS GENERATED !")

                jsonData = JSON.parse(data);
                bundleId = jsonData.b[0].bundleId;
                console.log("MIDDLE : "+bundleId);

                var bundleURI = "/bundle/"+bundleId+"/upload";

                wofxDropzone.options.url = bundleURI;

                $('#fileSubmit').show();
            });

            console.log("END : bundleId : "+bundleId);
            console.log("---------------------------------");
            event.preventDefault();
            return false;
        });
    });
});








/*  var bundleId = undefined;
  var myDropzone = undefined;
  console.log("hello");
  $("#droparea").hide();
  $('#fileSubmit').hide();

  $(function(){
    var wofxDropzone = new Dropzone("#droparea", {
      url: "undefinedUrl",
      acceptedFiles: "application/zip, application/x-tar, application/gzip, application/x-gzip", 
      maxFilesize: 1024,
      paramName: "file"
  } );
  wofxDropzone.autoDiscover = false;
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
    console.log("upload to :" + wofxDropzone.options.url);
    console.log(wofxDropzone);

    wofxDropzone.options.headers={"Content-Type": wofxDropzone.files[0].type};
    wofxDropzone.processQueue();
  });

  $('#metaBundle').submit(function(event, bundleId){
      console.log("submit");
      bundleName = $("#bundleName").val();
      bundleDescription = $("#bundleDescription").val();
      console.log(bundleDescription);

      $.ajax({
          type : 'POST',
          url : '/bundle',
          data : {'bundleName' : bundleName, 'bundleDescription' : bundleDescription}
      }).done(function(data, bundleId){
          $("#droparea").show();
          console.log("DROPZONE IS READY, BUNDLEID IS GENERATED !")

          jsonData = JSON.parse(data);
          bundleId = jsonData.b[0].bundleId;
          console.log("MIDDLE : "+bundleId);

          var bundleURI = "/bundle/"+bundleId+"/upload";

          wofxDropzone.options.url = bundleURI;

          $('#fileSubmit').show();
          // dict[url] = "/file/post";
          // $("div#myId").dropzone(dict);
    });

    console.log("END : bundleId : "+bundleId);
    console.log("---------------------------------");
    event.preventDefault();

  });
});*/
//});