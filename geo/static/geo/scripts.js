$.fn.jQuerySimpleCounter = function( options ) {
    var settings = $.extend({
        start:  0,
        end:    100,
        easing: 'swing',
        duration: 400,
        complete: ''
    }, options );

    var thisElement = $(this);

    $({count: settings.start}).animate({count: settings.end}, {
        duration: settings.duration,
        easing: settings.easing,
        step: function() {
            var mathCount = Math.ceil(this.count);
            thisElement.text(mathCount);
        },
        complete: settings.complete
    });
};

var num1 = $("#number1").text();
//var num2 = $("#number2").text();
//var num3 = $("#number3").text();
var num4 = $("#number4").text();


$('#content').waypoint(function(event, direction) {
    if (direction == 'down') {
        console.log("hola");
        $('#number1').jQuerySimpleCounter({end: num1,duration: 3000});
        //$('#number2').jQuerySimpleCounter({end: num2,duration: 3000});
        //$('#number3').jQuerySimpleCounter({end: num3,duration: 2000});
        $('#number4').jQuerySimpleCounter({end: num4,duration: 2500});
    }
});
