// Assuming you are using jQuery for AJAX

$(document).ready(function() {
    var recipeId = 123; // Replace with the actual recipe ID
  
    $.ajax({
      url: '/recipe/' + recipeId + '/ingredients',
      type: 'GET',
      success: function(data) {
        // Update the HTML with the received data
        if (data.length > 0) {
          var ingredientsHtml = '';
  
          for (var i = 0; i < data.length; i++) {
            var ingredient = data[i];
  
            ingredientsHtml += '<li class="ingredient-item">' +
              '<div class="ingredient-details">' +
              '<span class="ingredient-name">' + ingredient.ingredient_name + '</span>' +
              '<span class="ingredient-amount">' + ingredient.ingredient_amount + '</span>' +
              '<span class="ingredient-unit">' + ingredient.ingredient_unit + '</span>' +
              '</div>' +
              '</li>';
          }
  
          $('.ingredient-list').html(ingredientsHtml);
        } else {
          $('.ingredient-list').html('<p>No ingredients found.</p>');
        }
      },
      error: function() {
        console.log('Error occurred while fetching recipe ingredients.');
      }
    });
  });
  