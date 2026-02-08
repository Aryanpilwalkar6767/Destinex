/**
 * Main Application Script for DESTINEX
 * Handles search, API calls, filters, and UI interactions
 * Backend API: http://localhost:5000/search?city=<city_name>
 */

// ==========================================
// STATE MANAGEMENT
// ==========================================

let currentCategory = 'attractions';
let currentCity = '';
let allData = {
    attractions: [],
    hotels: [],
    restaurants: []
};

// Backend API URL
const API_BASE_URL = 'http://192.168.1.8:5000'; // Updated for mobile access

// Map variables
let map = null;
let markers = [];
const GEOAPIFY_API_KEY = 'f5a3b7556f5e4ccbae46750046a151c1'; // Using the key provided by user

// ==========================================
// DOM ELEMENTS
// ==========================================

const homepage = document.getElementById('homepage');
const resultsPage = document.getElementById('resultsPage');
const navBack = document.getElementById('navBack');
const citySearch = document.getElementById('citySearch');
const searchBtn = document.getElementById('searchBtn');
const cityName = document.getElementById('cityName');
const cardsGrid = document.getElementById('cardsGrid');
const resultsTitle = document.getElementById('resultsTitle');
const resultsCount = document.getElementById('resultsCount');
const loadingOverlay = document.getElementById('loadingOverlay');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const tabBtns = document.querySelectorAll('.tab-btn');
const ratingFilter = document.getElementById('ratingFilter');
const budgetFilter = document.getElementById('budgetFilter');
const distanceFilter = document.getElementById('distanceFilter');
const resetFilters = document.getElementById('resetFilters');
const lastSearchBtn = document.getElementById('lastSearchBtn');

// ==========================================
// LAST SEARCH FEATURE
// ==========================================

/**
 * Save the last searched city to localStorage
 */
function saveLastSearch(city) {
    localStorage.setItem('destinex_last_search', city);
}

/**
 * Get the last searched city from localStorage
 */
function getLastSearch() {
    return localStorage.getItem('destinex_last_search');
}

/**
 * Update the last search button visibility
 */
function updateLastSearchButton() {
    const lastCity = getLastSearch();
    const container = document.getElementById('lastSearchContainer');
    const citySpan = document.getElementById('lastSearchCity');

    if (lastCity) {
        citySpan.textContent = lastCity;
        container.style.display = 'block';
    } else {
        container.style.display = 'none';
    }
}

/**
 * Handle last search button click
 */
function handleLastSearch() {
    const lastCity = getLastSearch();
    if (lastCity) {
        citySearch.value = lastCity;
        performSearch(lastCity);
    } else {
        alert('No previous search found. Try searching for a city first!');
    }
}

// ==========================================
// API CALLS
// ==========================================

/**
 * Fetch data from backend API
 * No mock data - only real API calls
 */
async function fetchCityData(city) {
    try {
        const response = await fetch(`${API_BASE_URL}/search?city=${encodeURIComponent(city)}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Failed to fetch data');
        }

        return data;

    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ==========================================
// SEARCH FUNCTIONALITY
// ==========================================

/**
 * Perform search for a city
 */
async function performSearch(city) {
    if (!city || !city.trim()) {
        alert('Please enter a city name');
        return;
    }

    currentCity = city.trim();

    // Show loading
    showLoading(true);
    hideError();

    try {
        // Fetch data from backend
        const data = await fetchCityData(currentCity);

        // Store data
        allData = {
            attractions: data.attractions || [],
            hotels: data.hotels || [],
            restaurants: data.restaurants || []
        };

        // Save to last search
        saveLastSearch(currentCity);

        // Update UI
        cityName.textContent = data.city || currentCity;

        // Show results page
        showResultsPage();

        // Initialize/Update Map
        let centerLat = 0, centerLon = 0;
        const allItems = [...data.attractions, ...data.hotels, ...data.restaurants];
        if (allItems.length > 0) {
            // Use the first item to set the map center
            if (allItems[0].lat && allItems[0].lon) {
                centerLat = allItems[0].lat;
                centerLon = allItems[0].lon;
                initMap(centerLat, centerLon);

                // Initial markers (attractions by default)
                updateMapMarkers(data.attractions);
            }
        }

        // Default to attractions
        switchCategory('attractions');

        // Reset filters
        resetAllFilters();

    } catch (error) {
        showError(error.message || 'Failed to fetch data. Please try again.');
        console.error('Search error:', error);
    } finally {
        showLoading(false);
    }
}

/**
 * Show/hide loading overlay
 */
function showLoading(show) {
    loadingOverlay.style.display = show ? 'flex' : 'none';
}

/**
 * Show error message
 */
function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'block';
    showResultsPage(); // Ensure user sees the error page
    cardsGrid.innerHTML = '';
    resultsCount.textContent = '0 results found';
}

/**
 * Hide error message
 */
function hideError() {
    errorMessage.style.display = 'none';
}

// ==========================================
// MAP FUNCTIONALITY
// ==========================================

/**
 * Initialize Leaflet Map
 */
function initMap(lat, lon) {
    if (map) {
        map.setView([lat, lon], 13);
        return;
    }

    if (typeof L === 'undefined') {
        console.error('Leaflet library not loaded');
        return;
    }

    map = L.map('map').setView([lat, lon], 13);

    L.tileLayer(`https://maps.geoapify.com/v1/tile/osm-bright/{z}/{x}/{y}.png?apiKey=${GEOAPIFY_API_KEY}`, {
        attribution: 'Powered by <a href="https://www.geoapify.com/" target="_blank">Geoapify</a> | © OpenStreetMap contributors',
        maxZoom: 20,
        id: 'osm-bright'
    }).addTo(map);
}

/**
 * Update map markers based on data
 */
function updateMapMarkers(data) {
    // Check if map is initialized
    if (!map) return;

    // Clear existing markers
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];

    if (!data || data.length === 0) return;

    // Add new markers
    data.forEach(item => {
        if (item.lat && item.lon) {
            const marker = L.marker([item.lat, item.lon])
                .addTo(map)
                .bindPopup(`<b>${item.name}</b><br>${item.rating || '4.0'} <i class="fas fa-star" style="color: gold;"></i>`);
            markers.push(marker);
        }
    });

    // Fit bounds if multiple markers
    if (markers.length > 0) {
        const group = new L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.1));
    }
}

// ==========================================
// UI NAVIGATION
// ==========================================

/**
 * Show results page
 */
function showResultsPage() {
    homepage.style.display = 'none';
    resultsPage.style.display = 'block';
    navBack.style.display = 'flex';
    window.scrollTo(0, 0);
}

/**
 * Show homepage
 */
function showHomepage() {
    homepage.style.display = 'flex';
    resultsPage.style.display = 'none';
    navBack.style.display = 'none';
    hideError();
    citySearch.value = '';
    updateLastSearchButton();
}

// ==========================================
// CATEGORY & FILTERING
// ==========================================

/**
 * Switch between categories (attractions, hotels, restaurants)
 */
function switchCategory(category) {
    currentCategory = category;

    // Update active tab
    tabBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.category === category);
    });

    // Update title
    const titles = {
        attractions: 'Places to Visit',
        hotels: 'Nearby Hotels',
        restaurants: 'Nearby Restaurants'
    };
    resultsTitle.textContent = titles[category] || 'Results';

    // Apply filters and render
    applyFilters();

    // Update Map Markers for new category
    updateMapMarkers(allData[currentCategory] || []);
}

/**
 * Apply filters to current category data
 */
function applyFilters() {
    let data = [...(allData[currentCategory] || [])];

    // Rating Filter
    const minRating = parseFloat(ratingFilter.value);
    if (!isNaN(minRating)) {
        data = data.filter(item => item.rating >= minRating);
    }

    // Budget Filter
    const budget = budgetFilter.value;
    if (budget !== 'all') {
        const priceMap = { '1': '₹', '2': '₹₹', '3': '₹₹₹' };
        data = data.filter(item => item.price_range === priceMap[budget]);
    }

    // Distance Filter
    const maxDistance = parseFloat(distanceFilter.value);
    if (!isNaN(maxDistance)) {
        data = data.filter(item => item.distance <= maxDistance);
    }

    renderCards(data);
}

/**
 * Reset all filters to default
 */
function resetAllFilters() {
    ratingFilter.value = 'all';
    budgetFilter.value = 'all';
    distanceFilter.value = 'all';
    applyFilters();
}

// ==========================================
// CARD RENDERING
// ==========================================

/**
 * Render cards to the grid
 */
function renderCards(data) {
    cardsGrid.innerHTML = '';

    if (data.length === 0) {
        cardsGrid.innerHTML = `
            <div class="no-results" style="grid-column: 1/-1; text-align: center; padding: 60px 20px;">
                <i class="fas fa-search" style="font-size: 3rem; color: var(--text-light); margin-bottom: 16px;"></i>
                <h3 style="color: var(--text-dark); margin-bottom: 8px;">No results found</h3>
                <p style="color: var(--text-light);">Try adjusting your filters to see more results.</p>
            </div>
        `;
        resultsCount.textContent = '0 results found';
        return;
    }

    resultsCount.textContent = `${data.length} results found`;

    data.forEach((item, index) => {
        const card = createCard(item, index);
        cardsGrid.appendChild(card);
    });
}

/**
 * Create a single card element
 */
function createCard(item, index) {
    const card = document.createElement('div');
    card.className = 'card';
    card.style.animationDelay = `${index * 0.05}s`;

    // Get icon based on category
    const iconMap = {
        attractions: 'fa-landmark',
        hotels: 'fa-hotel',
        restaurants: 'fa-utensils'
    };
    const icon = iconMap[currentCategory] || 'fa-map-marker-alt';

    card.innerHTML = `
        <div class="card-image">
            <i class="fas ${icon}"></i>
            <div class="card-badge">
                <i class="fas fa-star"></i> ${item.rating || '4.0'}
            </div>
        </div>
        <div class="card-content">
            <div class="card-header">
                <h3 class="card-title">${item.name}</h3>
                <span class="card-price">${item.price_range || '₹'}</span>
            </div>
            <div class="card-insight">
                <p><i class="fas fa-robot"></i> ${item.ai_insight || 'A great place to visit!'}</p>
            </div>
            <div class="card-meta">
                <div class="card-rating">
                    <i class="fas fa-star"></i>
                    <span>${item.rating || '4.0'}</span>
                </div>
                <div class="card-distance">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>${item.distance || 0} km</span>
                </div>
            </div>
        </div>
    `;

    card.addEventListener('click', () => {
        alert(`Opening details for ${item.name}...\n\n(This feature will be implemented in future updates)`);
    });

    return card;
}

// ==========================================
// EVENT LISTENERS
// ==========================================

document.addEventListener('DOMContentLoaded', function () {

    // Search button click
    searchBtn.addEventListener('click', () => {
        const city = citySearch.value.trim();
        if (city) {
            performSearch(city);
        } else {
            citySearch.focus();
        }
    });

    // Search on Enter key
    citySearch.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchBtn.click();
        }
    });

    // Back button
    navBack.addEventListener('click', showHomepage);

    // Category tabs
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            switchCategory(btn.dataset.category);
        });
    });

    // Filters
    [ratingFilter, budgetFilter, distanceFilter].forEach(filter => {
        filter.addEventListener('change', applyFilters);
    });

    // Reset filters
    resetFilters.addEventListener('click', resetAllFilters);

    // Last search button
    lastSearchBtn.addEventListener('click', handleLastSearch);

});