$(document).ready(function () {
    $(".viewJobsButton").click( function () {
        $("#loadingbutton").css("display","flex");

        var endpoint = $(this).data("endpoint")
        fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify()
        })
            .then(resp => resp.json())
            .then(data => {
                $("#loadingbutton").css("display","none");

                var cardText = this.closest(".card").querySelector(".card-text");
                cardText.innerHTML = "";

                if (data === 1) {cardText.innerHTML = "No Position Open Right Now.";}
                else if (data === -1) {cardText.innerHTML = "No Careers Link";}
                else if (data === 2) {cardText.innerHTML = "Coming Soon...";}
                else {
                    for (var jobID in data) {
                    var job = data[jobID];
                    var link = document.createElement("a");
                    link.href = job.link;
                    link.textContent = job.job_title;
                    link.classList.add("job-link")

                    cardText.appendChild(link);
                }
                }

            })
            .catch(error => {
                console.error("Error: ",error);
                $("#loadingbutton").css("display","none");
            });
    });
});