/**
 * Created by Koko on 6/25/2017.
 */
$(document).ready(function() {
    reloadOwnedCardsAfterModal(false);
    if ($('#sidebar-wrapper #id_type').length > 0 && $('#sidebar-wrapper #id_type + .cuteform').length < 1) {
	multiCuteForms({
	    'type': cuteformType,
	});
    }
});