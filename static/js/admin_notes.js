function showNote(bookingId) {
    let note = document.getElementById("note-" + bookingId);
    if (note.style.display === "none") {
        note.style.display = "table-row";
    } else {
        note.style.display = "none";
    }
}
