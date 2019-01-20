
$('.mouse-over').on('mouseover mouseleave', function(event){
  if (event.type == "mouseover") {
    $(this).removeClass('mouse-over');
    $(this).addClass('its-over');

  }else if (event.type == "mouseleave"){
    $(this).removeClass('its-over');
    $(this).addClass('mouse-over');
  }
});

var n_p = 50;
var p = 1;
function setButtons(){
  if (n_p <= 10) {

    for (var i = 1; i <= n_p; i++) {
       $('.pages-num').append('<a href="/categories/' + i + '">'+ 
          '<button class="btn" name="'+ i +'">' + i +'</button></a>');
    }

  }else if (n_p > 10) {
    p = $.cookie("page_num");
    if (p == undefined) {
      $.cookie("page_num", 1);
    }
    // console.log(p);
    if(p <= 5){
      for (var i = 1; i <= n_p; i++) {
       $('.pages-num').append('<a href="/categories/' + i + '">'+ 
          '<button class="btn" name="'+ i +'">' + i +'</button></a>');
       if (i == 8) {
        $('.pages-num').append('<span class="btn">....</span>');
        $('.pages-num').append('<a href="/categories/' + n_p + '">'+ 
          '<button class="btn" name="'+ n_p +'">' + n_p +'</button></a>');
        break;
       }
      }
    }else if (p > 5) {
      $('.pages-num').append('<a href="/categories/'+1+'">'+ 
      '<button class="btn" name="'+ 1 +'">' + 1 +'</button></a>');

      $('.pages-num').append('<span class="btn">....</span>');

      if (p >= n_p - 3) {
          for (var j = parseInt(p) - 7; j < n_p; j++) {
            $('.pages-num').append('<a href="/categories/' + j + '">'+ 
            '<button class="btn" name="'+ j +'">' + j +'</button></a>');
          }
          $('.pages-num').append('<a href="/categories/' + n_p + '">'+ 
          '<button class="btn" name="'+ n_p +'">' + n_p +'</button></a>');
          
      }else {
          for (var j = parseInt(p) - 3; j <= parseInt(p) + 3; j++) {
          $('.pages-num').append('<a href="/categories/' + j + '">'+ 
          '<button class="btn" name="'+ j +'">' + j +'</button></a>');
          }
          $('.pages-num').append('<span class="btn">....</span>');
          $('.pages-num').append('<a href="/categories/' + n_p + '">'+ 
          '<button class="btn" name="'+ n_p +'">' + n_p +'</button></a>');
      }          
    }

  }
}
$('.pages-num').ready(setButtons());

$('.pages-num').on('click','button', function(){
  var val = $(this).attr('name');
  $.cookie("page_num", val);
  console.log(p);
});


if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
}



function showOptions(caller){
  $(caller).find('ul').toggle();
   console.log('')
};

function mouseover(caller) {
  $(caller).removeClass('mouse-over');
    $(caller).addClass('its-over');
}

function mouseleave(caller) {
   $(caller).removeClass('its-over');
    $(caller).addClass('mouse-over');
}
