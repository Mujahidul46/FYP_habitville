<template>
    <div class="profile-page">
      <h1>Profile</h1>
      <div>
        <label>Username:</label>
        <p>{{ user.username }}</p>
      </div>
      <div>
        <label>Email:</label>
        <p>{{ user.email }}</p>
      </div>
      <div>
        <label>Goals:</label>
        <p>{{ user.goals }}</p>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from "vue";
  
  interface UserData {
    username: string;
    email: string;
    goals: string;
  }
  
  export default defineComponent({
    setup() {
      const user = ref<UserData>({
        username: "",
        email: "",
        goals: "",
      });
  
      const fetchUserProfile = async () => {
        try {
          const response = await fetch("http://localhost:8000/user/", {
            method: "GET",
            credentials: "include",
          });
  
          if (response.ok) {
            const userData = (await response.json()) as UserData;
            user.value = userData;
          } else {
            console.error(
              "Failed to fetch user data:",
              response.status,
              response.statusText
            );
          }
        } catch (error) {
          console.error("Error during fetch:", error);
        }
      };
  
      fetchUserProfile();
  
      return { user };
    },
  });
  </script>
  
  <style scoped>
  </style>
  