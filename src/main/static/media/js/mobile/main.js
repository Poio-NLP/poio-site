
$('#writetyper').on('pagebeforeshow', function() {
	if (iso == 'None') {
		$.mobile.navigate( "#languages" )
	}
});

$('textarea#prediction').on('focus', function() {
    setTimeout(function(){
         window.scrollTo(0, $('textarea#prediction').offset().top-10);
    }, 0);        
}).on('keyup', function() {
    setTimeout(function() {
         window.scrollTo(0, $('textarea#prediction').offset().top-10);
    }, 0);
});

$("#sendmail").click(function (e) {
    e.stopImmediatePropagation();
    e.preventDefault();

    var link = "mailto:?body=" + $('textarea#prediction').val();
    window.location.href = link;
});

$("#sendsms").click(function (e) {
    e.stopImmediatePropagation();
    e.preventDefault();

    var link = "sms:?body=" + $('textarea#prediction').val();;
    window.location.href = link;
});
