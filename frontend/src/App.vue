<template>
  <nav class="navbar navbar-expand-lg navbar-custom">
    <div class="container">
      <span class="navbar-brand">Habitville</span>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto">
          <!-- Habit Tracker button -->
          <li class="nav-item">
            <router-link
              to="/"
              class="btn btn-outline-light m-2"
              active-class="nav-link-active"
            >Habit Tracker</router-link>
          </li>
          <!-- Profile Page button -->
          <li class="nav-item">
            <router-link
              to="/profile"
              class="btn btn-outline-light m-2"
              active-class="nav-link-active"
            >Profile Page</router-link>
          </li>
          <!-- Logout button -->
          <li class="nav-item">
            <button
              type="button"
              class="btn btn-outline-light m-2"
              @click="logout"
            >Logout</button>
          </li>
        </ul>
      </div>
      <!-- Profile icon and points display -->
      <div class="navbar-account">
        <span class="navbar-text">
          <i class="fas fa-user"></i>
          <span class="username">{{ userProfile.username }}</span>
          <!-- Habit Points and Life Points -->
          <span class="points" v-if="userProfile && userProfile.life_points !== undefined">
            HP: {{ userProfile.habit_points || 0 }} | LP: {{ userProfile.life_points.toFixed(2) }}
          </span>
        </span>
      </div>
    </div>
  </nav>
  
  <main class="container pt-4">
    <RouterView></RouterView>
  </main>
</template>



<script>
import { defineComponent, onMounted, computed } from "vue";
import { RouterView } from "vue-router";
import { useProfileStore } from "@/stores/useProfileStore";

export default defineComponent({
  components: { RouterView },

  setup() {
    const profileStore = useProfileStore();

    onMounted(async () => {
      await profileStore.fetchUserProfile();
    });

    const userProfile = computed(() => profileStore.user);

    const logout = () => {
      window.location.href = "http://localhost:8000/logout/";
    };

    return {
      userProfile,
      logout,
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
    background-color: #4CAF50;
    display: flex;
    justify-content: space-between; 
    align-items: center;
    padding: 0 1rem;
}

.navbar-custom .navbar-brand,
.navbar-custom .navbar-brand:hover,
.navbar-custom .navbar-nav .nav-link,
.navbar-custom .navbar-nav .nav-link:hover {
    color: white;
    cursor: pointer;
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
    font-size: 1.2rem;
}

.navbar-custom .username {
    font-weight: bold;
    white-space: nowrap;
}

.navbar-custom .navbar-account {
    display: flex;
    align-items: center;
    margin-left: auto; 
}


main {
    flex: 1;
    background-color: #65dc6f;
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
  box-shadow: 0 0 20px 0 rgba(1, 163, 104, 0.7); 
  transition: all 0.3s ease; 
  transform: translateY(-2px); 
  background-image: linear-gradient(45deg, #025301, rgb(3, 160, 97)); 
  color: #ffffff; 
  border-radius: 4px; 
  padding: .375rem .75rem; 
  border: 1px solid #027d40; 
}

</style>