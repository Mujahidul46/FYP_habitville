<template>
  <div class="profile-page">
    <h1>Profile</h1>
    <form @submit.prevent="updateProfile">
      <div>
        <label for="username">Username:</label>
        <input id="username" v-model="user.username" />
      </div>
      <div>
        <label for="email">Email:</label>
        <input id="email" type="email" v-model="user.email" />
      </div>
      <div>
        <label for="goals">Goals:</label>
        <textarea id="goals" placeholder="Write your goals and motivations here!" v-model="user.goals"></textarea>
      </div>
      <button type="submit">Update Profile</button>
    </form>
    <p v-if="statusMessage" class="status-message">{{ statusMessage }}</p>
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

      const statusMessage = ref("");
  
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
  
      const updateProfile = async () => {
      try {
        const response = await fetch("http://localhost:8000/user/update/", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(user.value),
          credentials: "include",
        });

        if (response.ok) {
            statusMessage.value = "Profile updated successfully"; 
          } else {
            statusMessage.value = "Failed to update profile. Please try again."; 
          }
        } catch (error) {
          statusMessage.value = "An error occurred while updating the profile."; 
        }
      };

    fetchUserProfile();

    return { user, updateProfile, statusMessage };
  },
});
</script>
  
<style scoped>
.profile-page input,
.profile-page textarea {
    background-color: white; 
    border: 1px solid #ccc; 
    padding: 8px; 
    margin-bottom: 10px; 
    width: 100%; 
}

.profile-page button {
    background-color: #1a1a80; 
    color: white; 
    padding: 8px 16px; 
    border: none;
    cursor: pointer; 
    margin-top: 10px; 
}
</style>
