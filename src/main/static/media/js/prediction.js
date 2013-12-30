
///////////////////////////////// Text input post-processing

function normalizeText() {
  cursorPos = getCaretPosition(document.getElementById('prediction')); // Doesn't work with jQuery
  lastChar = $('textarea#prediction').val().charAt(cursorPos - 1);
  charAt2 = $('textarea#prediction').val().charAt(cursorPos - 2);
  textLenght = $('textarea#prediction').val().length;

  if (cursorPos == 1) { // Capitalize first letter of the text box
    newChar = $('textarea#prediction').val().charAt(0).toUpperCase();
    newText = newChar + $('textarea#prediction').val().substr(1, textLenght - 1);
    $('textarea#prediction').val(newText);
    setCaretPosition(document.getElementById('prediction'), cursorPos);
  }

  if (charAt2 == " ") { // Capitalize first letter after punctuation
    charAt3 = $('textarea#prediction').val().charAt(cursorPos - 3);
    if (  (charAt3 == "." ) ||
          (charAt3 == "!" ) ||
          (charAt3 == "?" ) ) {
      prevText = $('textarea#prediction').val();
      newChar = lastChar.toUpperCase();
      newText = prevText.substr(0, cursorPos - 1) + newChar + prevText.substr(cursorPos, textLenght - 1);
      $('textarea#prediction').val(newText);
      setCaretPosition(document.getElementById('prediction'), cursorPos);
    }
  }

  if ( ((lastChar == ".") || // Remove space before punctuation
        (lastChar == ",") ||
        (lastChar == ";") ||
        (lastChar == ":") ||
        (lastChar == "!") ||
        (lastChar == "?")) &&
        (charAt2 == " ")  ) {
    prevText = $('textarea#prediction').val();
    newText = prevText.substr(0, cursorPos - 2) + lastChar + " " + prevText.substr(cursorPos, textLenght - 1);
    $('textarea#prediction').val(newText);
    setCaretPosition(document.getElementById('prediction'), cursorPos);
  };

}

///////////////////////////////////////////////// API calls

function getPredictions(iso) {
  var iso;

  if ($('select#language_chooser').length > 0)
    iso = $('select#language_chooser').val();
  else
    iso = window.iso;

  $.getJSON($SCRIPT_ROOT + '/api/prediction', {

    text: $('textarea#prediction').val(),
    iso : iso,
    token : $TOKEN
    
    }, function(data) {
    
      var length = data.length, element = null;
      for (var i = 0; i < length; i++) {
        element = data[i];
        $("#predict-" + i).text(element)

      }
    }
  );
}

///////////////////////////////////////////////// Helpers

function getCaretPosition (ctrl) {
  var CaretPos = 0;
  // IE Support
  if (document.selection) {
    ctrl.focus ();
    var Sel = document.selection.createRange ();
    Sel.moveStart ('character', -ctrl.value.length);
    CaretPos = Sel.text.length;
  }
  // Firefox and most others support 
  else if (ctrl.selectionStart || ctrl.selectionStart == '0')
    CaretPos = ctrl.selectionStart;
  return (CaretPos);
}

function setCaretPosition(ctrl, pos){
  if(ctrl.setSelectionRange)
  {
    ctrl.focus();
    ctrl.setSelectionRange(pos,pos);
  }
  else if (ctrl.createTextRange) {
    var range = ctrl.createTextRange();
    range.collapse(true);
    range.moveEnd('character', pos);
    range.moveStart('character', pos);
    range.select();
  }
}

function addText(text) {
  prevText = $('textarea#prediction').val();
  newText = prevText.substr(0, prevText.lastIndexOf(" "));
  if (prevText.lastIndexOf(" ") != -1) { newText += " ";}; // Don't add a space in the begining
  newText += text;
  newText += " ";
  $('textarea#prediction').val(newText);  
}

////////////////////////////////////////////// Prediction

$('textarea#prediction').bind('input focus', function() {
  getPredictions();
  normalizeText();
  return false;
});

$( 'textarea#prediction' ).keydown(function(evt) {
  var charCode = (evt.which) ? evt.which : event.keyCode
  if (( charCode == 112 ) ||
      ( charCode == 113 ) ||
      ( charCode == 114 ) ||
      ( charCode == 115 ) ||
      ( charCode == 116 ) ||
      ( charCode == 117 ) ) {
    i = charCode - 112;
    text = $("#predict-" + i).text();
    addText(text);
    getPredictions();
    return false;
  }
  else return true;
});


$( '.predicted-word' ).on('touchstart', function(e) {
    e.preventDefault();
    text = $(this).text();
    addText(text);
    getPredictions();
}).on('touchend touchcancel', function(e) {
    e.preventDefault();
});

$( '.predicted-word' ).on('click', function(e) {
    text = $(this).text();
    addText(text);
    getPredictions();
    $( 'textarea#prediction' ).focus();
})