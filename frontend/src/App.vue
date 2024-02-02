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
            >
              Habit Tracker
            </router-link>
          </li>
          <!-- Profile Page button -->
          <li class="nav-item">
            <router-link
              to="/profile"
              class="btn btn-outline-light m-2"
            >
              Profile Page
            </router-link>
          </li>
          <!-- Logout button -->
          <li class="nav-item">
            <button
              type="button"
              class="btn btn-outline-light m-2"
              @click="logout"
            >
              Logout
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  
  <main class="container pt-4">
    <RouterView class="flex-shrink-0" />
  </main>
</template>


<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },

    methods: {
      logout() {
        window.location.href = "http://localhost:8000/logout/";
      },
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
}

.navbar-custom .navbar-brand,
.navbar-custom .navbar-brand:hover,
.navbar-custom .navbar-nav .nav-link,
.navbar-custom .navbar-nav .nav-link:hover {
    color: white;
    cursor: pointer; 
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

</style>
