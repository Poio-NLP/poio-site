
////////////////////////////////////////////////////// About page hover stuff

$( "a.icon_prediction" ).hover(
  function() {
    $( "img#icon_prediction" ).attr('src', '/static/media/img/icon_prediction_selected_green.png');
    $( "a.icon_prediction" ).css('color', '#2bb673');
  }, function() {
    $( "img#icon_prediction" ).attr('src', '/static/media/img/icon_prediction.png');
    $( "a.icon_prediction" ).css('color', '#000');
  }
);

$( "a.icon_testemonial" ).hover(
  function() {
    $( "img#icon_testemonial" ).attr('src', '/static/media/img/icon_testemonial_selected_green.png');
    $( "a.icon_testemonial" ).css('color', '#2bb673');
  }, function() {
    $( "img#icon_testemonial" ).attr('src', '/static/media/img/icon_testemonial.png');
    $( "a.icon_testemonial" ).css('color', '#000');
  }
);

$( "a.icon_documentation" ).hover(
  function() {
    $( "img#icon_documentation" ).attr('src', '/static/media/img/icon_documentation_selected_green.png');
    $( "a.icon_documentation" ).css('color', '#2bb673');
  }, function() {
    $( "img#icon_documentation" ).attr('src', '/static/media/img/icon_documentation.png');
    $( "a.icon_documentation" ).css('color', '#000');
  }
);

$( "a.icon_map" ).hover(
  function() {
    $( "img#icon_map" ).attr('src', '/static/media/img/icon_map_selected_green.png');
    $( "a.icon_map" ).css('color', '#2bb673');
  }, function() {
    $( "img#icon_map" ).attr('src', '/static/media/img/icon_map.png');
    $( "a.icon_map" ).css('color', '#000');
  }
);

/////////////////////////////////////////// Scrolling

$(".main").onepage_scroll({
  sectionContainer: "section",
  easing: "ease",
  animationTime: 1000,
  pagination: false,
  updateURL: true,
  beforeMove: function(index) {},
  afterMove: function(index) {
    $( "span.menu_about" ).toggleClass('selected', false);
    $( "span.menu_tools" ).toggleClass('selected', false);
    $( "span.menu_team" ).toggleClass('selected', false);
    $( "span.menu_map" ).toggleClass('selected', false);
    $( "span.menu_documentation" ).toggleClass('selected', false);
    $( "a.scroll_down").css("display", "block");
    $( "a.scroll_up").css("display", "none");
    current_index = parseInt($("section.active").attr("data-index"));
    switch(current_index) {
      case 2:
        $( "span.menu_about" ).toggleClass('selected', true);
        break;    
      case 3:
        $( "span.menu_tools" ).toggleClass('selected', true);
        break;    
      case 4:
        $( "span.menu_map" ).toggleClass('selected', true);
        break;    
      case 5:
        $( "span.menu_team" ).toggleClass('selected', true);
        break;    
      case 6:
        $( "span.menu_documentation" ).toggleClass('selected', true);
        $( "a.scroll_down").css("display", "none");
        $( "a.scroll_up").css("display", "block");
        break;    
    }
  },
  loop: false,
  responsiveFallback: false
});

$( "a.scroll_down" ).click(function() {
  $(".main").moveDown();
});

$( "a.scroll_up" ).click(function() {
  $(".main").moveUp();
});

$( "a.menu_start" ).click(function() {
  $(".main").moveTo(1);
});

$( "a.menu_about" ).click(function() {
  $(".main").moveTo(2);
});

$( "a.menu_tools" ).click(function() {
  $(".main").moveTo(3);
});

$( "a.menu_map" ).click(function() {
  $(".main").moveTo(4);
});

$( "a.menu_team" ).click(function() {
  $(".main").moveTo(5);
});

$( "a.menu_documentation" ).click(function() {
  $(".main").moveTo(6);
});

$( "a.icon_prediction" ).click(function() {
  $(".main").moveTo(3);
});

$( "a.icon_map" ).click(function() {
  $(".main").moveTo(4);
});

$( "a.icon_documentation" ).click(function() {
  $(".main").moveTo(6);
});
