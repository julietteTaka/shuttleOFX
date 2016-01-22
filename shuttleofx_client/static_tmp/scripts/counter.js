var currentUrl = window.location.href;
var decomposedUrl = currentUrl.split("?");

var search ; // keyword in search field
var count = 10; // number of plugin per page default = 10
var skip = 1; // number of current page default = 1
var totalPlugins = $("#totalPlugins").val(); // number of plugins return by the search 

// get parameters in url and put them in count, skip and search
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

// Update cookie with new parameters
cookieManager({"search": search, "count": count, "skip":skip});

// Change number of plugin per page
$('select#pageSize').change(function(){
  count = $('select#pageSize').val();
  maxPage = Math.ceil(totalPlugins/$('select#pageSize').val());
  if (skip > maxPage) {
    skip = maxPage;
  }

  cookieManager({"count": count, "skip": skip});

  if (typeof search == "undefined") {
    window.location.href = "/plugin?count=" + count + "&skip=" + skip;
  }
  else {
    window.location.href = "/plugin?search=" + search + "&count=" + count + "&skip=" + skip;
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

// disable clic on object with class disabled
$("li.disabled a").click(function(e){
  e.preventDefault();
  return;
})
