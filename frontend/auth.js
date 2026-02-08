/**
 * Authentication Service for DESTINEX
 * Handles login, signup, and user session management
 * Uses localStorage for storing user data (frontend-only)
 */

// Auth state
let currentUser = null;

/**
 * Initialize authentication on page load
 * Checks if user is already logged in
 */
function initAuth() {
    const savedUser = localStorage.getItem('destinex_user');
    
    if (savedUser) {
        try {
            currentUser = JSON.parse(savedUser);
            showMainApp();
        } catch (e) {
            console.error('Error parsing user data:', e);
            localStorage.removeItem('destinex_user');
            showLoginPage();
        }
    } else {
        showLoginPage();
    }
}

/**
 * Show login page, hide other sections
 */
function showLoginPage() {
    document.getElementById('loginPage').style.display = 'flex';
    document.getElementById('signupPage').style.display = 'none';
    document.getElementById('homepage').style.display = 'none';
    document.getElementById('resultsPage').style.display = 'none';
    document.getElementById('navActions').style.display = 'none';
    document.getElementById('footer').style.display = 'none';
}

/**
 * Show signup page
 */
function showSignupPage() {
    document.getElementById('loginPage').style.display = 'none';
    document.getElementById('signupPage').style.display = 'flex';
    document.getElementById('homepage').style.display = 'none';
    document.getElementById('resultsPage').style.display = 'none';
    
    // Clear any previous errors
    clearErrors();
}

/**
 * Show main app (homepage after login)
 */
function showMainApp() {
    document.getElementById('loginPage').style.display = 'none';
    document.getElementById('signupPage').style.display = 'none';
    document.getElementById('homepage').style.display = 'flex';
    document.getElementById('resultsPage').style.display = 'none';
    document.getElementById('navActions').style.display = 'flex';
    document.getElementById('footer').style.display = 'block';
    
    // Update user greeting
    if (currentUser) {
        document.getElementById('userGreeting').textContent = `Hello, ${currentUser.name}`;
    }
    
    // Check and show last search button
    updateLastSearchButton();
    
    // Focus search input
    setTimeout(() => {
        document.getElementById('citySearch').focus();
    }, 100);
}

/**
 * Handle login form submission
 */
function handleLogin(e) {
    e.preventDefault();
    clearErrors();
    
    const email = document.getElementById('loginEmail').value.trim().toLowerCase();
    const password = document.getElementById('loginPassword').value;
    
    // Validate inputs
    if (!email || !password) {
        showError('loginError', 'Please enter both email and password');
        return;
    }
    
    // Check if user exists in localStorage
    const users = getUsersFromStorage();
    const user = users.find(u => u.email === email && u.password === password);
    
    if (user) {
        // Login successful
        currentUser = {
            name: user.name,
            email: user.email
        };
        
        // Save to localStorage
        localStorage.setItem('destinex_user', JSON.stringify(currentUser));
        
        // Clear form
        document.getElementById('loginForm').reset();
        
        // Show main app
        showMainApp();
    } else {
        showError('loginError', 'Invalid email or password');
    }
}

/**
 * Handle signup form submission
 */
function handleSignup(e) {
    e.preventDefault();
    clearErrors();
    
    const name = document.getElementById('signupName').value.trim();
    const email = document.getElementById('signupEmail').value.trim().toLowerCase();
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('signupConfirmPassword').value;
    
    // Validate inputs
    if (!name || !email || !password) {
        showError('signupError', 'Please fill in all fields');
        return;
    }
    
    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showError('signupError', 'Please enter a valid email address');
        return;
    }
    
    // Validate password length
    if (password.length < 6) {
        showError('signupError', 'Password must be at least 6 characters');
        return;
    }
    
    // Check passwords match
    if (password !== confirmPassword) {
        showError('signupError', 'Passwords do not match');
        return;
    }
    
    // Check if user already exists
    const users = getUsersFromStorage();
    if (users.find(u => u.email === email)) {
        showError('signupError', 'An account with this email already exists');
        return;
    }
    
    // Create new user
    const newUser = {
        name: name,
        email: email,
        password: password,
        createdAt: new Date().toISOString()
    };
    
    // Save to users list
    users.push(newUser);
    localStorage.setItem('destinex_users', JSON.stringify(users));
    
    // Auto-login after signup
    currentUser = {
        name: name,
        email: email
    };
    localStorage.setItem('destinex_user', JSON.stringify(currentUser));
    
    // Clear form
    document.getElementById('signupForm').reset();
    
    // Show main app
    showMainApp();
}

/**
 * Handle logout
 */
function handleLogout() {
    // Clear current user
    currentUser = null;
    localStorage.removeItem('destinex_user');
    
    // Reset UI
    document.getElementById('citySearch').value = '';
    document.getElementById('cardsGrid').innerHTML = '';
    
    // Show login page
    showLoginPage();
}

/**
 * Get all registered users from localStorage
 */
function getUsersFromStorage() {
    const usersJson = localStorage.getItem('destinex_users');
    return usersJson ? JSON.parse(usersJson) : [];
}

/**
 * Show error message
 */
function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.classList.add('show');
}

/**
 * Clear all error messages
 */
function clearErrors() {
    document.querySelectorAll('.form-error').forEach(el => {
        el.textContent = '';
        el.classList.remove('show');
    });
}

/**
 * Check if user is logged in
 */
function isLoggedIn() {
    return currentUser !== null;
}

/**
 * Get current user
 */
function getCurrentUser() {
    return currentUser;
}

// Event Listeners for Auth
document.addEventListener('DOMContentLoaded', function() {
    // Initialize auth
    initAuth();
    
    // Login form
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    
    // Signup form
    document.getElementById('signupForm').addEventListener('submit', handleSignup);
    
    // Toggle between login and signup
    document.getElementById('showSignup').addEventListener('click', function(e) {
        e.preventDefault();
        showSignupPage();
    });
    
    document.getElementById('showLogin').addEventListener('click', function(e) {
        e.preventDefault();
        showLoginPage();
    });
    
    // Logout button
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);
});