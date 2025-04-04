import { createRouter, createWebHistory, RouteRecordRaw, NavigationGuardNext, RouteLocationNormalized } from 'vue-router'

import Dashboard from '../pages/Dashboard.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import VillageMap from '../components/VillageMap.vue';
import FishingMinigame from '../components/FishingMinigame.vue';
import Statistics from '../components/Statistics.vue';


let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

const routes: Array<RouteRecordRaw> = [
    { path: '/', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
    { path: '/profile/', name: 'Profile Page', component: ProfilePage, meta: { requiresAuth: true } },
    { path: '/village', name: 'VillageMap', component: VillageMap, meta: { requiresAuth: true } },
    { path: '/fishing-minigame', name: 'FishingMinigame', component: FishingMinigame, meta: { requiresAuth: true, fullscreen: true } },
    { path: '/statistics', name: 'Statistics', component: Statistics, meta: { requiresAuth: true } },

];

const router = createRouter({
    history: createWebHistory(base),
    routes
});

async function isLoggedIn(): Promise<boolean> {
    try {
        const response = await fetch('http://localhost:8000/check_authentication/', {
            credentials: 'include'
        });
        if (response.ok) {
            const data = await response.json();
            return data.isAuthenticated;
        }
        return false;
    } catch (error) {
        console.error('Error checking authentication:', error);
        return false;
    }
}

router.beforeEach(async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
    const auth = await isLoggedIn();

    if (to.path === '/login/') {
        // If user goes to protected URL "http://localhost:5173/login/" redirect them to login form URL
        if (!auth) {
            window.location.href = 'http://localhost:8000/login/';
            return;
        } else {
            next({ path: '/' }); 
            return;
        }
    }

    if (to.matched.some(record => record.meta.requiresAuth) && !auth) {
        window.location.href = 'http://localhost:8000/login/';
        return;
    }
    
    next();
});

export default router;
