$(document).ready(function(e) {
        document.getElementById("slide").addEventListener('click', function() {
                document.getElementById("cover").classList.toggle("shadow");
                document.getElementById("cover").classList.toggle("clickable");
        });

        document.getElementById("searchButton").addEventListener('click', function() {
                document.getElementById("query").submit();
        });

        document.getElementById("cover").addEventListener('click', function() {
                document.getElementById("slide").checked = false;
                document.getElementById("cover").classList.toggle("shadow");
                document.getElementById("cover").classList.toggle("clickable");
        });
});