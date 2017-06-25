function handleAddCard() {
    $('#collection [href="#addCard"]').unbind('click');
    $('#collection [href="#addCard"]').click(function(e) {
	e.preventDefault();
	var button = $(this);
	var collection = button.closest('.account-collection');
	var form = collection.find('form');
	var loader = collection.find('.flaticon-loading');
	button.hide();
	loader.show();
	form.ajaxSubmit({
	    success: function(data) {
		if ($('.current-card_item').length > 0) {
		    $('#collection').replaceWith(data);
		} else {
		    freeModal($('#freeModal .modal-header h4').text(), data);
		    if (typeof cards_to_reload != 'undefined') {
			var id = parseInt($('#collection').data('card-id'));
			if (cards_to_reload.indexOf(id) == -1) {
			    cards_to_reload.push(id);
			}
		    }
		}
	    },
	});
	return false;
    });
}

$(document).ready(function() {
    loadToolTips();
    loadPopovers();
    ajaxModals();
    handleAddCard();
});