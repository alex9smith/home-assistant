// FUNCTIONS

function renderItem(item) {
    // Takes a shopping list item and renders a new row at the end of the container
    $('#shopping-list').append(
        $('<li>').attr('class', 'collection-item').attr('id', item['_id']).append(
            $('<div>').text(item['name']).append(
                $('<div>').attr('class', 'secondary-content remove').append(
                    $('<i>').attr('class', 'material-icons left').attr('id', item['_id']).text('done_outline')
                )
            )
        )
    );
};

function getAndRenderShoppingListItems() {
    // Deletes all the li items then
    // Hits the API and renders the list again
    $('li.collection-item').remove();
    $.get('/api/v1/shoppinglist', function(data, status) {
        data['items'].forEach(element => {
            renderItem(element);
        });

        // Set up click listener for deletions
        $('.remove i').click(function() {
            removeItemFromShoppingList(this.id);
        });
    });
}

function removeItemFromShoppingList(id) {
    // Makes a call to the API to delete the item from the list
    // If it succeeds, also remove the li element
    $.ajax({
        url: '/api/v1/shoppinglist/' + id,
        type: 'DELETE',
        contentType: 'application/json',
        success: function(data, status) {
            if (data['status'] == 'Success') {
                $('li#' + id).slideUp()
                $('li#' + id).remove()
            }
        }
    });
}

function addItemToShoppingList() {
    // Reads the contents of the input box
    // Adds to shopping list
    // Then refreshes the list contents
    var id = $('input#shopping').val();
    $.ajax({
        url: '/api/v1/shoppinglist/' + id,
        type: 'PUT',
        contentType: 'application/json',
        success: function(data, status) {
            if (data['status'] == 'Success') {
                getAndRenderShoppingListItems()
            }
        }
    });
    id = $('input#shopping').val('')
}

// DOCUMENT READY

$(document).ready(function(){
    
    // Set up sidebar
    $('.sidenav').sidenav();

    // Load items on list from API and render
    items = getAndRenderShoppingListItems();

    // Set up listener for the input box
    $(document).keypress(function(e) {
        if(e.which == 13) {
            addItemToShoppingList()
        }
    });

}); // end of document ready
  
