// Get the Sidebar
var mySidebar = document.getElementById("mySidebar");
// Get the DIV with overlay effect
var overlayBg = document.getElementById("myOverlay");

// Toggle between showing and hiding the sidebar, and add overlay effect
function w3_open() {
    if (mySidebar.style.display === 'block') {
        mySidebar.style.display = 'none';
        overlayBg.style.display = "none";
    } else {
        mySidebar.style.display = 'block';
        overlayBg.style.display = "block";
    }
};

// Close the sidebar with the close button
function w3_close() {
    mySidebar.style.display = "none";
    overlayBg.style.display = "none";
};

function openType(evt, typeName) {
	var temp = evt.currentTarget.className.replace(" active", "");

	if (evt.currentTarget.className == temp + " active"){

		evt.currentTarget.className = evt.currentTarget.className.replace(" active", "");
		document.getElementById(typeName).style.display = "none";

	} else {

		var i, tabcontent, tablinks;
		tabcontent = document.getElementsByClassName("tabcontent");
		for (i = 0; i < tabcontent.length; i++) {
			tabcontent[i].style.display = "none";
		}

		tablinks = document.getElementsByClassName("FilterType");
		for (i = 0; i < tablinks.length; i++) {
			tablinks[i].className = tablinks[i].className.replace(" active", "");
		}

		document.getElementById(typeName).style.display = "block";
		evt.currentTarget.className += " active";
	}
};

function select(evt){
	var temp = evt.currentTarget.className.replace(" active", "");

	if (evt.currentTarget.className == temp + " active") {
		evt.currentTarget.className = evt.currentTarget.className.replace(" active", "");
	} else {
		evt.currentTarget.className += " active";
	}
};