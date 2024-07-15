function toggleForm(formId) {
    var form = document.getElementById(formId);
    var forms = document.querySelectorAll('.resource-form');
    
    var isOpen = form.style.display === "block";
    
    forms.forEach(f => f.style.display = 'none');
    
    if (!isOpen) {
        form.style.display = "block";
    }
}

function toggleSection(sectionId) {
    var section = document.getElementById(sectionId);
    if (section.style.maxHeight === "0px" || section.style.maxHeight === "") {
        section.style.maxHeight = section.scrollHeight + "px";
        section.classList.add('open');
    } else {
        section.style.maxHeight = section.scrollHeight + "px"; // Set to current height for transition
        setTimeout(() => {
            section.style.maxHeight = "0px";
            section.classList.remove('open');
        }, 1);
    }
}

function toggleContent(contentId) {
    var content = document.getElementById(contentId);
    if (content.style.maxHeight === "0px" || content.style.maxHeight === "") {
        content.style.maxHeight = content.scrollHeight + "px";
        content.classList.add('open');
    } else {
        content.style.maxHeight = content.scrollHeight + "px"; // Set to current height for transition
        setTimeout(() => {
            content.style.maxHeight = "0px";
            content.classList.remove('open');
        }, 1);
    }
}
