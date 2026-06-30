$(document).ready(function() {
  $('.rating-form').submit(function(event) {
    event.preventDefault();

    let form = $(this);
    let productId = form.find('input[name="product_id"]').val();
    let rating = form.find('input[name="rating"]:checked').val();

    $.ajax({
       type: 'POST',
       url: '{% url "rate_product" %}',
       data: {
         'product_id': productId,
         'rating': rating,
         'csrfmiddlewaretoken': form.find('input[name="csrfmiddlewaretoken"]').val()
       },
       success: function(data) {
        $('#rating-' + productId).html(data.rating_stars);
        $('#message-' + productId).html(data.message);
        // Set current rating
        form.find('input[name="rating"]').each(function() {
          if ($(this).val() == rating) {
            $(this).prop('checked', true);
          }
        });
       }
    });
  });
});





// TO HANDLE REMOVE RATING
$(document).ready(function() {
  $('.remove-rating').click(function(event) {
    event.preventDefault();
    let productId = $(this).attr('id').split('-')[2];
    $.ajax({
      type: 'POST',
      url: '{% url "remove_rating" %}',
      data: {
        'product_id': productId,
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
      },
      success: function(data) {
        $('#rating-' + productId).html(data.rating_stars);
        $('#message-' + productId).html(data.message);
      }
    });
  });
});





