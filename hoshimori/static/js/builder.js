/**
 * Created by Koko on 8/16/2017.
 */

var functionLoaders = function (account) {

    var cards_data = JSON.parse(ownedcards_values[account]);

    // Card updates
    var next_empty = null;
    var current_mains = $('.builder-container-' + account + ' [data-card-role="main"]');
    var current_subs = $('.builder-container-' + account + ' [data-card-role="sub"]');
    var leader = $('.builder-container-' + account + ' .leader');
    var partner_1 = $('.builder-container-' + account + ' .partner-1');
    var partner_2 = $('.builder-container-' + account + ' .partner-2');
    var current_cards = {};
    var results = $('.result-' + account);

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

    var update_valid = function () {
        if (next_empty !== null) {
            var char_0 = current_mains.eq(0).children().data('chara');
            var char_1 = current_mains.eq(1).children().data('chara');
            var char_2 = current_mains.eq(2).children().data('chara');
            var blocked = {}; // Map to store invalid-card cards

            current_mains.each(function () {
                blocked[$(this).children().eq(0).data('id')] = true;
            });
            current_subs.each(function () {
                blocked[$(this).children().eq(0).data('id')] = true;
            });
            // If next card is main

            if (next_empty.data("card-role") === "main") {
                $('.builder-container-' + account + ' .card-pool .card-block').each(function () {
                    if (blocked[$(this).data('id')]
                        || $(this).data('chara') === char_0
                        || $(this).data('chara') === char_1
                        || $(this).data('chara') === char_2) {
                        $(this).attr("data-invalid-card", true);
                    } else {
                        $(this).removeAttr("data-invalid-card");
                        $(this).removeData("invalid-card");
                    }

                    if (!current_cards[$(this).data('id')]) {
                        $(this).removeAttr("data-selected-card");
                        $(this).removeData("selected-card");
                    } else {
                        $(this).attr("data-selected-card", true);
                    }
                });
            } else {
                $('.builder-container-' + account + ' .card-block').each(function () {
                    if (blocked[$(this).data('id')]) {
                        $(this).attr("data-invalid-card", true);
                    } else {
                        $(this).removeAttr("data-invalid-card");
                        $(this).removeData("invalid-card");
                    }

                    if (!current_cards[$(this).data('id')]) {
                        $(this).removeAttr("data-selected-card");
                        $(this).removeData("selected-card");
                    } else {
                        $(this).attr("data-selected-card", true);
                    }
                });
            }
        } else {
            $('.builder-container-' + account + ' .card-block').each(function () {
                $(this).attr("data-invalid-card", true);
                if (!current_cards[$(this).data('id')]) {
                    $(this).removeAttr("data-selected-card");
                    $(this).removeData("selected-card");
                } else {
                    $(this).attr("data-selected-card", true);
                }
            });
        }
    };

    var get_result = function (position) {
        var main = position.find('[data-card-role="main"] .card-block');
        var subs = position.find('[data-card-role="sub"] .card-block');
        var i_weapon = main.data('i-weapon');

        var hp = main.data('hp');
        var sp = main.data('sp');
        var atk = main.data('atk');
        var def = main.data('def');
        var skills = {};
        skills[main.data('skill-jpn-name')] = {
            combo: main.data('skill-combo'),
            sp: main.data('skill-sp'),
            affinity: main.data('skill-affinity'),
            effect: main.data('skill-effect')
        };

        subs.each(function () {
            // Only add skills with same weapon type
            if (i_weapon === $(this).data('i-weapon')) {
                skills[$(this).data('skill-jpn-name')] = {
                    combo: $(this).data('skill-combo'),
                    sp: $(this).data('skill-sp'),
                    affinity: $(this).data('skill-affinity'),
                    effect: $(this).data('skill-effect')
                };
            }
            var multiplier = 0.25;
            if ($(this).data('subcard-effect') === 'True') {
                multiplier = 0.35;
            }
            hp += Math.floor($(this).data('hp') * multiplier);
            sp += Math.floor($(this).data('sp') * multiplier);
            atk += Math.floor($(this).data('atk') * multiplier);
            def += Math.floor($(this).data('def') * multiplier);
        });

        return {
            hp: hp, sp: sp, atk: atk, def: def,
            skills: skills,
            nakayoshi_jpn_name: main.data('nakayoshi-jpn-name'),
            nakayoshi_target: main.data('nakayoshi-target'),
            nakayoshi_effect: main.data('nakayoshi-effect')
        };
    };

    var update_result = function () {
        // Check for validity
        if (leader.find('[data-card-role="main"]').is(':empty')) {
            results.find('.invalid-deck').css("display", "");
            results.find('.results').css("display", "none");
        } else {
            results.find('.invalid-deck').css("display", "none");
            results.find('.results').css("display", "");

            var leader_results = get_result(leader);
            var leader_ele = $('.results-main');
            leader_ele.find('.results-hp').text(leader_results['hp']);
            leader_ele.find('.results-sp').text(leader_results['sp']);
            leader_ele.find('.results-atk').text(leader_results['atk']);
            leader_ele.find('.results-def').text(leader_results['def']);
            leader_ele.find('.nakayoshi-name').text(leader_results['nakayoshi_jpn_name']);
            leader_ele.find('.nakayoshi-target').text(leader_results['nakayoshi_target']);
            leader_ele.find('.nakayoshi-effect').text(leader_results['nakayoshi_effect']);
            leader_ele.find('.skills').html("");
            $.each(leader_results["skills"], function (k, v) {
                leader_ele.find('.skills').append('<tr> <th class="column-title"><strong>Skill name</strong></th> <th class="skill-name">' + k + '</th> <td class="column-title"><strong>Combo</strong></td><td class="skill-combo">' + v["combo"] + '</td><td class="column-title"><strong>SP</strong></td><td class="skill-sp">' + v["sp"] + '</td></tr><tr> <td class="column-title"><strong>Affinity</strong></td><td class="skill-affinity" colspan="5">' + v["affinity"] + '</td></tr>');
                if (v["effect"] !== "") {
                    leader_ele.find('.skills').append('<tr> <td class="column-title"><strong>Effect</strong></td><td class="skill-effect" colspan="5">' + v["effect"] + '</td></tr>');
                }
            });

            // Hide unnecessary fields
            if (partner_1.find('[data-card-role="main"]').is(':empty')) {
                results.find('.results-partner-1').css("display", "none");
            } else {
                var partner_1_results = get_result(partner_1);
                var partner_1_ele = $('.results-partner-1');
                partner_1_ele.find('.results-hp').text(partner_1_results['hp']);
                partner_1_ele.find('.results-sp').text(partner_1_results['sp']);
                partner_1_ele.find('.results-atk').text(partner_1_results['atk']);
                partner_1_ele.find('.results-def').text(partner_1_results['def']);
                partner_1_ele.find('.nakayoshi-name').text(partner_1_results['nakayoshi_jpn_name']);
                partner_1_ele.find('.nakayoshi-target').text(partner_1_results['nakayoshi_target']);
                partner_1_ele.find('.nakayoshi-effect').text(partner_1_results['nakayoshi_effect']);
                partner_1_ele.find('.skills').html("");
                $.each(partner_1_results["skills"], function (k, v) {
                    partner_1_ele.find('.skills').append('<tr> <th class="column-title"><strong>Skill name</strong></th> <th class="skill-name">' + k + '</th> <td class="column-title"><strong>Combo</strong></td><td class="skill-combo">' + v["combo"] + '</td><td class="column-title"><strong>SP</strong></td><td class="skill-sp">' + v["sp"] + '</td></tr><tr> <td class="column-title"><strong>Affinity</strong></td><td class="skill-affinity" colspan="5">' + v["affinity"] + '</td></tr>');
                    if (v["effect"] !== "") {
                        partner_1_ele.find('.skills').append('<tr> <td class="column-title"><strong>Effect</strong></td><td class="skill-effect" colspan="5">' + v["effect"] + '</td></tr>');
                    }
                });
                results.find('.results-partner-1').css("display", "");
            }
            if (partner_2.find('[data-card-role="main"]').is(':empty')) {
                results.find('.results-partner-2').css("display", "none");
            } else {
                var partner_2_results = get_result(partner_2);
                var partner_2_ele = $('.results-partner-2');
                partner_2_ele.find('.results-hp').text(partner_2_results['hp']);
                partner_2_ele.find('.results-sp').text(partner_2_results['sp']);
                partner_2_ele.find('.results-atk').text(partner_2_results['atk']);
                partner_2_ele.find('.results-def').text(partner_2_results['def']);
                partner_2_ele.find('.nakayoshi-name').text(partner_2_results['nakayoshi_jpn_name']);
                partner_2_ele.find('.nakayoshi-target').text(partner_2_results['nakayoshi_target']);
                partner_2_ele.find('.nakayoshi-effect').text(partner_2_results['nakayoshi_effect']);
                partner_2_ele.find('.skills').html("");
                $.each(partner_2_results["skills"], function (k, v) {
                    partner_2_ele.find('.skills').append('<tr> <th class="column-title"><strong>Skill name</strong></th> <th class="skill-name">' + k + '</th> <td class="column-title"><strong>Combo</strong></td><td class="skill-combo">' + v["combo"] + '</td><td class="column-title"><strong>SP</strong></td><td class="skill-sp">' + v["sp"] + '</td></tr><tr> <td class="column-title"><strong>Affinity</strong></td><td class="skill-affinity" colspan="5">' + v["affinity"] + '</td></tr>');
                    if (v["effect"] !== "") {
                        partner_2_ele.find('.skills').append('<tr> <td class="column-title"><strong>Effect</strong></td><td class="skill-effect" colspan="5">' + v["effect"] + '</td></tr>');
                    }
                });
                results.find('.results-partner-2').css("display", "");
            }
        }
    };

    var push_card = function (card) {
        // Find next empty slot
        if (next_empty !== null && !card.data('invalid-card')) {

            var clone_data = card.clone();
            clone_data.children()[1].remove();
            var dict = cards_data[card.data('id')];
            for (var key in dict) {
                clone_data.data(key, dict[key]);
            }

            next_empty.html(clone_data);

            current_cards[card.data('id')] = true;
            update_next_empty();
            update_valid();
        } else if (card.data('selected-card')) {
            // If this is a selected card, remove it from the slots
            current_mains.each(function () {
                if (card.data('id') === $(this).children().eq(0).data('id')) {
                    remove_card($(this));
                    return false;
                }
            });
            current_subs.each(function () {
                if (card.data('id') === $(this).children().eq(0).data('id')) {
                    remove_card($(this));
                    return false;
                }
            });
        }
        update_result();
    };
    var remove_card = function (slot) { // e.g. slot = $('#sub-12')
        delete current_cards[slot.children().eq(0).data('id')];
        slot.html("");
        update_next_empty();
        update_valid();
        update_result();
    };

    var pool = $('.builder-container-' + account + ' .card-pool');
    var all_cards = pool.find('.col-md-4').clone();

    // Filters
    var filter = function () {
        // Get filters
        var filters = {};
        $('.card-pool-filter-container span').each(function () {
            if ($(this).data('on')) {
                filters[$(this).data('weapon')] = true;
            }
        });

        // Remove card that is not in the filter
        var clone_cards = [];
        all_cards.each(function () {
            if (!filters[$(this).find('.card-block').data('i-weapon')]) {
                clone_cards.push($(this));
            }
        });

        // Generate HTML anew
        pool.html("");
        // Add rows first
        for (var i = 0; i < Math.ceil(clone_cards.length / 3); ++i) {
            pool.append('<div class="row">');
        }
        // Then add cards
        var rows = pool.find('.row');
        for (var j = 0; j < clone_cards.length; ++j) {
            rows[Math.floor(j / 3)].append(clone_cards[j][0]);
        }
        update_next_empty();
        update_valid();
    };

    var toggle_filter = function (weapon) {
        if (weapon.data("on")) { // If on, turn off
            weapon.removeAttr("data-on");
            weapon.removeData("on");
        } else { // turn on
            weapon.attr("data-on", true);
        }
    };

    var reloader = function () {
        /* Assign add card to pool */
        $('.builder-container-' + account + ' .card-pool .icon').each(function () {
            $(this).on("click", function () {
                push_card($(this).parent());
            });
        });
    };
    /* Assign remove card to slot */
    $('.builder-container-' + account + ' .card-builder').each(function () {
        $(this).on("click", function () {
            remove_card($(this));
        });
    });
    /* Assign clear card */
    $('.builder-container-' + account + ' .clear-button').each(function () {
        var clearBtn = $(this);
        clearBtn.on("click", function () {
            clearBtn.parent().find('.card-builder').each(function () {
                remove_card($(this));
            });
        });
    });
    /* Assign clear filters */
    $('.builder-container-' + account + ' .clear-filters-button').on("click", function () {
        $('.builder-container-' + account + ' .card-pool-filter-container span').each(function () {
            if ($(this).data('on')) {
                toggle_filter($(this));
            }
        });
        filter();
        reloader();
    });
    /* Assign filtering */
    $('.builder-container-' + account + ' .card-pool-filter-container span').each(function () {
        $(this).on("click", function () {
            if (event.altKey) { // Reverse filter
                var current_weap = $(this).data('weapon');
                $('.builder-container-' + account + ' .card-pool-filter-container span').each(function () {
                    if (($(this).data('weapon') !== current_weap && !$(this).data('on'))
                        || ($(this).data('weapon') === current_weap && $(this).data('on'))) {
                        toggle_filter($(this));
                    }
                });
            } else {
                toggle_filter($(this));
            }
            filter();
            reloader();
        });
    });

    // Initialization
    update_next_empty();
    update_result();
    filter();
    reloader();
};