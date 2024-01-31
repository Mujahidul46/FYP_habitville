<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
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
  
  <style scoped>
  </style>
  