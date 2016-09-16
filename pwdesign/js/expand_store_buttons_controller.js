$(function() {

    var plus_buttons = $(".product_show_stores"),
        store_container = $(".product_container_stores");

    store_container.hide();

    plus_buttons.click(function() {

        if ($(this).hasClass("plus")) {
            $(this).removeClass("plus");
            $(this).html('<i class="material-icons">add</i>');
        } else {
            $(this).addClass("plus");
            $(this).html('<i class="material-icons">remove</i>');
        }

        var container_parent_button = $(this).parent(this),
            container_stores = container_parent_button.parent(container_parent_button).siblings(this);

        container_stores.slideToggle(300);
    });

});