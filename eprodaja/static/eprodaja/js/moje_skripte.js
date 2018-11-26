$(document).ready(function () {
    $('#messagemodal').modal('show');
	$("#kupi").click(function() {
		$('.modal').modal('show');
	});
	// napravi modal i prikazi
	jQuery(document.body).on('click touch', '.artikal_detail', function(e) {
		e.preventDefault();
		$("#modal-artikal").html("");
		var artikal_id = $(this).attr('id');
		$.ajax({
			context: this,
			url: '/create_modal/',
			data: {
				   'artikal_id': artikal_id
			},
			dataType: 'json',
			success: function (data) {
				//console.log(data);
				var modal_line = '<div class="modal-dialog" role="document"> \
									<div class="modal-content"> \
									  <div class="modal-header"> \
										<h5 class="modal-title"></h5> \
										  <p>Artikal ID: #'+data[0][0].id+'</p> \
									  </div> \
									  <div class="modal-body"> \
										<img width="360" height="360" class="velika_slika glavna_slika" src="/media/' + data[0][0].slika + '" alt="" /> \
										  <div class="image-grid"> \
											  <a class="mala_slika image" href="/media/' + data[0][0].slika + '"><img width="60" height="60" src="/media/' + data[0][0].slika + '" alt=""></a>';
												for (j = 0; j < data[1].length; j++){
													var imageLine = '<a class="mala_slika image" data-id="data[1][j].id" href="/media/' + data[1][j].slika + '"><img width="60" height="60" src="/media/' + data[1][j].slika + '" alt=""></a>';
												  	modal_line = modal_line + imageLine;
												}
				lineRest = '							</div> \
										<h4>'+ data[0][0].opis +'</h4> \
										<h3>'+ data[0][0].cena +' din</h3> \
									  </div> \
									  <div class="modal-footer"> \
										<button type="button" class="btn btn-secondary" data-dismiss="modal">Nazad</button> \
									  </div> \
									</div> \
								  </div> \
								</div>';
				modal_line = modal_line + lineRest;
				$("#modal-artikal").append(modal_line);
			}
	    });
		$("#modal-artikal").modal('show');
	});
	// male slike
	jQuery(document.body).on('click touch', '.mala_slika', function(e) {
		e.preventDefault();
		var nova_putanja = $(this).children('img').attr('src');
		var $imageContainer = $(this).parent().prev('.velika_slika');
		$imageContainer.attr('src', nova_putanja);
	});
	// dodaj proizvod u korpu
    jQuery(document.body).on('click touch', '.u_korpu', function() {
		var artikal_id = this.id;
		$.ajax({
			context: this,
			url: '/dodaj_artikal/',
			data: {
				   'artikal_id': artikal_id
			},
			dataType: 'json',
			success: function (data) {
				if (data.error) {
					window.location = '/logovanje/';
				} else{
					$('html, body').animate({
						'scrollTop' : $("#korpa").position().top
					});

					var itemImg = $(this).parent().parent().find('img').eq(0);
					flyToElement($(itemImg), $('#korpa'));
					$("#korpa").html(data.proizvoda_u_korpi);
					$(this).hide();
				}
			}
		});
    });
	$('.pretraga').on("contextmenu",function(){
       return false;
    });
    $('.pretraga').on("click touch",function(){
		var artikli_za_filter =  $(this).data("id");
		$.ajax({
			context: this,
			url: '/filter/',
			data: {
				   'artikli_za_filter': artikli_za_filter
			},
			dataType: 'json',
			success: function (data) {
				$("#filter_artikli").html("");
				if (data.length > 0) {
					$("#filter_artikli").css('paddingBottom', '0px');
					for (i = 0; i < data.length; i++){
						var line = '<div class="col-md-3 col-sm-6 col-xs-6"> \
                                        <div class="product-image-wrapper"> \
                                            <div class="productinfo text-center"> \
                                                <a class="artikal_detail" href="/media/' + data[i].slika + '" id="'+data[i].id+'"> \
                                                <img src="/media/' + data[i].slika + '" alt="" /> \
                                                </a> \
                                                <h2>' + data[i].cena.toFixed(1) + 'din</h2> \
                                                    <p>' + data[i].opis + '</p> \
                                            </div> \
                                            <button id="' + data[i].id + '" class="u_korpu btn btn-default add-to-cart" type="submit" value="U korpu"><i class="fa fa-shopping-cart input_span"></i> U korpu</button> \
                                        </div> \
                                    </div>';
						$("#filter_artikli").append(line);
						//console.log(data[i].cena.toFixed(2));
					}
				}
				else{
					$("#filter_artikli").css('paddingBottom', '450px');
					var line = '<h4 class="title text-center">Trenutno nema proizvoda u ovoj sekciji</h4>';
					$("#filter_artikli").append(line);
				}
			}
        });
        $(this).effect('highlight',{color: '#ffaa02'},1500);
    });

	$('#main-contact-form-search').submit(function (e) {
		e.preventDefault();
		$("#pretrazi_artikle").click();
	});
    $('#pretrazi_artikle').on("click touch",function(){
    	var pretraga = $('input[name=pretraga_svih_artikala]').val();
    	$('input[name=pretraga_svih_artikala]').val("");
    	$.ajax({
			context: this,
			url: '/pretraga/',
			data: {
				   'pretraga': pretraga,
			},
			dataType: 'json',
			success: function (data) {
				$("#filter_artikli").html("");
				if (data.length > 0) {
					for (i = 0; i < data.length; i++){
						var line = '<div class="col-md-3 col-sm-6 col-xs-6"> \
                                        <div class="product-image-wrapper"> \
                                            <div class="productinfo text-center"> \
                                                <a class="artikal_detail" href="/media/' + data[i].slika + '" id="'+data[i].id+'"> \
                                                <img src="/media/' + data[i].slika + '" alt="" /> \
                                                </a> \
                                                <h2>' + data[i].cena.toFixed(1) + 'din</h2> \
                                                    <p>' + data[i].opis + '</p> \
                                            </div> \
                                            <button id="' + data[i].id + '" class="u_korpu btn btn-default add-to-cart" type="submit" value="U korpu"><i class="fa fa-shopping-cart input_span"></i> U korpu</button> \
                                        </div> \
                                    </div>';
						$("#filter_artikli").append(line);
					}

				}
				else{
					$("#filter_artikli").css('paddingBottom', '450px');
					var line = '<h4 class="title text-center">Trenutno nema proizvoda za traženi kriterijum</h4>';
					$("#filter_artikli").append(line);
				}
			}
        });
    });
    //
    $('#button_xs').on("click touch",function(){
    $("#mySidenav").removeClass("hidden-xs");
    $("#mySidenav").removeClass("hidden-sm");
    $('html, body').animate({scrollTop: $('#accordian').offset().top -100 }, 'slow');
    });
    moveScroller();

});
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";
    document.body.style.backgroundColor = "white";
}
function goBack() {
    window.history.back();
}

function moveScroller() {
    var $anchor = $("#scroller-anchor");
    var $scroller = $('#button_xs');

    var move = function() {
        var st = $(window).scrollTop();
        var ot = $anchor.offset().top;
        if(st > ot) {
            $scroller.css({
                position: "fixed",
                top: "0"
            });
        } else {
            $scroller.css({
                position: "relative",

            });
        }
    };
    $(window).scroll(move);
    move();
}
