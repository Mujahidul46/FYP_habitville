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
  
<script>
import { defineComponent, ref, watch, onMounted } from "vue";
import { useProfileStore } from "@/stores/useProfileStore";

export default defineComponent({
  setup() {
    const profileStore = useProfileStore();
    const localUser = ref({ ...profileStore.user });
    const statusMessage = ref(profileStore.statusMessage);

    watch(() => profileStore.statusMessage, (newMessage) => {
      statusMessage.value = newMessage;
    });

    watch(localUser, (newUser) => {
      profileStore.user = newUser;
    }, { deep: true });

    const updateProfile = async () => {
      await profileStore.updateProfile(localUser.value);
    };

    onMounted(() => {
      localUser.value = { ...profileStore.user };
      profileStore.fetchUserProfile().then(() => {
        localUser.value = { ...profileStore.user };
      });
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