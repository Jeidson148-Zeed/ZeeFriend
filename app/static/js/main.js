// Modal logic
function openPostModal() {
    document.getElementById("postModal").style.display = "block";
    document.body.style.overflow = "hidden"; // Prevent scrolling
}

function closePostModal() {
    document.getElementById("postModal").style.display = "none";
    document.body.style.overflow = "auto";
}

// Close modal when clicking outside
window.onclick = function(event) {
    let modal = document.getElementById("postModal");
    if (event.target == modal) {
        closePostModal();
    }
}
