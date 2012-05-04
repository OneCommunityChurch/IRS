navHover = function() {
	var lis = document.getElementById("navmenu").getElementsByTagName("LI");
	for (var i=0; i<lis.length; i++) {
		lis[i].onmouseover=function() {
			this.className+=" iehover";
		}
		lis[i].onmouseout=function() {
			this.className=this.className.replace(new RegExp(" iehover\\b"), "");
		}
	}
}
if (window.attachEvent) window.attachEvent("onload", navHover);


navHover = function() {
	var lis = document.getElementById("submenu").getElementsByTagName("LI");
	for (var i=0; i<lis.length; i++) {
		lis[i].onmouseover=function() {
			this.className+=" iehoversm";
		}
		lis[i].onmouseout=function() {
			this.className=this.className.replace(new RegExp(" iehoversm\\b"), "");
		}
	}
}
if (window.attachEvent) window.attachEvent("onload", navHover);