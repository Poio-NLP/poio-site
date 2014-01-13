
////////////////////////////////////////////////////// About page hover stuff

$( "a.icon_prediction" ).hover(
  function() {
    $( "img#icon_prediction" ).attr('src', '/static/media/img/icon_prediction_selected_{{ g.color }}.png');
    $( "a.icon_prediction" ).css('color', '{{ g.color_code }}');
  }, function() {
    $( "img#icon_prediction" ).attr('src', '/static/media/img/icon_prediction.png');
    $( "a.icon_prediction" ).css('color', '#000');
  }
);

$( "a.icon_testemonial" ).hover(
  function() {
    $( "img#icon_testemonial" ).attr('src', '/static/media/img/icon_testemonial_selected_{{ g.color }}.png');
    $( "a.icon_testemonial" ).css('color', '{{ g.color_code }}');
  }, function() {
    $( "img#icon_testemonial" ).attr('src', '/static/media/img/icon_testemonial.png');
    $( "a.icon_testemonial" ).css('color', '#000');
  }
);

$( "a.icon_documentation" ).hover(
  function() {
    $( "img#icon_documentation" ).attr('src', '/static/media/img/icon_documentation_selected_{{ g.color }}.png');
    $( "a.icon_documentation" ).css('color', '{{ g.color_code }}');
  }, function() {
    $( "img#icon_documentation" ).attr('src', '/static/media/img/icon_documentation.png');
    $( "a.icon_documentation" ).css('color', '#000');
  }
);

$( "a.icon_map" ).hover(
  function() {
    $( "img#icon_map" ).attr('src', '/static/media/img/icon_map_selected_{{ g.color }}.png');
    $( "a.icon_map" ).css('color', '{{ g.color_code }}');
  }, function() {
    $( "img#icon_map" ).attr('src', '/static/media/img/icon_map.png');
    $( "a.icon_map" ).css('color', '#000');
  }
);

$( ".nav span a" ).click(
  function () {
    $( "span.menu_about" ).toggleClass('selected', false);
    $( "span.menu_tools" ).toggleClass('selected', false);
    $( "span.menu_team" ).toggleClass('selected', false);
    $( "span.menu_map" ).toggleClass('selected', false);
    $( "span.menu_documentation" ).toggleClass('selected', false);
    $(this).parent().toggleClass('selected', true);
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
        $( "textarea#prediction" ).val('')
        $( "span.menu_tools" ).toggleClass('selected', true);
        break;    
      case 4:
        $( "span.menu_map" ).toggleClass('selected', true);
        if (!mapDrawn)
          drawMap();
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


///////////////////////////////// Use jquery chosen for language selector

$(function(){
  $(".chosen-select").chosen();
});


///////////////////////////////////////////////// Map

function drawMap() {

  //////////////////////////////////////////////////////////////// Globals

  var land;
  var borders;
  var tooltipLayer;
  var dragStarted = false;
  var lastMouseX = -1;
  var lastMouseY = -1;
  var lastR = 0;
  var worldData;
  var projection;
  var path;
  var c;

  //////////////////////////////////////////////////////////////// Functions

  function drawLand() {
    c.beginPath();
    c.fillStyle = "{{ g.color_code }}";
    path(land);
    c.fill();

    c.beginPath();
    c.strokeStyle = "#fff"; 
    c.lineWidth = .5;
    path(borders);
    c.stroke();
  }

  function drawLanguages() {
    Object.keys(languages).forEach(function (key) {
      var value = languages[key]
      var centerX = projection([value.geo.lon, value.geo.lat])[0];
      var centerY = projection([value.geo.lon, value.geo.lat])[1];

      var circle = new Kinetic.Circle({
        x: centerX,
        y: centerY,
        fill: "red",
        stroke: "#330000",
        strokeWidth: 2,
        radius: 5
      });

      circle.on("mousemove", function(){
        var mousePos = stage.getMousePosition();
        tooltip.setPosition(mousePos.x + 5, mousePos.y - 20);
        tooltip.setText(value.label);
        tooltip.show();
        tooltipLayer.draw();
        document.body.style.cursor = "pointer";
      });

      circle.on("mouseout", function(){
        tooltip.hide();
        tooltipLayer.draw();
        document.body.style.cursor = "default";
      });

      circle.on("click", function(){
        //window.location = '/tools/prediction/' + key
        $('select#language_chooser').val(key);
        $('select#language_chooser').trigger('chosen:updated');
        $(".main").moveUp();
      });

      shapesLayer.add(circle);

    });

    var tooltip = new Kinetic.Text({
      text: "",
      fontFamily: "Calibri",
      fontSize: 12,
      padding: 5,
      textFill: "white",
      fill: "black",
      alpha: 0.75,
      visible: false
    });

    tooltipLayer.add(tooltip);
    shapesLayer.draw();
  }

  function makeDraggable() {
    //worldLayer.setDraggable(true);
    stage.getContainer().addEventListener('mousedown', function(e) {
      lastMouseX = e.screenX;
      lastMouseY = e.screenY;
      dragStarted = true;
      lastR = projection.rotate();
    });
    stage.getContainer().addEventListener('mouseup', function(e) {
      lastMouseX = -1;
      lastMouseY = -1;
      dragStarted = false;
    });
    stage.getContainer().addEventListener('mouseout', function(e) {
      lastMouseX = -1;
      lastMouseY = -1;
      dragStarted = false;
    });
    stage.getContainer().addEventListener('mousemove', function(e) {
      if (dragStarted) {
        var diffX = lastR[0] + ( (e.screenX - lastMouseX) / 10);
        var diffY = lastR[1] + ( (lastMouseY - e.screenY) / 10);

        projection.rotate([diffX, diffY, 0]);

        c.clearRect(0, 0, width, height);
        tooltipLayer.removeChildren();
        shapesLayer.removeChildren();
        drawLand();
        drawLanguages();
      }
    });
  }

  function transitionEnded() {
    drawLanguages();
    makeDraggable();
  }

  //////////////////////////////////////////////////////////////// Main

  var width = 930,
  height = 500;

  var stage = new Kinetic.Stage({
    container: 'map',
    width: width,
    height: height
  });
  worldLayer = new Kinetic.Layer();
  shapesLayer = new Kinetic.Layer();
  tooltipLayer = new Kinetic.Layer();
  stage.add(worldLayer);
  stage.add(shapesLayer);
  stage.add(tooltipLayer);

  c = worldLayer.getContext();

  projection = d3.geo.orthographic()
  .scale(250)
  .translate([700,250])
  .clipAngle(90)
  .clipExtent([[0,0],[width,height]]);

  path = d3.geo.path()
  .projection(projection)
  .context(c);
  
  queue()
  .defer(d3.json, '/static/media/data/world-110m.json')
  .await(ready);

  function ready(error, world) {
    worldData = world;
    land = topojson.feature(worldData, worldData.objects.land);
    borders = topojson.mesh(worldData, worldData.objects.countries, function(a, b) { return a !== b; });

    c.clearRect(0, 0, width, height);

    drawLand();
    mapDrawn = true;

    (function transition() {
      d3.transition()
      .delay(1000)
      .duration(2500)
      .tween("rotate", function() {
        var r = d3.interpolate(projection.rotate(), [-40, -55]);
        var s = d3.interpolate(projection.scale(), 900);
        return function(t) {
          projection.rotate(r(t));
          projection.scale(s(t));
          c.clearRect(0, 0, width, height);
          drawLand();
        };
      })
      .each("end", transitionEnded)
    })();
  }

}