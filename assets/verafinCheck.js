$(document).ready(function () {
    $("#verafinButton").click( function () {
        fetch("/verafin", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify()
        })
            .then(resp => resp.json())
            .then(data => {
                var cardText = this.closest(".card").querySelector(".card-text");
                cardText.innerHTML = "";
                for (var jobID in data) {
                    var job = data[jobID];
                    var link = document.createElement("a");
                    link.href = job.link;
                    link.textContent = job.job_title;
                    link.classList.add("job-link")

                    cardText.appendChild(link);
                }
            })
            .catch(error => {
                console.error("Error: ",error);
            });
    });
});