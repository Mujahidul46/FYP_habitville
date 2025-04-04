<template>
  <nav class="navbar navbar-expand-lg navbar-custom" v-if="!isFullscreen">
      <span class="navbar-brand">Habitville</span>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto">
          <!-- Habit Tracker button -->
          <li class="nav-item">
            <router-link
              to="/"
              class="btn btn-outline-custom m-2"
              active-class="nav-link-active"
            >Habit Tracker</router-link>
          </li>
          <!-- Village button -->
          <li class="nav-item">
            <router-link
              to="/village"
              class="btn btn-outline-custom m-2"
              active-class="nav-link-active"
            >Village</router-link>
          </li>
          <!-- Profile Page button -->
          <li class="nav-item">
            <router-link
              to="/profile"
              class="btn btn-outline-custom m-2"
              active-class="nav-link-active"
            >Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link
              to="/statistics"
              class="btn btn-outline-custom m-2"
              active-class="nav-link-active"
            >Statistics</router-link>
          </li>
          <!-- Logout button -->
          <li class="nav-item">
            <button
              type="button"
              class="btn btn-outline-custom m-2"
              @click="logout"
            >Logout</button>
          </li>
        </ul>
      </div>
      <!-- Profile icon and points display -->
      <div class="navbar-account">
        <span class="navbar-text">
          <span class="points" v-if="userProfile && userProfile.life_points !== undefined">
            <img src="@/assets/gem_1.png" class="gem-icon" alt="HP" />
            <span class="points-number">{{ userProfile.habit_points || 0 }}</span>
            <i class="fas fa-heart pixelated-heart"></i>
            <span class="points-number">{{ userProfile.life_points.toFixed(2) }}</span>
          </span>
          <i class="fas fa-user"></i>
          <span class="username">{{ userProfile.username }}</span>
        </span>
      </div>
  </nav>
  <notification
    v-for="(notification, index) in notifications"
    :key="notification.id"
    :message="notification.message"
    :show="notification.show"
    :style="{ '--notification-top': `${70 + index * 60}px` }" 
  />
  <main class="container-fluid pt-4">
    <RouterView></RouterView>
  </main>
</template>

<script>
import { defineComponent, onMounted, computed, watch } from 'vue';
import { RouterView, useRoute } from 'vue-router';
import { useProfileStore } from '@/stores/useProfileStore';
import Notification from '@/components/Notification.vue';
import { useNotificationStore } from '@/stores/useNotificationStore';

export default defineComponent({
  components: { RouterView, Notification },

  setup() {
    const profileStore = useProfileStore();
    const notificationStore = useNotificationStore();
    const route = useRoute();

    onMounted(async () => {
      await profileStore.fetchUserProfile();
      updateColorStyles(profileStore.user);
    });

    const userProfile = computed(() => profileStore.user);
    const notifications = computed(() => notificationStore.notifications);

    watch(userProfile, (newValue) => {
      updateColorStyles(newValue);
    }, { deep: true });

    const updateColorStyles = (user) => {
      if (user.navbar_color && user.main_content_color) {
        document.documentElement.style.setProperty('--navbar-bg-color', user.navbar_color);
        document.documentElement.style.setProperty('--main-content-bg-color', user.main_content_color);
      }
    };

    const logout = () => {
      window.location.href = "http://localhost:8000/logout/";
    };

    const isFullscreen = computed(() => route.meta.fullscreen);

    return {
      userProfile,
      notifications, 
      logout,
      isFullscreen,
    };
  },
});
</script>


<style>
body, html {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background-color: #65dc6f;
    color: #333;
}

#app { 
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #65dc6f;
}

.navbar-custom {
    background-color: var(--navbar-bg-color);
    display: flex;
    justify-content: space-between; 
    align-items: center;
    padding: 0 1.5rem !important;
}

.navbar-custom .navbar-brand {
    font-weight: bold;
}

.navbar-custom .navbar-nav .nav-item .btn,
.navbar-custom .navbar-nav .nav-item .btn:hover,
.navbar-custom .navbar-nav .nav-item .btn:focus {
    color: rgb(0, 0, 0);
    font-weight: 500;
    cursor: pointer;
}

.btn-outline-custom {
    color: rgb(0, 0, 0);
    background-color: transparent;
    border: 1px solid rgb(0, 0, 0);
}


.navbar-custom .navbar-collapse {
    display: flex;
    justify-content: start; 
}

.navbar-custom .navbar-nav {
    display: flex;
    align-items: center;
    margin-right: auto; 
}

.navbar-custom .navbar-text {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.navbar-custom .fas.fa-user {
    font-size: 1.35rem;
    position: relative;
    top: 2px; 
    margin-right: 0.25rem; 
}

.navbar-custom .username {
    font-weight: bold;
    white-space: nowrap;
    font-size: 1.1rem;
    margin-left: -0.4rem; 
}

.navbar-custom .navbar-account {
    display: flex;
    align-items: center;
    margin-left: auto; 
}

main {
    flex: 1;
    background-color: var(--main-content-bg-color);
}

.footer-custom {
    background-color: #4CAF50;
    color: white;
}

#app .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}

#app .modal-content {
    background-color: #FFF;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
    width: auto;
    max-width: 500px;
    z-index: 10000;
}

#app .modal-content input,
#app .modal-content textarea {
    width: calc(100% - 20px);
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.modal-footer {
    display: flex;
    justify-content: space-between;
}

.modal-footer button {
    margin-left: 10px;
    margin-right: 10px;
}

.modal-footer button[type="submit"] {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
}

.modal-footer button[type="button"] {
    border: none;
    padding: 10px 20px;
    cursor: pointer;
}

.navbar-custom .navbar-nav .nav-item .nav-link-active {
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease; 
  transform: translateY(-2px);
  background-color: var(--navbar-bg-color);
  background-image: none;
  color: #000000;
  border-radius: 4px; 
  padding: .375rem .75rem; 
  border: 1px solid darken(var(--navbar-bg-color), 10%);
}

.points-number {
  font-weight: bold;
  font-size: larger;
  margin-left: 0.25rem; 
  position: relative;
  top: 1.75px; 
}

.gem-icon {
  width: 1.8rem; 
  height: auto;
  image-rendering: -moz-crisp-edges;
  image-rendering: crisp-edges;
  position: relative;
}

.pixelated-heart {
  color: red;
  -webkit-text-stroke: 2px black;
  font-size: 1.5rem;
  image-rendering: pixelated;
  image-rendering: -moz-crisp-edges;
  image-rendering: crisp-edges;
  position: relative;
  top: 5.5px; 
  margin-left: 0.5rem; 
  margin-right: 0.1rem;
}
</style>