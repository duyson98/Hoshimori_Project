/**
 * Created by Koko on 7/6/2017.
 */
$(document).ready(function() {
    cuteformclear();
    if (typeof oss != 'undefined') {
	cuteform($('#id_i_os'), {
	    'html': oss,
	});
    }
});