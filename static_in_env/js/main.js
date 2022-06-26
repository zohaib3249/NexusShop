(function($) {
    "use strict";

    /*[ Load page ]
    ===========================================================*/
    $(".animsition").animsition({
        inClass: 'fade-in',
        outClass: 'fade-out',
        inDuration: 1500,
        outDuration: 800,
        loadingCss: "",
        linkElement: '.animsition-link',
        loading: true,
        loadingParentElement: 'html',
        loadingClass: 'animsition-loading-1',
        loadingInner: '<style>@keyframes poofity {0% {transform: scale(1, 1) rotate(90deg);opacity: 0.1;}50% {transform: scale(4, 4) rotate(-360deg);opacity: 0;}}@keyframes poof {0% {transform: scale(1, 1) rotate(0deg);opacity: 0.2;}50% {transform: scale(4, 4) rotate(360deg);opacity: 0;}} .another {opacity: 0.1;transform: rotate(90deg);animation: poofity 5s infinite;animation-delay: 1s;}@keyframes loadEr {0% {border-top-color: rgba(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0);border-left-color: rgba(33, 33, 33, 0);} 10.4% {border-top-color: rgba(44, 44, 44, 0.5);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0);border-left-color: rgba(33, 33, 33, 0);}    20.8% {border-top-color: rgba(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0);  border-left-color: rgba(33, 33, 33, 0);}  31.2% {border-top-color: rgba(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0.5);border-bottom-color: rgba(66, 66, 66, 0);border-left-color: rgba(33, 33, 33, 0);} 41.6% {border-top-color: rgba(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0);border-left-color: rgba(33, 33, 33, 0);transform: rotate(40deg);} 52% {border-top-color: rgba(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0.5);border-left-color: rgba(33, 33, 33, 0);} 62.4% {border-top-color: rgba(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0);border-left-color: rgba(33, 33, 33, 0);} 72.8% {border-top-color: rgba(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0);border-left-color: rgba(33, 33, 33, 0.5);}} .text {position: absolute;top: 95px;left: 8px;font-family: Arial;text-transform: uppercase;color: #888;animation: opaa 10s infinite;} @keyframes opaa {0% {opacity: 1;}10% {opacity: 0.5}15% {opacity: 1;}30% {opacity: 1;}65% {opacity: 0.3;}90% {opacity: 0.8;}}</style><div class="wrap" style="position: absolute;top: 40%;width: 100%;margin-left:40%"><div class="loader" style="position: absolute;top: 0;z-index: 10;width: 50px;height: 50px;border: 15px solid;border-radius: 50%;border-top-color: rgb(44, 44, 44, 0);border-right-color: rgba(55, 55, 55, 0);border-bottom-color: rgba(66, 66, 66, 0);border-left-color: rgba(33, 33, 33, 0);animation: loadEr 3s infinite;"></div><div class="loaderbefore" style="width: 50px;height: 50px;border: 15px solid #ddd;border-radius: 50%;position: absolute;top: 0;z-index: 9;"></div><div class="circular" style="position: absolute;top: -15px;left: -15px;width: 70px;height: 70px;border: 20px solid;border-radius: 50%;border-top-color: #333;border-left-color: #fff;border-bottom-color: #333;border-right-color: #fff;opacity: 0.2;animation: poof 5s infinite;"></div><div class="circular another" style="opacity: 0.1;transform: rotate(90deg);animation: poofity 5s infinite;animation-delay: 1s;"></div><div class="text">Loading</div></div>',
        timeout: false,
        timeoutCountdown: 5000,
        onLoadEvent: true,
        browser: ['animation-duration', '-webkit-animation-duration'],
        overlay: false,
        overlayClass: 'animsition-overlay-slide',
        overlayParentElement: 'html',
        transition: function(url) { window.location.href = url; }
    });

    /*[ Back to top ]
    ===========================================================*/
    var windowH = $(window).height() / 2;

    $(window).on('scroll', function() {
        if ($(this).scrollTop() > windowH) {
            $("#myBtn").css('display', 'flex');
        } else {
            $("#myBtn").css('display', 'none');
        }
    });

    $('#myBtn').on("click", function() {
        $('html, body').animate({ scrollTop: 0 }, 300);
    });


    /*[ Show header dropdown ]
    ===========================================================*/
    $('.js-show-header-dropdown').on('click', function() {
        $(this).parent().find('.header-dropdown')
    });

    var menu = $('.js-show-header-dropdown');
    var sub_menu_is_showed = -1;

    for (var i = 0; i < menu.length; i++) {
        $(menu[i]).on('click', function() {

            if (jQuery.inArray(this, menu) == sub_menu_is_showed) {
                $(this).parent().find('.header-dropdown').toggleClass('show-header-dropdown');
                sub_menu_is_showed = -1;
            } else {
                for (var i = 0; i < menu.length; i++) {
                    $(menu[i]).parent().find('.header-dropdown').removeClass("show-header-dropdown");
                }

                $(this).parent().find('.header-dropdown').toggleClass('show-header-dropdown');
                sub_menu_is_showed = jQuery.inArray(this, menu);
            }
        });
    }

    $(".js-show-header-dropdown, .header-dropdown").click(function(event) {
        event.stopPropagation();
    });

    $(window).on("click", function() {
        for (var i = 0; i < menu.length; i++) {
            $(menu[i]).parent().find('.header-dropdown').removeClass("show-header-dropdown");
        }
        sub_menu_is_showed = -1;
    });


    /*[ Fixed Header ]
    ===========================================================*/
    var posWrapHeader = $('.topbar').height();
    var header = $('.container-menu-header');

    $(window).on('scroll', function() {

        if ($(this).scrollTop() >= posWrapHeader) {
            $('.header1').addClass('fixed-header');
            $(header).css('top', -posWrapHeader);

        } else {
            var x = -$(this).scrollTop();
            $(header).css('top', x);
            $('.header1').removeClass('fixed-header');
        }

        if ($(this).scrollTop() >= 200 && $(window).width() > 992) {
            $('.fixed-header2').addClass('show-fixed-header2');
            $('.header2').css('visibility', 'hidden');
            $('.header2').find('.header-dropdown').removeClass("show-header-dropdown");

        } else {
            $('.fixed-header2').removeClass('show-fixed-header2');
            $('.header2').css('visibility', 'visible');
            $('.fixed-header2').find('.header-dropdown').removeClass("show-header-dropdown");
        }

    });

    /*[ Show menu mobile ]
    ===========================================================*/
    $('.btn-show-menu-mobile').on('click', function() {
        $(this).toggleClass('is-active');
        $('.wrap-side-menu').slideToggle();
    });

    var arrowMainMenu = $('.arrow-main-menu');

    for (var i = 0; i < arrowMainMenu.length; i++) {
        $(arrowMainMenu[i]).on('click', function() {
            $(this).parent().find('.sub-menu').slideToggle();
            $(this).toggleClass('turn-arrow');
        })
    }

    $(window).resize(function() {
        if ($(window).width() >= 992) {
            if ($('.wrap-side-menu').css('display') == 'block') {
                $('.wrap-side-menu').css('display', 'none');
                $('.btn-show-menu-mobile').toggleClass('is-active');
            }
            if ($('.sub-menu').css('display') == 'block') {
                $('.sub-menu').css('display', 'none');
                $('.arrow-main-menu').removeClass('turn-arrow');
            }
        }
    });


    /*[ remove top noti ]
    ===========================================================*/
    $('.btn-romove-top-noti').on('click', function() {
        $(this).parent().remove();
    })


    /*[ Block2 button wishlist ]
    ===========================================================*/
    $('.block2-btn-addwishlist').on('click', function(e) {
        e.preventDefault();
        $(this).addClass('block2-btn-towishlist');
        $(this).removeClass('block2-btn-addwishlist');
        $(this).off('click');
    });

    /*[ +/- num product ]
    ===========================================================*/
    $('.btn-num-product-down').on('click', function(e) {
        e.preventDefault();
        var numProduct = Number($(this).next().val());
        if (numProduct > 1) $(this).next().val(numProduct - 1);
    });

    $('.btn-num-product-up').on('click', function(e) {
        e.preventDefault();
        var numProduct = Number($(this).prev().val());
        $(this).prev().val(numProduct + 1);
    });


    /*[ Show content Product detail ]
    ===========================================================*/
    $('.active-dropdown-content .js-toggle-dropdown-content').toggleClass('show-dropdown-content');
    $('.active-dropdown-content .dropdown-content').slideToggle('fast');

    $('.js-toggle-dropdown-content').on('click', function() {
        $(this).toggleClass('show-dropdown-content');
        $(this).parent().find('.dropdown-content').slideToggle('fast');
    });


    /*[ Play video 01]
    ===========================================================*/
    var srcOld = $('.video-mo-01').children('iframe').attr('src');

    $('[data-target="#modal-video-01"]').on('click', function() {
        $('.video-mo-01').children('iframe')[0].src += "&autoplay=1";

        setTimeout(function() {
            $('.video-mo-01').css('opacity', '1');
        }, 300);
    });

    $('[data-dismiss="modal"]').on('click', function() {
        $('.video-mo-01').children('iframe')[0].src = srcOld;
        $('.video-mo-01').css('opacity', '0');
    });

})(jQuery);