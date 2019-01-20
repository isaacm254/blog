$('#add-link').dialog({
  autoOpen: false,
  modal: true,
  buttons: {
      "add link":
       function() {
        var the_link = $('#the-link').val();
        var titel_link = $('#title-link').val();
        var the_content = $('#content').val();
        $('#the-link').val("");
        $('#title-link').val("");
        $('#content').val(the_content + '<a href="' + titel_link + '" target="_blank">' + the_link + '</a>');
        $('#add-link').dialog( "close" );
      },'cancel':
    function(){
      $('#the-link').val("");
      $('#title-link').val("");
      $('#add-link').dialog( "close" );
    }
  }
});

$('#show').on('click', function(){
  $('#add-link').dialog('open');
});

$('#add-italic').click(function(){
  var the_content = $('#content').val();
  $('#content').val(the_content + '<em>text</em>');
});

$('#add-bold').click(function(){
  var the_content = $('#content').val();
  $('#content').val(the_content + '<b>text</b>');
});

$('#view').click(function(){
  var title = $('#title').val();
  var main_img = $(".main_img").attr("src");

  var all = $('#sub-imgs-view img').map(function(){
    return $(this).attr('src');
  });

  var the_content = $('#content').val();

  if (main_img !== undefined) {

    $('#view-test').html('<h3>' + title + '</h3>' + '<img src="' 
      + main_img + '" class="main_img_view" id="main_img_view"><div id="sub_img_view"></div>'+'<p>'+ the_content + '</p>');

    for(var i = 0; i < all.length; i++){
     $('#sub_img_view').append('<img src="' + all[i] + '" class="sub_img_view">');
    }

  }else {
    $('#view-test').html('<h3 id="title-test">' + title + '</h3><div id="sub_img_view"></div>' +'<p>'+ the_content + '</p>');
    for(var i = 0; i < all.length; i++){
     $('#sub_img_view').append('<img src="' + all[i] + '" class="sub_img_view">');
    }
  }
  
});

$('#view-test').on('click','#sub_img_view', function(){
  var viewer = new Viewer(document.getElementById('sub_img_view'));
});

$('#view-test').on('click','#main_img_view', function(){
  var viewer = new Viewer(document.getElementById('main_img_view'));
});


function mainUrl(input) {
  if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
        $('.main_img').remove();
        $('#main-img-view').append('<img src="'+ e.target.result+ '" class="main_img">');
      };

      reader.readAsDataURL(input.files[0]);
  }
}

function subUrl(input) {
  if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
          $('#sub-imgs-view').append('<img src="'+ e.target.result+ '" class="sub_img">');
      };

      reader.readAsDataURL(input.files[0]);
  }
}


$('#content').keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
        var the_content = $('#content').val();
        $('#content').val(the_content + '<br>');
    }
});

$('.mouse-over').on('mouseover mouseleave', function(event){
  if (event.type == "mouseover") {
    $(this).removeClass('mouse-over');
    $(this).addClass('its-over');

  }else if (event.type == "mouseleave"){
    $(this).removeClass('its-over');
    $(this).addClass('mouse-over');
  }
});

if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
}

function postData(data, url, successFunction){
  $.ajax({
     url: url,
     data: JSON.stringify(data),
     contentType: "application/json; charset=utf-8",
     error: function(error) {
        console.log(error);
     },
     dataType: 'json',
     success: function(rec_data) {
        console.log(rec_data);
        successFunction(rec_data);
     },
     type: 'POST'
  });

}

$('.sub_img').click(function() {
  $(this).remove();
});

function publish(){
  url = '/admin/editor/add-article/'

  var title = $('#title').val();
  var title_json = JSON.stringify(title);

  var main_img = $('#main-img-view').find('img').map(function(){
    return $(this).attr('src');
  }).get();
  var main_img_json = JSON.stringify(main_img);

  var sub_imgs = $('#sub-imgs-view').find('img').map(function(){
    return $(this).attr('src');
  }).get();
  var sub_img_json = JSON.stringify(sub_imgs);

  var content = $('#content').val();
  var content_json = JSON.stringify(content);

  var classes = $('.class:checked').map(function(){
      return $(this).val();
    }).get();
    var classes_json = JSON.stringify(classes);

  data = {
    'title': title,
    'main-img': main_img,
    'sub-imgs': sub_imgs,
    'article': content,
    'class': classes
  }

  postData(data, url, the_succ);
}

function the_succ(xhttp){
  console.log(xhttp);
}

$('#add-class').click(function(){
  data = {class: $('#new-class').val()};
  url = '/admin/editor/add-class/';

  postData(data, url, success);
});

function success(xhttp){
  console.log(xhttp);
}
