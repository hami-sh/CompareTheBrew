$(document).ready(function (e) {
    document.getElementById("slide").addEventListener('click', function () {
        document.getElementById("cover").classList.toggle("shadow");
        document.getElementById("cover").classList.toggle("clickable");
    });

    document.getElementById("searchButton").addEventListener('click', function () {
        document.getElementById("query").submit();
    });

    document.getElementById("cover").addEventListener('click', function () {
        document.getElementById("slide").checked = false;
        document.getElementById("cover").classList.toggle("shadow");
        document.getElementById("cover").classList.toggle("clickable");
    });

    document.getElementById("slide").checked = false;

    // handle switching of buttons
    var url;
    url = window.location.href;
    console.log(url);
    var split = url.split("/");
    console.log(split);
    console.log(split[3]);
    var search_type = split[3].split("=")[1];
    var search_term = split[4];
    console.log(search_type);
    console.log(search_term);
    var bestscore = "window.location.href=" + "'http://" + split[2] + "/results=" + "score-desc" + "/" + search_term + "';";
    var worstscore = "window.location.href=" + "'http://" + split[2] + "/results=" + "score-asc" + "/" + search_term + "';";
    var worstprice = "window.location.href=" + "'http://" + split[2] + "/results=" + "price-desc" + "/" + search_term + "';";
    var volume = "window.location.href=" + "'http://" + split[2] + "/results=" + "size-desc" + "/" + search_term + "';";
    document.getElementById("bestscore").setAttribute("onclick", bestscore);
    document.getElementById("worstscore").setAttribute("onclick", worstscore);
    document.getElementById("worstprice").setAttribute("onclick", worstprice)
    document.getElementById("volume").setAttribute("onclick", volume)

    if (search_type == "score-desc") {
        document.getElementById("bestscore").className = "buttonSortActive"
        document.getElementById("worstscore").className = "buttonSort"
        document.getElementById("worstprice").className = "buttonSort"
        document.getElementById("volume").className = "buttonSort"
    } else if (search_type == "score-asc") {
        document.getElementById("bestscore").className = "buttonSort"
        document.getElementById("worstscore").className = "buttonSortActive"
        document.getElementById("worstprice").className = "buttonSort"
        document.getElementById("volume").className = "buttonSort"
    } else if (search_type == "price-desc") {
        document.getElementById("bestscore").className = "buttonSort"
        document.getElementById("worstscore").className = "buttonSort"
        document.getElementById("worstprice").className = "buttonSortActive"
        document.getElementById("volume").className = "buttonSort"
    } else if (search_type == "size-desc") {
        document.getElementById("bestscore").className = "buttonSort"
        document.getElementById("worstscore").className = "buttonSort"
        document.getElementById("worstprice").className = "buttonSort"
        document.getElementById("volume").className = "buttonSortActive"
    }

});