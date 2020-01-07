$(document).ready(function (e) {
    var url;
    url = window.location.href;
    console.log(url);
    var split = url.split("/");
    console.log(split);
    var search_term = split[4].toUpperCase();
    header = document.getElementById("BigHeader");
    console.log(header);
    console.log(search_term);
    header.textContent += search_term;

});