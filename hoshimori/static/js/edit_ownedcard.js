/**
 * Created by Koko on 6/25/2017.
 */
$(document).ready(function() {
    // Add ownedcard edited to the ones to reload
    if (typeof ownedcards_to_reload != 'undefined') {
	var id = parseInt($('#id_thing_to_delete').val());
	if (ownedcards_to_reload.indexOf(id) == -1) {
	    ownedcards_to_reload.push(id);
	}
    }
    // Add card to the ones to reload
    if (typeof cards_to_reload != 'undefined') {
	var id = parseInt($('h1#edit').text().match(/\d+/).slice(-1)[0]);
	if (cards_to_reload.indexOf(id) == -1) {
	    cards_to_reload.push(id);
	 }
    }
});