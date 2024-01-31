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
          console.log("Profile updated successfully");
        } else {
          console.error("Failed to update profile:", response.status, response.statusText);
        }
      } catch (error) {
        console.error("Error updating profile:", error);
      }
    };

    fetchUserProfile();

    return { user, updateProfile };
  },
});
</script>
  
<style scoped>
</style>
  