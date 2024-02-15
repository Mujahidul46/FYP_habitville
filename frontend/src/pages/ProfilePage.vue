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
    <transition name="status-message">
      <p v-show="statusMessage" class="status-message" :key="statusMessage">{{ statusMessage }}</p>
    </transition>
  </div>
</template>
  
<script>
import { defineComponent, ref, onMounted, nextTick } from "vue";
import { useProfileStore } from "@/stores/useProfileStore";

export default defineComponent({
  setup() {
    const profileStore = useProfileStore();
    const localUser = ref({ ...profileStore.user });
    const statusMessage = ref("");

    const updateProfile = async () => {
      statusMessage.value = "";
      
      await nextTick();

      if (JSON.stringify(localUser.value) === JSON.stringify(profileStore.user)) {
        statusMessage.value = "No changes made.";
        return;
      }

      const updateResult = await profileStore.updateProfile(localUser.value);
      if (updateResult) {
        profileStore.user = { ...localUser.value };
        statusMessage.value = "Profile updated successfully!";
      } else {
        statusMessage.value = "Failed to update profile.";
      }
    };


    onMounted(async () => {
      await profileStore.fetchUserProfile();
      localUser.value = { ...profileStore.user };
    });

    return {
      user: localUser,
      updateProfile,
      statusMessage,
    };
  },
});
</script>

 
<style scoped>

.profile-page {
  max-width: 540px;
  margin: auto;
}
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

.status-message-enter-from,
.status-message-leave-to {
  opacity: 0;
}

.status-message-enter-to,
.status-message-leave-from {
  opacity: 1;
}

.status-message-enter-active,
.status-message-leave-active {
  transition: opacity 0.5s ease;
}


</style>