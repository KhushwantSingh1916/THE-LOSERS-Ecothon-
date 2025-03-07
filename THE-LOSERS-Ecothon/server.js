const express = require('express');
const session = require('express-session');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware for session management
app.use(session({
    secret: 'khushwant',
    resave: false,
    saveUninitialized: true,
}));

// Initialize Passport for authentication
app.use(passport.initialize());
app.use(passport.session());

// Configure Passport to use Google OAuth2
passport.use(new GoogleStrategy({
    clientID: '390921447359-b8ol5og3avpp7q0eu1jsomk1acjhi81g.apps.googleusercontent.com',
    clientSecret: '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',
    callbackURL: '/auth/google/callback',
}, (accessToken, refreshToken, profile, done) => {
    // Save user profile to session
    return done(null, profile);
}));

passport.serializeUser((user, done) => {
    done(null, user);
});

passport.deserializeUser((user, done) => {
    done(null, user);
});

// Serve static files
app.use(express.static(path.join(__dirname, 'src')));

// Routes
app.get('/auth/google', passport.authenticate('google', {
    scope: ['profile', 'email'],
}));

app.get('/auth/google/callback', 
    passport.authenticate('google', { failureRedirect: '/login.html' }),
    (req, res) => {
        // Successful authentication, redirect to dashboard
        res.redirect('/index.html');
    }
);

app.get('/logout', (req, res) => {
    req.logout();
    res.redirect('/login.html');
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});