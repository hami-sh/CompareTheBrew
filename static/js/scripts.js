$(document).ready(function(e) {
        document.getElementById("slide").addEventListener('click', function() {
                document.getElementById("cover").classList.toggle("shadow");
        });

        document.getElementById("searchButton").addEventListener('click', function() {
                document.getElementById("query").submit();
        });
});