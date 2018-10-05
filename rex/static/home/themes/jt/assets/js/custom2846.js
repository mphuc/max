// Set some variables
	// default logo top margin - will use it for on scroll header minimizer
	def_logo_top_margin = jQuery('.brand img').css('margin-top');
	def_logo_max_height = jQuery('.brand img').css('max-height');
	if ( def_logo_max_height == 'none' ) {
		def_logo_max_height = '95px';
	}

// Tour Tabs
//=======================================
jQuery(document).ready(function() {
	/*jQuery('.nav-list').each(function() {
		jQuery(this).find('li:first').addClass('first');
		jQuery(this).find('li:last').addClass('last');
	});
	jQuery('.sf-menu > .current-menu-item').addClass('nav-active');
	jQuery('.sf-menu > .current-menu-parent').addClass('nav-active');
	jQuery('.sf-menu > .current-page-ancestor').addClass('nav-active');
	jQuery('.wpb_carousel').addClass('content-bubble drop-shadow curved');*/
});

// Tool Tip
//=======================================
jQuery("[rel=alternate]").tooltip()
jQuery(".icons").tooltip()

// Drop Down Menu
//=======================================
jQuery('.dropdown-toggle').dropdown()

// Features Hover Bubble
//=======================================
jQuery(document).ready(function() {
   jQuery(".features").hover(
   	function () {
   		   jQuery(this).addClass("features-active");
   	
   	}
   );
   jQuery(".features").hover(
   	function () {
   			jQuery('.features').removeClass("features-active");
   		   jQuery(this).addClass("features-active");
   	
   	}
   );
});

// Tabs 
//=======================================
jQuery('#myTab a').click(function (e) {
	e.preventDefault();
	jQuery(this).tab('show');
})

jQuery('#tabs a').click(function (e) {
	e.preventDefault();
	jQuery(this).tab('show');
})

// Contact Form
//=======================================
jQuery('#submit').click(function() {
	
	var name = jQuery("#name").val();
	var email = jQuery("#email").val();
	var message = jQuery("#message").val();
	
	var dataString = 'name='+ name + '&email=' + email + '&message=' + message;  
	//alert (dataString);return false;  
	jQuery.ajax({  
	  type: "POST",  
	  url: "contact.php",  
	  data: dataString,  
	  success:  function (html) { 
	  	if (html == "invalid_email ") {
	  		jQuery('.contact-alerts').empty();
	  		jQuery('.contact-alerts').append('<div id="email-error" class="alert alert-error">This email is invalid!</div>');
	  	} else if (html == "success ") {
	 		jQuery('.contact-alerts').empty();
			jQuery('.contact-alerts').append('<div id="email-success" class="alert alert-success">Your email has been sent!</div>');
	  	} else if (html == "error ") {
	  		jQuery('.contact-alerts').empty();
	  		jQuery('.contact-alerts').append('<div id="email-error" class="alert alert-error">Please fill out all the fields!</div>');
	  	}

	  }  
	});  
});

// Style Switcher
//=======================================
jQuery(document).ready(function() {
	jQuery('#navigation > li ').toggle(function() {
		jQuery('span,#panel',jQuery(this)).stop().animate({'marginLeft':'-145px'},200);
	},function(){
		jQuery('span,#panel',jQuery(this)).stop().animate({'marginLeft':'0px'},200);
	});
});
 
// Vertical Align Function
//=======================================
 (function ($) {
	 $.fn.vAlign = function() {
		return this.each(function(i){
		var ah = $(this).height();
		var ph = $(this).parent().height();
		var mh = Math.ceil((ph-ah) / 2);
		$(this).css('margin-top', mh);
		});
	 };
 })(jQuery);
 
jQuery(window).load(function() {
	jQuery('.vcenter').vAlign();
	
	// Initialize flexslider for portfolio
	jQuery('.portfolio_flexsliders').flexslider({
		animation: "slide",
		slideshowSpeed: 5000,
		prevText: "&#xe011;",
		nextText: "&#xe014;",
		pauseOnHover: true,
		controlNav: false,
		smoothHeight: false
	});	
});
 
 jQuery(window).resize(function(){
 	jQuery('.vcenter').vAlign();
});
 
// TinyNav, Dropkick
//=======================================

jQuery(document).ready(function() {
	jQuery(function () {
		jQuery(".navbar .nav").tinyNav();
	});
	  
	jQuery(document).ready(function() {
		jQuery('.dk_toggle').css('width','170px');
		// Find current page
		var current_Menu_Item = jQuery('.current-menu-item').find('a').attr('href');
		var is_404_or_no_menu = true;
		jQuery('#tinynav1').find('option').each(function() {
			if (jQuery(this).val() == current_Menu_Item) {
				jQuery(this).attr('selected','selected');
				is_404_or_no_menu = false;
			}
		});
		if ( is_404_or_no_menu == true ) {
			var nav_choose_text = tmq_script_vars.nav_choose_text;
			jQuery('#tinynav1').prepend('<option selected="selected">'+ nav_choose_text +'</option>');
		}
	});
	
});
   
// Nav-active Arrow
//=======================================
jQuery('.nav-active').prepend('<i class="nav-active-arrow"></i>');
jQuery('.sf-menu > .current-menu-item').prepend('<i class="nav-active-arrow"></i>');
jQuery('.sf-menu > .current-menu-parent').prepend('<i class="nav-active-arrow"></i>');
jQuery('.widget_nav_menu ul').addClass('nav nav-list');
jQuery('.widget_nav_menu ul .current-menu-item').addClass('active');

// For pages that are not in menu but you want to show parent in highlight mode
jQuery('.sf-menu > .current-page-ancestor').addClass('nav-active');
jQuery('.sf-menu > .current-page-ancestor').prepend('<i class="nav-active-arrow"></i>');

// Fancy Box
//=======================================   
jQuery(document).ready(function() {
	jQuery(".fancybox").fancybox({
	helpers : {
	    overlay : {
	        locked : false
	    }
	},

	padding: ['5px', '5px', '5px', '5px']
	});
});

// Goto Top
//=======================================   
jQuery(window).scroll(function() {
	// Initialize it on 250px from top;
	var tmq_small_header = tmq_script_vars.small_header;	
	// Goto top button config
	if ( jQuery(window).scrollTop() > 250 ) {
		jQuery('.gototop').fadeIn(300);

		// Prevent scroll to top override with social elements
		var fooffset = jQuery('.footer').offset().top;
		var gotoffset = jQuery('.gototop').offset().top;

		if (gotoffset >= fooffset - 100) {
			jQuery('.w1170px .gototop').css({'bottom': '80px'});
		}
		if (gotoffset <= fooffset - 200) {
			jQuery('.w1170px .gototop').css({'bottom': '30px'});
		}
		// End Prevent!
		var tmq_fullwidthmenu = jQuery('.full-width-menu-header');
		if ( ( tmq_small_header == 'tmq_enable' || tmq_small_header == 'on' ) && tmq_fullwidthmenu.length == 0 ) {
			// Check if this option is enabled in OT
			if (jQuery(window).width() > 767) {
				// Header Minimizer
				jQuery('.sf-menu > li > a').css({'padding': '15px 15px 15px'});
				jQuery('.navbar-inner').css({'min-height': '50px'});
				jQuery('.navbar-inner').css({'height': '50px'});
				jQuery('.nav-active-arrow').css({'top': '50px'});
				jQuery('.brand img').css({'margin-top': '10px'});
				jQuery('.brand img').css({'max-height': '30px'});
			}
		}
	} else {
		jQuery('.gototop').fadeOut(300);
		var tmq_fullwidthmenu = jQuery('.full-width-menu-header');
		if ( ( tmq_small_header == 'tmq_enable' || tmq_small_header == 'on' ) && tmq_fullwidthmenu.length == 0 ) {	
			if (jQuery(window).width() > 767) {
				// Header Back to Default
				jQuery('.sf-menu > li > a').css({'padding': '38px 15px 38px'});
				jQuery('.navbar-inner').css({'min-height': '95px'});
				jQuery('.navbar-inner').css({'height': '95px'});
				jQuery('.nav-active-arrow').css({'top': '95px'});
				jQuery('.brand img').css({'margin-top': def_logo_top_margin});
				jQuery('.brand img').css({'max-height': def_logo_max_height});
			} else {
				// Reset for small screens
				jQuery('.sf-menu > li > a').css({'padding': '38px 15px 38px'});
				jQuery('.navbar-inner').css({'min-height': '95px'});
				jQuery('.navbar-inner').css({'height': 'auto'});
				jQuery('.nav-active-arrow').css({'top': '95px'});
				jQuery('.brand img').css({'margin-top': def_logo_top_margin});
				jQuery('.brand img').css({'max-height': def_logo_max_height});			
			}
		}
	}
});

jQuery(document).ready(function() {
	jQuery('.gototop').click(function() {
		  jQuery('html, body').animate({ scrollTop: 0 }, 1000 );
		  return false;
	});
});

// Prettify
//=======================================
jQuery(document).ready(function() {
	prettyPrint();
});

// Nice Scroll
//=======================================
jQuery(document).ready(function() {
	// Check if NiceScroll is enabled
	if (tmq_script_vars.nicescroll == 'smooth') {
		jQuery("html").niceScroll({
			autohidemode: true,
			cursorborder: 1,
			cursorborderradius: 10,
			cursorcolor: '#444',
			cursorwidth: 10,
			mousescrollstep: 40,
			scrollspeed: 70,
			horizrailenabled: false
		});
	}
});


// Menu Chooser
//=======================================
jQuery(document).ready(function() {

});



// Superfish Menu
//=======================================   
(function($){ //create closure so we can safely use $ as alias for jQuery

	$(document).ready(function(){

		// initialise plugin
		var example = $('#header-menu').superfish({
			//add options here if required
		});

		// buttons to demonstrate Superfish's public methods
		$('.destroy').on('click', function(){
			example.superfish('destroy');
		});

		$('.init').on('click', function(){
			example.superfish();
		});

		$('.open').on('click', function(){
			example.children('li:first').superfish('show');
		});

		$('.close').on('click', function(){
			example.children('li:first').superfish('hide');
		});
	});

})(jQuery);

// Share This Buttons
function tmq_shareThis(site,url) {
	var shareWindow=null;
	switch (site) {
		case 'facebook':
			site = 'http://www.facebook.com/sharer.php?u=';
			break;
		case 'twitter':
			site = 'https://twitter.com/intent/tweet?original_referer=';
			break;
		case 'google':
			site = 'https://plus.google.com/share?url=';
			break;
		case 'pinterest':
			site = 'http://pinterest.com/pin/create/button/?url=';
			break;
		case 'linkedin':
			site = 'https://www.linkedin.com/shareArticle?url=';
			break;
		case 'reddit':
			site = 'http://www.reddit.com/submit?url=';
			break;
		case 'stumbleupon':
			site = 'http://www.stumbleupon.com/submit?url=';
			break;
		case 'delicious':
			site = 'http://delicious.com/save?v=5&noui&jump=close&url=';
			break;
		default:
			break;
	}
	shareWindow = window.open(site + encodeURI(url) ,'shareThis','width=640,height=380');
}
