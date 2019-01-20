
$body = $("body");
var articles_array = [];
page = '';

function postData(data, url, successFunction){
  $('.articles-group').children('p').remove();
  $.ajax({
     url: url,
     data: JSON.stringify(data),
     contentType: "application/json; charset=utf-8",
     error: function(error) {
        console.log(error);
     },
     dataType: 'json',
     success: function(rec_data) {
      
        successFunction(rec_data);
     },
     type: 'POST'
  });

}

$(document).ready(function(){
  $(window).scroll(function(){
    if($(window).scrollTop()==($(document).height()-window.innerHeight)){
      if (!$('.articles-group').children('p').length && page == 'articles') {
      $('.loading-data').fadeIn();
      var url = '/categories/';
      var data = {
        'article_date': $('.articles-group').children().last().find('.article-date').text(),
        'id': $('.articles-group').children().first().find('.title').attr('name')
      };
      postData(data, url, loading_response);
      }
    }
  });
});

$('input[type=checkbox]').change(function() {
  var checked_classes = $('.class:checked').map(function(){
      return $(this).val();
    }).get();
    if (checked_classes.length == 0) {
      $('.articles-group > div').each(function () { 
        $(this).show();
        $(this).siblings('hr').first().show();
      });
    }else {
    $('.articles-group > div').each(function () { 
      var article_classes = $(this).find('.article_classes').map(function(){ return $(this).text(); }).get();
      for (var i = 0; i < checked_classes.length; i++) {
        var checked = checked_classes[i];
        if ($.inArray(checked, article_classes) != -1) {
          $(this).show();
        }else {
          $(this).hide();
          $(this).siblings('hr').first().hide();
        }
      }
    });
  }
});

function search(caller) {
  query = $(caller).siblings('input').val();

  url = '/search/'
  data = {
    'query': query
  };
  $('.articles-group').children().remove();
  postData(data, url, loading_response)
}

$('.articles-group').ready(function(){
    $body.addClass('loading');
    var url = window.location.pathname;
    var data = {
      'article_date': $('#article-date').text()
    }
    postData(data, url, loading_response);
});



function increase_reads(article_id) {
  url = '/add-reads/';
  data = {
    'article_id': article_id
  };

  postData(data, url, reads_increase_response)
}

function loading_response(response){
  if (response.success == true) {
    if (response.message == 'redirect') {
      location.replace('/categories/')
    }else {
      articles_array= response.message;
      page = response.page;
      appendArticles(response);
    }
  }
}

function sharingToFacebook() {
  FB.ui({
    method: 'share',
    mobile_iframe: true,
    href: 'https://developers.facebook.com/docs/',
  }, function(response){});
}

function sharingToTwitter() {
  
  var twitterWindow = window.open('https://twitter.com/share?url=' + document.URL, 'twitter-popup', 'height=350,width=600');
  if(twitterWindow.focus) { twitterWindow.focus(); }
    return false;
  
}

function fixing_date(date) {
  var new_date = date.split(':')[0];
  new_date = new_date.slice(0, -2);
  return new_date;
}

function addClasses(classes) {
  return_classes = '';
  for (var i = 0; i < classes.length; i++) {
    var class_ = classes[i];
    return_classes = return_classes + '<span class="article_classes">' + class_[1] + '</span>';
  }

  return return_classes;
}

function the_parag(parag) {
  paragraph = '';
  if (page == 'article') {
    paragraph = '<p>' +  parag + '</p>';
  }
  return paragraph;
}

function addSubImgs(sub_imgs) {
  var imgs_to_return = '';
  if (page == 'article') {
    for (var i = 0; i < sub_imgs.length; i++) {
      var the_img = sub_imgs[i];
      var img = '<img src="' + the_img + '" alt="sub picture" class="sub_img_view">';
      imgs_to_return = imgs_to_return + img;
    }
  }
  return imgs_to_return;
}

function showArticle(caller){
  var id = $(caller).attr('name');
  location.replace('/categories/' + id);
}

function reads_increase_response(response) {
  console.log(response);
}
