<template>
  <nav class="navbar navbar-expand-lg navbar-custom">
    <div class="container">
      <a class="navbar-brand">Habitville</a>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto">
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
/* Global styles */
body, html {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background-color: #65dc6f; /* Lighter green background */
    color: #333;
}

#app { 
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #65dc6f; /* Ensures that the flex container also has a green background */
}

.navbar-custom {
    background-color: #4CAF50; /* Dark green navbar */
}

.navbar-custom .navbar-brand,
.navbar-custom .navbar-nav .nav-link {
    color: white;
}

main {
    flex: 1; /* Makes sure the main content area expands to fill the available space */
    background-color: inherit; /* This will ensure it inherits the #app's background color */
}

/* Add footer styles if you have a footer */
.footer-custom {
    background-color: #4CAF50; /* Dark green footer */
    color: white;
}

/* Ensures that any content within main also has a green background */
main * {
    background-color: inherit;
}

/* Additional global styles can go here */
</style>
