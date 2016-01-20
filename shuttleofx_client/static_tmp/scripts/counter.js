var currentUrl = window.location.href;
var decomposedUrl = currentUrl.split("?");

var count = 10;
var skip = 1;
var totalPlugins = $("#totalPlugins").val();

if (typeof decomposedUrl[1] != "undefined") {
  decomposedUrl = decomposedUrl[1].split("&");
  var params = [];

  for (var i = 0; i < decomposedUrl.length; i++) {
    tmp = decomposedUrl[i].split("=");
    key = tmp[0];
    val = tmp[1];
    params[key] = val;
  };

  if (typeof params["search"] != "undefined") search = params["search"];
  if (typeof params["skip"] != "undefined") skip = params["skip"];
  if (typeof params["count"] != "undefined") count = params["count"];
};

/*if (skip <= 1) {
    $('#previous').addClass('disabled');
}
else if (skip == Math.ceil(totalPlugins/count)) {
  $('#next').addClass('disabled');
}*/

$('select#pageSize').change(function(){
  count = $('select#pageSize').val();
  maxPage = Math.ceil(totalPlugins/$('select#pageSize').val());
  if (skip > maxPage) {
    skip = maxPage;
  }

  alert(totalPlugins+"; "+maxPage+"; "+skip);

  cookieManager({"count": count, "skip": skip});

  if (typeof search == "undefined") {
    window.location.href = "http://localhost/plugin?count=" + count + "&skip=" + skip;
  }
  else {
    window.location.href = "http://localhost/plugin?search=" + search + "&count=" + count + "&skip=" + skip;
  }

/*    if (typeof window.location.href.split("?")[1] != "undefined"){
      url = window.location.href.split("?")[1].split("=")
      if (url[0] == "search") {
      if (typeof url[2] == "undefined") {
         url[1] += "&count";
         url[2] = "10&skip";
      };
         window.location.href = "/plugin?" + url[0] + "=" + url[1] + "=" + count + url[2].substring(2)+"="+skip;
     }
     else if (url[0] == "count") {
         window.location.href = "/plugin?" + url[0] + "=" + count + url[1].substring(2)+"="+skip;
     }
  }
  else  {
      window.location.href = "/plugin?count=" + count + "&skip="+skip;
  };*/

});

/*$('#next a').click(function(event){
  event.preventDefault();
  if (!$("#next").hasClass("disabled")) {
    skip ++;
    cookieManager({"count": count, "skip": skip});
    window.location.href = "/plugin?count=" + count + "&skip=" + skip;
  }
});

$('#previous a').click(function(event){
  event.preventDefault();
  if (!$("#previous").hasClass("disabled")) {
    skip --;
    cookieManager({"count": count, "skip": skip});
    window.location.href = "/plugin?count=" + count + "&skip=" + skip;
  }
});
*/

// Manage User sorting preferences inside cookies 
// count --> number of plugins to be displayed
// skip --> on which page is the user
function cookieManager(value){
  if (!Cookies.get("user_sorting_prefs")) {
      Cookies.set("user_sorting_prefs", value, { expires: 30, path: "/" });
  } else {
    Cookies.set("user_sorting_prefs", value);
  }
}

$("li.disabled a").click(function(e){
  e.preventDefault();
  return;
})
