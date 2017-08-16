/**
 * Created by Koko on 8/16/2017.
 */

var functionLoaders = function (account) {

    // Find empty slot
    var next_empty = null;
    var update_next_empty = function () {
        var broken = false;
        $('.builder-container-' + account + ' .card-builder').each(function () {
                if ($(this).is(':empty')) {
                    next_empty = $(this);
                    broken = true;
                    return false;
                }
            }
        );
        if (!broken) {
            next_empty = null;
        }
    };
    update_next_empty();

    var update_all = function () {
        if (next_empty !== null) {
            var current_mains = $('.builder-container-' + account + ' [data-card-role="main"]');
            var current_subs = $('.builder-container-' + account + ' [data-card-role="sub"]');
            var char_0 = current_mains.eq(0).children().data('card-chara');
            var char_1 = current_mains.eq(1).children().data('card-chara');
            var char_2 = current_mains.eq(2).children().data('card-chara');

            var blocked = {}; // Map to store invalid-card cards
            current_mains.each(function () {
                blocked[$(this).children().eq(0).data('card-id')] = true;
            });
            current_subs.each(function () {
                blocked[$(this).children().eq(0).data('card-id')] = true;
            });

            // If next card is main
            if (next_empty.data("card-role") === "main") {
                $('.builder-container-' + account + ' .card-pool .card-block').each(function () {
                    if (blocked[$(this).data('card-id')]
                        || $(this).data('card-chara') === char_0
                        || $(this).data('card-chara') === char_1
                        || $(this).data('card-chara') === char_2) {
                        $(this).attr("data-invalid-card", true);
                    } else {
                        $(this).removeAttr("data-invalid-card");
                        $(this).removeData("invalid-card");
                    }
                });
            } else {
                $('.builder-container-' + account + ' .card-block').each(function () {
                    if (blocked[$(this).data('card-id')]) {
                        $(this).attr("data-invalid-card", true);
                    } else {
                        $(this).removeAttr("data-invalid-card");
                        $(this).removeData("invalid-card");
                    }
                });
            }
        } else {
            $('.builder-container-' + account + ' .card-block').each(function () {
                $(this).attr("data-invalid-card", true);
            });
        }
    };

    var push_card = function (card) {
        // Find next empty slot
        if (next_empty !== null && !card.data('invalid-card')) {
            var clone_data = card.clone();
            clone_data.children()[1].remove();
            next_empty.html(clone_data);
            update_next_empty();
            update_all();
        }
    };
    var remove_card = function (slot) { // e.g. slot = $('#sub-12')
        slot.html("");
        update_next_empty();
        update_all();
    };

    // Assign add card to pool
    $('.builder-container-' + account + ' .card-pool img').each(function () {
        $(this).on("click", function () {
            push_card($(this).parent());
        });
    });
    // Assign remove card to slot
    $('.builder-container-' + account + ' .card-builder').each(function () {
        $(this).on("click", function () {
            remove_card($(this));
        });
    });
};