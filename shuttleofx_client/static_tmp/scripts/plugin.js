$( document ).ready(function() {
    $("#rate").raty({
        click: function(score, evt) {
            $(".thanks").animate({opacity:1});
            var pluginId = $("#rate").attr("attr-pluginId");
            var userId = $("#rate").attr("attr-userId");
            var versionMaj = $("#rate").attr("attr-pluginVersionMajor");
            var versionMin = $("#rate").attr("attr-pluginVersionMinor");
            //send the score
            $.ajax({
                type: "POST",
                url: "/plugin/"+pluginId+"/rate",
                contentType: 'application/json; charset=utf-8',
                data : JSON.stringify({
                    'userId' : userId,
                    'score': score,
                    'version' : [versionMaj, versionMin]
                }),
              })
              .error(function(data) {
                  console.log("error", data);
              })
              .done(function(data){
                location.reload();
              });
            }
    });

    var pluginScore = $("#usersRate").attr("attr-pluginScore");
    $("#usersRate").raty({
      readOnly: true,
      score: pluginScore
    });
});
