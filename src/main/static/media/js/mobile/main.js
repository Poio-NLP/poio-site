
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
