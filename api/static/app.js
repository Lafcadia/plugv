let d = document;
function search() {
    d.getElementById("result-table").style.display = "none"; // Hide the table
    d.getElementById("error").innerText = "";
    d.getElementById("submit").innerText = "Searching...";
    d.getElementById("submit").disabled = true;
    var search = d.getElementById("search").value;
    var searchEngine = d.getElementsByName("SearchE")[0].checked ? "bing" : "google";
    fetch("/s?q=" + encodeURIComponent(search) + "&s=" + encodeURIComponent(searchEngine)).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            response.text().then(data => {
                d.getElementById("error").innerText = "Error: " + data;
                d.getElementById("submit").innerText = "Search";
                d.getElementById("submit").disabled = false;
            })
            return Promise.resolve([]);
        }
    }).then(data => {
        if (data.length > 0) {
            d.getElementById("submit").innerText = "Search";
            d.getElementById("submit").disabled = false;
            d.getElementById("result-table").style.display = "table"; // Show the table
            d.getElementById("result").innerHTML = data.map(result => `<tr><td><a href="${result["2"]}" target="_blank">${result["0"]}</a></td><td>${result["1"]}</td></tr>`).join("");
        } else {
            d.getElementById("error").innerText = "Error: No results found";
            d.getElementById("submit").innerText = "Search";
            d.getElementById("submit").disabled = false;
        }
    }).catch(error => {
        d.getElementById("error").innerText = "Error: " + error;
        d.getElementById("submit").innerText = "Search";
        d.getElementById("submit").disabled = false;
    });
}


window.addEventListener("keydown", (event) => {
    if (event.code === "Enter") {
        search();
    }
});