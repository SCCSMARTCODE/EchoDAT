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
    var isOpen = section.style.display === "block";

    if (isOpen) {
        section.style.display = "none";
    } else {
        section.style.display = "block";
    }
}

function toggleContent(contentId) {
    var content = document.getElementById(contentId);
    var isOpen = content.style.display === "block";

    if (isOpen) {
        content.style.display = "none";
    } else {
        content.style.display = "block";
    }
}


