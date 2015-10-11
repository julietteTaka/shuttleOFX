$(document).ready(function() {
    var marginTopInput = 30;
    var count = 1;
    var numItemsInput = $('.clip-input').length + 1;
    $('.clip').css( "height", marginTopInput*numItemsInput);
    $('.clip .clip-name').css( "line-height", $('.clip').height() + "px");

    $( ".clip-input" ).each(function( i ) {
        $( this ).css( "marginTop", marginTopInput*count -15);
        count += 1;
    });

    $( ".clip-output" ).each(function( i ) {
        $( this ).css( "marginTop", $('.clip').height()/2 -15);
    });

    $('.clip-input').popover();
    $('.clip-output').popover();
    $('.clip-mask').popover();
});