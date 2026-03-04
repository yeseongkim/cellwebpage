(function(jQuery) { "use strict";


	// acordian FAQ
	jQuery('.head').click(function() {
	  jQuery(this).toggleClass('active');
	  jQuery(this).parent().find('.arrow').toggleClass('arrow-animate');
	  jQuery(this).parent().find('.content').slideToggle(280);
	});
	
	// parallax
	jQuery(window).scroll(function() {
			var scrollDistance = jQuery(window).scrollTop();

			// Show/hide menu on scroll
			//if (scrollDistance >= 850) {
			//		jQuery('nav').fadeIn("fast");
			//} else {
			//		jQuery('nav').fadeOut("fast");
			//}
		
			// Assign active class to nav links while scolling
			jQuery('.section').each(function(i) {
				if (jQuery(this).position().top <= scrollDistance) {
					jQuery('.menu li.active').removeClass('active');
					jQuery('.menu li').eq(i).addClass('active');
				}
			});
	}).scroll();
	
	
	//Serch
	jQuery('.header').on('click', '.search-toggle', function(e) {
	  var selector = jQuery(this).data('selector');

	  jQuery(selector).toggleClass('show').find('.search-input').focus();
	  jQuery(this).toggleClass('active');

	  e.preventDefault();          
	});
	
	
	//Menu On Hover
		
	jQuery('body').on('mouseenter mouseleave','.nav-item',function(e){
			if (jQuery(window).width() > 750) {
				var _d=jQuery(e.target).closest('.nav-item');_d.addClass('show');
				setTimeout(function(){
				_d[_d.is(':hover')?'addClass':'removeClass']('show');
				},1);
			}
	});	
	
	jQuery('.dropdown-submenu a').click(function() {

       jQuery('.dropdown-submenu').toggleClass('show');
		return false;
	});
		
	// Scroll to down anchor                
	jQuery(function() {
		jQuery('.scroll-down').click (function() {
		  jQuery('html, body').animate({scrollTop: jQuery('section.service').offset().top }, 'slow');
		  return false;
		});
	});
	
	/* ---------------------------------------------- /*
	* Scroll top
	/* ---------------------------------------------- */

	jQuery(window).scroll(function() {
		if (jQuery(this).scrollTop() > 100) {
			jQuery('.page-scroll-up').fadeIn();
		} else {
			jQuery('.page-scroll-up').fadeOut();
		}
	});
	
	jQuery('.page-scroll-up').click(function () {
		jQuery("html, body").animate({
			scrollTop: 0
		}, 700);
		return false;
	});

	/* ---------------------------------------------- /*
	* Loader
	/* ---------------------------------------------- */
	
	setTimeout(function() {
		jQuery('body').addClass('loaded');
	}, 3500);
			
			

	/* ---------------------------------------------- /*
	* Slider Particle JS
	/* ---------------------------------------------- */

	jQuery(window).load(function() {
		//Particle js
		   /*----- Particles JS Config -----*/
		var particles = jQuery('#particles-js');
		if(particles.length) {

			particlesJS("particles-js", {
				"particles": {
					"number": {
						"value": 50,
						"density": {
							"enable": true,
							"value_area": 800
						}
					},
					"color": {
						"value": "#ffffff"
					},
					"shape": {
						"type": "circle",
						"stroke": {
							"width": 0,
							"color": "#000000"
						},
						"polygon": {
							"nb_sides": 5
						},
						"image": {
							"src": "img/github.svg",
							"width": 100,
							"height": 100
						}
					},
					"opacity": {
						"value": 0.5,
						"random": false,
						"anim": {
							"enable": false,
							"speed": 1,
							"opacity_min": 0.1,
							"sync": false
						}
					},
					"size": {
						"value": 3,
						"random": true,
						"anim": {
							"enable": false,
							"speed": 40,
							"size_min": 0.1,
							"sync": false
						}
					},
					"line_linked": {
						"enable": true,
						"distance": 150,
						"color": "#ffffff",
						"opacity": 0.4,
						"width": 1
					},
					"move": {
						"enable": true,
						"speed": 4,
						"direction": "none",
						"random": false,
						"straight": false,
						"out_mode": "out",
						"bounce": false,
						"attract": {
							"enable": false,
							"rotateX": 600,
							"rotateY": 1200
						}
					}
				},
				"interactivity": {
					"detect_on": "window",
					"events": {
						"onhover": {
							"enable": false,
							"mode": "push"
						},
						"onclick": {
							"enable": false,
							"mode": "push"
						},
						"resize": true
					},
					"modes": {
						"grab": {
							"distance": 400,
							"line_linked": {
								"opacity": 1
							}
						},
						"bubble": {
							"distance": 400,
							"size": 40,
							"duration": 2,
							"opacity": 8,
							"speed": 3
						},
						"repulse": {
							"distance": 200,
							"duration": 0.4
						},
						"push": {
							"particles_nb": 4
						},
						"remove": {
							"particles_nb": 2
						}
					}
				},
				"backgroundMode": {
					"zIndex": 100, // any value >= 0 is good
					/* if you want elements above particles 
					   just set a bigger z-index in your css */
					"enable": false
				  },
				"retina_detect": false
			});

		}
	});

 })(jQuery);