const basicInfoLink = document.getElementById('basic-info-link');
const changePasswordLink = document.getElementById('change-password-link');
const updateEmailLink = document.getElementById('update-email-link');
const updateArtistUrlLink = document.getElementById('update-artist-url-link');
const appsLink = document.getElementById('apps-link');
const notificationsLink = document.getElementById('notifications-link');
const deleteAccountLink = document.getElementById('delete-account-link');
const basicInfoForm = document.getElementById('basic-info-form');
const changePasswordForm = document.getElementById('change-password-form');
const updateEmailForm = document.getElementById('update-email-form');
const updateArtistUrlForm = document.getElementById('update-artist-url-form');
const appsMessage = document.getElementById('apps-message');
const notificationsForm = document.getElementById('notifications-form');
const deleteAccountForm = document.getElementById('delete-account-form');

basicInfoLink.addEventListener('click', () => {
    basicInfoForm.style.display = basicInfoForm.style.display === 'none' ? 'block' : 'none';
    changePasswordForm.style.display = 'none';
    updateEmailForm.style.display = 'none';
    updateArtistUrlForm.style.display = 'none';
    appsMessage.style.display = 'none';
    notificationsForm.style.display = 'none';
    deleteAccountForm.style.display = 'none';
});

changePasswordLink.addEventListener('click', () => {
    changePasswordForm.style.display = changePasswordForm.style.display === 'none' ? 'block' : 'none';
    basicInfoForm.style.display = 'none';
    updateEmailForm.style.display = 'none';
    updateArtistUrlForm.style.display = 'none';
    appsMessage.style.display = 'none';
    notificationsForm.style.display = 'none';
    deleteAccountForm.style.display = 'none';
});

updateEmailLink.addEventListener('click', () => {
    updateEmailForm.style.display = updateEmailForm.style.display === 'none' ? 'block' : 'none';
    basicInfoForm.style.display = 'none';
    changePasswordForm.style.display = 'none';
    updateArtistUrlForm.style.display = 'none';
    appsMessage.style.display = 'none';
    notificationsForm.style.display = 'none';
    deleteAccountForm.style.display = 'none';
});

updateArtistUrlLink.addEventListener('click', () => {
    updateArtistUrlForm.style.display = updateArtistUrlForm.style.display === 'none' ? 'block' : 'none';
    basicInfoForm.style.display = 'none';
    changePasswordForm.style.display = 'none';
    updateEmailForm.style.display = 'none';
    appsMessage.style.display = 'none';
    notificationsForm.style.display = 'none';
    deleteAccountForm.style.display = 'none';
});

appsLink.addEventListener('click', () => {
    appsMessage.style.display = appsMessage.style.display === 'none' ? 'block' : 'none';
    basicInfoForm.style.display = 'none';
    changePasswordForm.style.display = 'none';
    updateEmailForm.style.display = 'none';
    updateArtistUrlForm.style.display = 'none';
    notificationsForm.style.display = 'none';
    deleteAccountForm.style.display = 'none';
});

notificationsLink.addEventListener('click', () => {
    notificationsForm.style.display = notificationsForm.style.display === 'none' ? 'block' : 'none';
    basicInfoForm.style.display = 'none';
    changePasswordForm.style.display = 'none';
    updateEmailForm.style.display = 'none';
    updateArtistUrlForm.style.display = 'none';
    appsMessage.style.display = 'none';
    deleteAccountForm.style.display = 'none';
});

deleteAccountLink.addEventListener('click', () => {
    deleteAccountForm.style.display = deleteAccountForm.style.display === 'none' ? 'block' : 'none';
    basicInfoForm.style.display = 'none';
    changePasswordForm.style.display = 'none';
    updateEmailForm.style.display = 'none';
    updateArtistUrlForm.style.display = 'none';
    appsMessage.style.display = 'none';
    notificationsForm.style.display = 'none';
});
