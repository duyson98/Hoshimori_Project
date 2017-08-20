// Your functions or code that should load on all pages goes here.

function updateOwnedCards() {
    $('.ownedcard').each(function () {
        $(this).popover({
            'container': 'body',
            'trigger': 'click',
            'title': $(this).data('card-title'),
            'content': $(this).find('.hidden').html(),
            'html': true,
            'placement': 'bottom',
        });
    });
    $('.ownedcard').on('shown.bs.popover', function () {
        ajaxModals();
        $('.popover a').click(function (e) {
            hidePopovers();
            $('.ownedcard').popover('hide');
        });
    });
}

function hoverUpdateOwnedCards() {
    $('.ownedcard').each(function () {
        $(this).data('state', 'hover');
        $(this).popover({
            'container': 'body',
            'trigger': 'manual',
            'title': $(this).data('card-title'),
            'content': $(this).find('.hidden').html(),
            'html': true,
            'placement': 'bottom',
        });
    }).on("mouseenter", function () {
        var _this = this;
        $(this).popover("show");
        $(".popover").on("mouseleave", function () {
            $(_this).popover('hide');
        });
    }).on("mouseleave", function () {
        var _this = this;
        setTimeout(function () {
            if (!$(".popover:hover").length) {
                $(_this).popover("hide");
            }
        }, 300);
    });

    $('.ownedcard').on('shown.bs.popover', function () {
        ajaxModals();
        $('.popover a').click(function (e) {
            hidePopovers();
            $('.ownedcard').popover('hide');
        });
    });
}

function reloadOwnedCardsAfterModal(on_profile) {
    on_profile = typeof on_profile == 'undefined' ? true : on_profile;
    if (is_authenticated) {
        $('#freeModal').on('hidden.bs.modal', function () {
            if (ownedcards_to_reload.length > 0) {
                $.get('/ajax/ownedcards/?ids=' + ownedcards_to_reload.join(',') + '&page_size=' + ownedcards_to_reload.length, function (data) {
                    var html = $(data);
                    // Remove all that weren't returned
                    $.each(ownedcards_to_reload, function (_, id) {
                        if (html.find('[data-ownedcard-id="' + id + '"]').length == 0) {
                            $('[data-ownedcard-id="' + id + '"]').after('<br><br><span class="text-muted">' + gettext('Deleted') + '</span><br><br>');
                            $('[data-ownedcard-id="' + id + '"]').remove();
                        }
                    });
                    html.find('.ownedcard').each(function () {
                        var newOwnedcardItem = $(this);
                        var ownedcardItem;
                        if (on_profile) {
                            ownedcardItem = $('.profile-account #' + newOwnedcardItem.prop('id'));
                        } else {
                            ownedcardItem = $('.current-ownedcard_list #' + newOwnedcardItem.prop('id'));
                        }
                        if (ownedcardItem.length > 0) {
                            // Replace existing
                            ownedcardItem.html(newOwnedcardItem.html());
                        } else {
                            // Add at the end
                            var account_id = newOwnedcardItem.data('ownedcard-account-id');
                            var newElement = $('<div class="col-sm-3"></div>');
                            newElement.html(newOwnedcardItem);
                            $('#account' + account_id + 'Cards .row').last().append(newElement);
                        }
                    });
                    ownedcards_to_reload = [];
                    updateOwnedCards();
                });
            }
        })
    }
}

function hoverReloadOwnedCardsAfterModal(on_profile) {
    on_profile = typeof on_profile == 'undefined' ? true : on_profile;
    if (is_authenticated) {
        $('#freeModal').on('hidden.bs.modal', function () {
            if (ownedcards_to_reload.length > 0) {
                $.get('/ajax/ownedcards/?ids=' + ownedcards_to_reload.join(',') + '&page_size=' + ownedcards_to_reload.length, function (data) {
                    var html = $(data);
                    // Remove all that weren't returned
                    $.each(ownedcards_to_reload, function (_, id) {
                        if (html.find('[data-ownedcard-id="' + id + '"]').length == 0) {
                            $('[data-ownedcard-id="' + id + '"]').after('<br><br><span class="text-muted">' + gettext('Deleted') + '</span><br><br>');
                            $('[data-ownedcard-id="' + id + '"]').remove();
                        }
                    });
                    html.find('.ownedcard').each(function () {
                        var newOwnedcardItem = $(this);
                        var ownedcardItem;
                        if (on_profile) {
                            ownedcardItem = $('.profile-account #' + newOwnedcardItem.prop('id'));
                        } else {
                            ownedcardItem = $('.current-ownedcard_list #' + newOwnedcardItem.prop('id'));
                        }
                        if (ownedcardItem.length > 0) {
                            // Replace existing
                            ownedcardItem.html(newOwnedcardItem.html());
                        } else {
                            // Add at the end
                            var account_id = newOwnedcardItem.data('ownedcard-account-id');
                            var newElement = $('<div class="col-sm-3"></div>');
                            newElement.html(newOwnedcardItem);
                            $('#account' + account_id + 'Cards .row').last().append(newElement);
                        }
                    });
                    ownedcards_to_reload = [];
                    hoverUpdateOwnedCards();
                });
            }
        })
    }
}

$(document).ready(function(){
    var color = getComputedStyle(document.getElementById("profile-header-banner"), null).getPropertyValue("background-color");

    var colorList = ["rgb(169, 169, 169)","rgb(240, 128, 128)","rgb(50, 205, 50)","rgb(175, 238, 238)","rgb(255, 196, 35)",
        "rgb(255, 150, 35)","rgb(173, 255, 47)","rgb(219, 112, 147)","rgb(218, 112, 214)","rgb(100, 149, 237)","rgb(222, 184, 135)",
        "rgb(248, 255, 42)","rgb(221, 160, 221)","rgb(255, 248, 220)","rgb(224, 255, 255)","rgb(255, 192, 203)","rgb(60, 179, 113)",
        "rgb(238, 232, 170)","rgb(95, 158, 160)","rgb(178, 34, 34)","rgb(245, 245, 245)","rgb(65, 105, 225)","rgb(205, 92, 92)","rgb(100, 149, 237)"];
    for (var i = 0; i < colorList.length; i++) {
        if (color === colorList[i]) {
            if (i === 20)
                i = 101;
            else if (i === 21)
                i = 102;
            else if (i === 22)
                i = 103;
            else if (i === 23)
                i = 104;
            $(".current-user_item div#profile.jumbotron.jumbotron-main").addClass("banner-"+i);
            $(".current-user_item a.btn.btn-lg.btn-main").css({"background-color": color, "border-color": "black"});
            $(".current-user_item a.btn.btn-main").css({"background-color": color, "border-color": "black"});
            $(".current-user_item div.profile-tabs td").css({"background-color": color, "border-color": "black"});
            break;
        }
    }
});