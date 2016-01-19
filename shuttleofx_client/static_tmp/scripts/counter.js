var currentUrl = window.location.href;
var decomposedUrl = currentUrl.split("?");

var skip;
var count;

var totalPlugins = $("#totalPlugins").val();

if (decomposedUrl.length < 2) {
  count = 10;
  skip = 1;
}
else if (decomposedUrl[1].indexOf("&") > -1) {
    // Only if the url contains the character &
    // Avoid a bug on the search page
    decomposedUrl = decomposedUrl[1].split("&");
    count = decomposedUrl[0].split("=")[1];
    skip = decomposedUrl[1].split("=")[1];
}

if (skip <= 1) {
    $('#previous').addClass('disabled');
}
else if (skip == Math.ceil(totalPlugins/count)) {
  $('#next').addClass('disabled');
}

$('select#pageSize').change(function(){
  count = $('select#pageSize').val();
  if (skip > Math.ceil(totalPlugins/$('select#pageSize').val())) {
    skip = Math.ceil(totalPlugins/$('select#pageSize').val());
  }
  cookieManager({"count": count, "skip": skip});
  url = window.location.href.split("?")[1].split("=");
  if (url[0] == "search") {
      window.location.href = "/plugin?" + url[0] + "=" + url[1] + "=" + count + url[2].substring(2)+"="+skip;
  }
  else if (url[0] == "count") {
      window.location.href = "/plugin?" + url[0] + "=" + count + url[1].substring(2)+"="+skip;
  };

});

$('#next a').click(function(event){
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
