/**
 * Created by Koko on 8/20/2017.
 */

$(document).ready(function () {
    $('#sidebar-wrapper input').keydown(function (e) {
        if (e.which === 13) {
            e.preventDefault();
            $('[type="submit"]').trigger('click');
        }
    });
});