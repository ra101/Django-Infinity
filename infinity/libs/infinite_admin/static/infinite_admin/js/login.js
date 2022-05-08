;!(function(){
    $(document).ready(function(){
        $('.captcha').click(function(){
            var captcha_image = $(this);
            var captcha_refresh_url = captcha_image.parent().attr("captcha-refresh-url");
            console.log(captcha_refresh_url);
            $.getJSON(captcha_refresh_url, function (result) {
                captcha_image.attr('src', result['image_url']);
                $('#id_captcha_0').val(result['key'])
            });
        });
    });
})(jQuery);
