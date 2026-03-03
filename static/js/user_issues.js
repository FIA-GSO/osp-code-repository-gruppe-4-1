const newMessage = document.getElementById("new-issue");
const showNewIssues = document.getElementById("show-new-issues");

function showNewIssue() {
    if (newMessage.style.display === "none") {
        showNewIssues.innerText = "Abbrechen";
        newMessage.style.display = "block";
    } else {
        showNewIssues.innerText = "Neue Anfrage erstellen";
        newMessage.style.display = "none";
    }
}

function checkMessage() {
    let message = document.getElementsByName("message")[0].value;
    if (message === "") {
        return false;
    }

    showNewIssues.innerText = "Neue Anfrage erstellen";
    newMessage.style.display = "none";

    return true;
}