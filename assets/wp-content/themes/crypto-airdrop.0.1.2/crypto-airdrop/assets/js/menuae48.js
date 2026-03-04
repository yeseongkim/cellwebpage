(function() {
	// Check if target matches to an element.
	function cryptoairdropTargetMatches(selector) {
		return event.target.matches ? event.target.matches(selector) : event.target.msMatchesSelector(selector);
	}

	// Get next sibling.
	function cryptoairdropNextSibling(element) {
		do {
			element = element.nextSibling;
		} while (element && element.nodeType !== 1);
		return element;
	}

	// Handle sub-menu arrow clicks.
	function cryptoairdropSubMenuArrowClick(subMenuArrow, subMenuArrows, subMenus) {
		var cryptoairdropSubMenu = cryptoairdropNextSibling(subMenuArrow);
		if(cryptoairdropSubMenu) {
			// Accessibility support for dropdown menu.
			var cryptoairdropSubMenuLink = subMenuArrow.previousSibling;

			cryptoairdropSetTabIndex(subMenus, -1);

			if(cryptoairdropSubMenu.classList.contains('sub-menu--open')) {
				subMenuArrow.classList.remove('sub-menu-show');
				cryptoairdropSubMenu.classList.remove('sub-menu--open');
				cryptoairdropSubMenuLink.setAttribute('aria-expanded', 'false');
				subMenuArrow.getElementsByClassName('menu-arrow-button-hide')[0].setAttribute('aria-hidden', 'true');
				subMenuArrow.getElementsByClassName('menu-arrow-button-show')[0].setAttribute('aria-hidden', 'false');
			} else {
				if(subMenus.length) {
					[].forEach.call(subMenus, function(el) {
						el.classList.remove('sub-menu--open');
					});
				}
				if(subMenuArrows.length) {
					for(var i = 0; i < subMenuArrows.length; i++) {
						subMenuArrows[i].classList.remove('sub-menu-show');
						subMenuArrows[i].previousSibling.setAttribute('aria-expanded', 'false');
						subMenuArrows[i].getElementsByClassName('menu-arrow-button-hide')[0].setAttribute('aria-hidden', 'true');
						subMenuArrows[i].getElementsByClassName('menu-arrow-button-show')[0].setAttribute('aria-hidden', 'false');
					}
				}

				subMenuArrow.classList.add('sub-menu-show');
				cryptoairdropSubMenu.classList.add('sub-menu--open');
				cryptoairdropSubMenuLink.setAttribute('aria-expanded', 'true');
				subMenuArrow.getElementsByClassName('menu-arrow-button-hide')[0].setAttribute('aria-hidden', 'false');
				subMenuArrow.getElementsByClassName('menu-arrow-button-show')[0].setAttribute('aria-hidden', 'true');
				cryptoairdropSetTabIndex(cryptoairdropSubMenu, 0);
				cryptoairdropSetTabIndex(cryptoairdropSubMenu.querySelectorAll('.sub-menu'), -1);
			}
		}
	}

	// Setup mobile menu.
	function cryptoairdropMobileMenu() {
		document.addEventListener('click', function(event) {
			if(cryptoairdropTargetMatches('.menu-toggle')) {
				event.preventDefault();
				var cryptoairdropNavIcon = event.target || event.srcElement;
				var cryptoairdropMainNav = document.querySelector('.main-navigation > .primary-menu-container');

				// Slide mobile menu.
				cryptoairdropNavIcon.classList.toggle('menu-toggle--open');
				cryptoairdropMainNav.classList.toggle('primary-menu-container--open');

				if(cryptoairdropNavIcon.classList.contains('menu-toggle--open')) {
					cryptoairdropNavIcon.setAttribute('aria-expanded', 'true');
					cryptoairdropSetTabIndex(document.querySelector('.main-navigation .menu'), 0);
					cryptoairdropSetTabIndex(document.querySelectorAll('.main-navigation .sub-menu'), -1);
				} else {
					cryptoairdropNavIcon.setAttribute('aria-expanded', 'false');
				}

			} else if(cryptoairdropTargetMatches('.main-navigation .menu .sub-menu li.menu-item-has-children > .menu-arrow-button')) {
				event.preventDefault();
				var cryptoairdropSubMenuArrow1 = event.target || event.srcElement;

				var cryptoairdropSubMenuArrows1 = document.querySelectorAll('.main-navigation .menu .sub-menu > li.menu-item-has-children > .menu-arrow-button');
				var cryptoairdropSubMenus1 = document.querySelectorAll('.main-navigation .menu .sub-menu > li.menu-item-has-children > .sub-menu');

				cryptoairdropSubMenuArrowClick(cryptoairdropSubMenuArrow1, cryptoairdropSubMenuArrows1, cryptoairdropSubMenus1);

			} else if(cryptoairdropTargetMatches('.main-navigation .menu li.menu-item-has-children > .menu-arrow-button')) {
				event.preventDefault();
				var cryptoairdropSubMenuArrow2 = event.target || event.srcElement;

				var cryptoairdropSubMenuArrows2 = document.querySelectorAll('.main-navigation .menu > li.menu-item-has-children > .menu-arrow-button');
				var cryptoairdropSubMenus2 = document.querySelectorAll('.main-navigation .menu > li.menu-item-has-children > .sub-menu');

				cryptoairdropSubMenuArrowClick(cryptoairdropSubMenuArrow2, cryptoairdropSubMenuArrows2, cryptoairdropSubMenus2);

			} else {
				var cryptoairdropSubMenuArrows3 = document.querySelectorAll('.main-navigation .menu > li.menu-item-has-children > .menu-arrow-button');
				var cryptoairdropSubMenus3 = document.querySelectorAll('.main-navigation .menu > li.menu-item-has-children > .sub-menu');
				if(cryptoairdropSubMenus3.length) {
					[].forEach.call(cryptoairdropSubMenus3, function(el) {
						el.classList.remove('sub-menu--open');
					});
				}
				if(cryptoairdropSubMenuArrows3.length) {
					for(var i = 0; i < cryptoairdropSubMenuArrows3.length; i++) {
						cryptoairdropSubMenuArrows3[i].classList.remove('sub-menu-show');
						cryptoairdropSubMenuArrows3[i].previousSibling.setAttribute('aria-expanded', 'false');
						cryptoairdropSubMenuArrows3[i].getElementsByClassName('menu-arrow-button-hide')[0].setAttribute('aria-hidden', 'true');
						cryptoairdropSubMenuArrows3[i].getElementsByClassName('menu-arrow-button-show')[0].setAttribute('aria-hidden', 'false');
					}
				}
				cryptoairdropSetTabIndex(document.querySelectorAll('.main-navigation .sub-menu'), -1);
			}
		});
	}

	// Mobile menu.
	cryptoairdropMobileMenu();

	var cryptoairdropFocusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';

	// Set tabindex of focusable elements.
	function cryptoairdropSetTabIndex(element, value) {
		if(NodeList.prototype.isPrototypeOf(element)) {
			[].forEach.call(element, function(el) {
				[].forEach.call(el.querySelectorAll(cryptoairdropFocusableElements), function(el) {
					el.setAttribute('tabindex', value);
				});
			});

		} else {
			[].forEach.call(element.querySelectorAll(cryptoairdropFocusableElements), function(el) {
				el.setAttribute('tabindex', value);
			});
		}
	}

	cryptoairdropSetTabIndex(document.querySelectorAll('.main-navigation .sub-menu'), -1);

	document.addEventListener('keydown', function(event) {
		var cryptoairdropIsTabPressed = ('Tab' === event.key || 9 === event.keyCode);
		if(!cryptoairdropIsTabPressed) {
			return;
		}

		var cryptoairdropNavIcon = document.querySelector('.menu-toggle');
		if(cryptoairdropNavIcon && ('none' !== getComputedStyle(cryptoairdropNavIcon, null).display)) {
			if(!cryptoairdropNavIcon.classList.contains('menu-toggle--open')) {
				cryptoairdropSetTabIndex(document.querySelector('.main-navigation .menu'), -1);
			}

			if(!event.shiftKey) {
				if(!document.activeElement.classList || !document.activeElement.classList.contains('sub-menu-show')) {
					var cryptoairdropActiveElementArrow = cryptoairdropNextSibling(document.activeElement);
					if(!cryptoairdropActiveElementArrow || (cryptoairdropActiveElementArrow.classList && !cryptoairdropActiveElementArrow.classList.contains('menu-arrow-button'))) {
						var cryptoairdropActiveElementSibling = cryptoairdropNextSibling(document.activeElement.parentNode);
						if(!cryptoairdropActiveElementSibling && document.activeElement.parentNode.parentNode.id && 'primary-menu' === document.activeElement.parentNode.parentNode.id) {
							var cryptoairdropMenuFocusableElements = document.activeElement.parentNode.parentNode.querySelectorAll(cryptoairdropFocusableElements);
							if(cryptoairdropMenuFocusableElements.length > 0) {
								event.preventDefault();
								cryptoairdropNavIcon.focus();
							}
						}
					}
				}
			} else {
				if(document.activeElement.classList && document.activeElement.classList.contains('menu-toggle--open')) {
					var cryptoairdropLastMenuItemArrowButton = document.querySelector('.main-navigation .menu > li:last-child > .menu-arrow-button');
					if(cryptoairdropLastMenuItemArrowButton) {
						cryptoairdropLastMenuItemArrowButton.focus();
						event.preventDefault();
					} else {
						var cryptoairdropLastMenuItemAnchor = document.querySelector('.main-navigation .menu > li:last-child > a');
						if(cryptoairdropLastMenuItemAnchor) {
							cryptoairdropLastMenuItemAnchor.focus();
							event.preventDefault();
						}
					}
				}
			}
		}

		if(!event.shiftKey) {
			if(!document.activeElement.classList || !document.activeElement.classList.contains('sub-menu-show')) {
				var cryptoairdropActiveElementArrow = cryptoairdropNextSibling(document.activeElement);
				if(!cryptoairdropActiveElementArrow || (cryptoairdropActiveElementArrow.classList && !cryptoairdropActiveElementArrow.classList.contains('menu-arrow-button'))) {
					var cryptoairdropActiveElementSibling = cryptoairdropNextSibling(document.activeElement.parentNode);
					if(!cryptoairdropActiveElementSibling && document.activeElement.parentNode.parentNode.classList && document.activeElement.parentNode.parentNode.classList.contains('sub-menu--open')) {
						var subMenuFocusableElements = document.activeElement.parentNode.parentNode.querySelectorAll(cryptoairdropFocusableElements);
						if(subMenuFocusableElements.length > 0) {
							event.preventDefault();
							subMenuFocusableElements[0].focus();
						}
					}
				}
			}
		}
	});

	// Sticky menu.
	var cryptoairdropMainMenuSticky = document.querySelector('.site-menu-content--sticky');
	if(cryptoairdropMainMenuSticky) {
		var cryptoairdropAfterMainMenu = cryptoairdropNextSibling(cryptoairdropMainMenuSticky);
		if(cryptoairdropAfterMainMenu) {
			var cryptoairdropSiteContent = cryptoairdropAfterMainMenu;
		} else {
			var cryptoairdropSiteContent = document.getElementById('site-content');
		}

		var cryptoairdropSiteContentMarginTop = window.getComputedStyle(cryptoairdropSiteContent, null).marginTop;

		var cryptoairdropStickyMenuHeight = cryptoairdropMainMenuSticky.offsetHeight;
		var cryptoairdropStickyMenuClass = 'sticky-menu';
		var cryptoairdropStickyMenuInViewClass = 'sticky-menu-in-view';
		var cryptoairdropHeaderHeight = document.querySelector('.site-menu-content').offsetHeight;
		window.addEventListener('scroll', function() {
			if(window.pageYOffset > cryptoairdropHeaderHeight) {
				cryptoairdropMainMenuSticky.classList.add(cryptoairdropStickyMenuClass);
				cryptoairdropSiteContent.style.marginTop = cryptoairdropStickyMenuHeight + 'px';
			} else {
				cryptoairdropMainMenuSticky.classList.remove(cryptoairdropStickyMenuClass);
				cryptoairdropSiteContent.style.marginTop = cryptoairdropSiteContentMarginTop;
			}
			if(window.pageYOffset > (cryptoairdropHeaderHeight * 1)) {
				cryptoairdropMainMenuSticky.classList.add(cryptoairdropStickyMenuInViewClass);
			} else {
				cryptoairdropMainMenuSticky.classList.remove(cryptoairdropStickyMenuInViewClass);
			}
		});
	}

	// Utility function.
	function cryptoairdropUtil() {}

	// Smooth scroll.
	cryptoairdropUtil.scrollTo = function(final, duration, cb) {
		var cryptoairdropStart = window.scrollY || document.documentElement.scrollTop,
			cryptoairdropCurrentTime = null;

		var cryptoairdropAnimateScroll = function(timestamp) {
			if(!cryptoairdropCurrentTime) {
				cryptoairdropCurrentTime = timestamp;
			}

			var cryptoairdropProgress = timestamp - cryptoairdropCurrentTime;

			if(cryptoairdropProgress > duration) {
				cryptoairdropProgress = duration;
			}

			var cryptoairdropVal = Math.easeInOutQuad(cryptoairdropProgress, cryptoairdropStart, final - cryptoairdropStart, duration);

			window.scrollTo(0, cryptoairdropVal);
			if(cryptoairdropProgress < duration) {
				window.requestAnimationFrame(cryptoairdropAnimateScroll);
			} else {
				cb && cb();
			}
		};

		window.requestAnimationFrame(cryptoairdropAnimateScroll);
	};

	// Animation curves.
	Math.easeInOutQuad = function (t, b, c, d) {
		t /= d/2;
		if(t < 1) return c/2*t*t + b;
		t--;
		return -c/2 * (t*(t-2) - 1) + b;
	};

	// Back to top.
	var cryptoairdropBackTop = document.querySelector('.back-to-top');
	if(cryptoairdropBackTop) {
		var cryptoairdropOffset = 300;
		var cryptoairdropOffsetOpacity = 1200;
		var cryptoairdropScrollDuration = 700;
		var cryptoairdropScrolling = false;
		window.addEventListener('scroll', function() {
			if(!cryptoairdropScrolling) {
				cryptoairdropScrolling = true;
				(!window.requestAnimationFrame) ? setTimeout(cryptoairdropCheckBackToTop, 250) : window.requestAnimationFrame(cryptoairdropCheckBackToTop);
			}
		});

		document.addEventListener('click', function(event) {
			if(cryptoairdropTargetMatches('.back-to-top')) {
				event.preventDefault();
				(!window.requestAnimationFrame) ? window.scrollTo(0, 0) : cryptoairdropUtil.scrollTo(0, cryptoairdropScrollDuration);
			}
		});
	}

	function cryptoairdropCheckBackToTop() {
		var cryptoairdropWindowTop = window.scrollY || document.documentElement.scrollTop;
		( cryptoairdropWindowTop > cryptoairdropOffset ) ? cryptoairdropBackTop.classList.add('back-to-top--show') : cryptoairdropBackTop.classList.remove('back-to-top--show', 'back-to-top--fade-out');
		( cryptoairdropWindowTop > cryptoairdropOffsetOpacity ) && cryptoairdropBackTop.classList.add('back-to-top--fade-out');
		cryptoairdropScrolling = false;
	}

})();
