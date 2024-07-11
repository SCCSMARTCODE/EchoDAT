const basicInfoLink = document.getElementById('basic-info-link');
const changePasswordLink = document.getElementById('change-password-link');
const updateEmailLink = document.getElementById('update-email-link');
const basicInfoForm = document.getElementById('basic-info-form');
const changePasswordForm = document.getElementById('change-password-form');
const updateEmailForm = document.getElementById('update-email-form');

basicInfoLink.addEventListener('click', () => {
    basicInfoForm.style.display = basicInfoForm.style.display === 'none' ? 'block' : 'none';
    changePasswordForm.style.display = 'none'; // Hide the change password form
    updateEmailForm.style.display = 'none'; // Hide the update email form
});

changePasswordLink.addEventListener('click', () => {
    changePasswordForm.style.display = changePasswordForm.style.display === 'none' ? 'block' : 'none';
    basicInfoForm.style.display = 'none'; // Hide the basic info form
    updateEmailForm.style.display = 'none'; // Hide the update email form
});

updateEmailLink.addEventListener('click', () => {
    updateEmailForm.style.display = updateEmailForm.style.display === 'none' ? 'block' : 'none';
    basicInfoForm.style.display = 'none'; // Hide the basic info form
    changePasswordForm.style.display = 'none'; // Hide the change password form
});
