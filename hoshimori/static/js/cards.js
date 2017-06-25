function handleClickAddCard() {
    $('.card a[href="#addCard"]').unbind('click');
    $('.card a[href="#addCard"]').click(function (e) {
        e.preventDefault();
        var button = $(this);
        var card = button.closest('.card');
        var form = card.find('form.form-add-card');
        var loader = card.find('.addcard-loader');
        button.hide();
        loader.show();
        form.ajaxSubmit({
            success: function (data) {
                loader.hide();
                button.show();
                card.replaceWith(data);
                updateCards();
                ajaxModals();
            },
            error: genericAjaxError,
        });
        return false;
    });
}

function handleClickFavoriteCard() {
    $('.card a[href="#favoriteCard"]').unbind('click');
    $('.card a[href="#favoriteCard"]').click(function (e) {
        e.preventDefault();
        var button = $(this);
        var card = button.closest('.card');
        var form = card.find('form.form-favorite-card');
        var loader = card.find('.favoritecard-loader');
        button.hide();
        loader.show();
        console.log(form.data('action-favorite'));
        form.ajaxSubmit({
            success: function (data) {
                loader.hide();
                button.show();
                card.replaceWith(data);
                updateCards();
                ajaxModals();
            },
            error: genericAjaxError,
        });
        return false;
    });
}

function handleClickInfo() {
    $('.card [data-info-ajax]').unbind('click');
    $('.card [data-info-ajax]').click(function (e) {
        e.preventDefault();
        var button = $(this);
        var card = button.closest('.card');
        var loader = card.find('.info-loader');
        button.hide();
        loader.show();
        $.get(button.data('info-ajax'), function (data) {
            loader.hide();
            button.show();
            $('[data-toggle="tooltip"]').tooltip('hide');
            freeModal(card.data('card-title'), data, 0);
            updateCards();
            ajaxModals();
        });
        return false;
    });
}

function updateCards() {
    $('[data-toggle="tooltip"]').tooltip();
    handleClickInfo();
    handleClickAddCard();
    handleClickFavoriteCard();
    handleLevels();
    $('.card-buttons .account-select').each(function () {
        var select = $(this);
        if (!select.next().hasClass('cuteform-modal-button')) {
            var accounts = {};
            select.find('option').each(function () {
                accounts[$(this).attr('value')] = $(this).text();
            });
            cuteform(select, {
                'modal': 'true',
                'html': accounts,
            });
        }
    });
}

function updateCardsAndOwnedCards() {
    updateCards();
    updateOwnedCards();
}

function changeSkillLevel(e) {
    e.preventDefault();
    var button = $(this);
    var skill = button.closest('.card-skills');
    var level_span = skill.find('.skill-level');
    var max_level = parseInt(level_span.data('max-level'));
    var skill_details = skill.data('levels');
    var current_level = parseInt(level_span.text());
    var new_level;
    if (button.attr('href').indexOf('+') >= 0) {
        new_level = current_level + 1;
    } else {
        new_level = current_level - 1;
    }
    if (new_level > max_level) {
        new_level = max_level;
    }
    if (new_level < 1) {
        new_level = 1;
    }
    if (new_level == max_level) {
        skill.find('[href="#changeSkillLevel+"]').addClass('disabled');
    } else {
        skill.find('[href="#changeSkillLevel+"]').removeClass('disabled');
    }
    if (new_level == 1) {
        skill.find('[href="#changeSkillLevel-"]').addClass('disabled');
    } else {
        skill.find('[href="#changeSkillLevel-"]').removeClass('disabled');
    }
    level_span.text(new_level);
    skill.find('.skill-details').first().text(skill_details['english'][new_level]);
    skill.find('.skill-details-jp').first().text(skill_details['japanese'][new_level]);
    return false;
}

function handleLevels() {
    if ($('.changeLevel').length > 0) {
        $('.changeLevel').click(function (e) {
            var button = $(this);
            var stats = button.closest('.card-stats');
            var level = button.find('.level').text();
            if (level) {
                changeStats(stats, level);
            }
        });
    }
    $('input[name="changeLevelNumber"]').bind("change paste keyup", function () {
        var level = $(this).val();
        var stats = $(this).closest('.card-stats');
        changeStats(stats, level);
    });
    $('[href="#changeSkillLevel+"]').unbind('click');
    $('[href="#changeSkillLevel+"]').click(changeSkillLevel);
    $('[href="#changeSkillLevel-"]').unbind('click');
    $('[href="#changeSkillLevel-"]').click(changeSkillLevel);
}

$(document).ready(function () {
    if ($('#sidebar-wrapper #id_type').length > 0 && $('#sidebar-wrapper #id_type + .cuteform').length < 1) {
        multiCuteForms({
            'type': cuteformType,
        });
    }
    if (typeof hidden_handler != 'undefined') {
        if (!hidden_handler && is_authenticated) {
            hidden_handler = true;
            $('#freeModal').on('hidden.bs.modal', function () {
                if (cards_to_reload.length > 0) {
                    $.get('/ajax/cards/?ids=' + cards_to_reload.join(',') + '&page_size=' + cards_to_reload.length, function (data) {
                        var html = $(data);
                        html.find('.card').each(function () {
                            var newCardItem = $(this);
                            var cardItem = $('#' + newCardItem.prop('id'));
                            if (cardItem.length > 0) {
                                cardItem.html(newCardItem.html());
                            }
                            cards_to_reload = [];
                            updateCards();
                            ajaxModals();
                        });
                    });
                }
            });
        }
    }
});