$(function () {
    $(window).on('scroll', function () {
        if ( $(window).scrollTop() > 10 ) {
            $('.navbar').addClass('active');
        } else {
            $('.navbar').removeClass('active');
        }
    });
});
$(function(){
    $('#hesap').on('click', function(){
        var kitap_sayfa_sayisi = document.getElementById('kitap').value;
        var okunan_sayfa_sayisi = document.getElementById('okunan').value;
        var kalan_miktar = kitap_sayfa_sayisi - okunan_sayfa_sayisi;
        var yuzde_hesapla = (100*kalan_miktar)/kitap_sayfa_sayisi;
        document.getElementById('count').innerHTML = yuzde_hesapla;
        var count = $(('#count'));
        $({ Counter: 0 }).animate({ Counter: count.text() }, {
        duration: 5000,
        easing: 'linear',
        step: function () {
            count.text(Math.ceil(this.Counter)+ "%");
        }
        });
    
        var s = Snap('#animated');
        var progress = s.select('#progress');
    
        progress.attr({strokeDasharray: '0, 251.2'});
        Snap.animate(0,251.2, function( value ) {
            progress.attr({ 'stroke-dasharray':value+',251.2'});
        }, 5000);
      });
   
});
