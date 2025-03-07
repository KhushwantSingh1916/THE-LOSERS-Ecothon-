// filepath: c:\Users\khush\OneDrive\ecothon\THE-LOSERS-Ecothon\src\app.js

document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.getElementById('loginButton');
    const logoutButton = document.getElementById('logoutButton');

    // Initialize Google API client
    function initClient() {
        gapi.load('client:auth2', function() {
            gapi.auth2.init({
                client_id: 'YOUR_GOOGLE_CLIENT_ID',
                scope: 'profile email'
            }).then(() => {
                updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get());
            });
        });
    }

    // Update UI based on sign-in status
    function updateSigninStatus(isSignedIn) {
        if (isSignedIn) {
            const user = gapi.auth2.getAuthInstance().currentUser.get();
            const profile = user.getBasicProfile();
            sessionStorage.setItem('user', JSON.stringify({
                id: profile.getId(),
                name: profile.getName(),
                email: profile.getEmail()
            }));
            window.location.href = 'index.html'; // Redirect to dashboard
        } else {
            logoutButton.style.display = 'none';
        }
    }

    // Handle login button click
    loginButton.addEventListener('click', function() {
        gapi.auth2.getAuthInstance().signIn();
    });

    // Handle logout button click
    logoutButton.addEventListener('click', function() {
        gapi.auth2.getAuthInstance().signOut().then(() => {
            sessionStorage.removeItem('user');
            window.location.href = 'login.html'; // Redirect to login page
        });
    });

    // Load the Google API client
    initClient();
});