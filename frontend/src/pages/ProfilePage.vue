<template>
  <div class="profile-page">
    <h1 class="ProfileFormTitle">Profile</h1>
    <form @submit.prevent="updateProfile">
      <!-- Username Input -->
      <div>
        <label for="username">Username:</label>
        <input id="username" v-model="user.username" />
      </div>
      <!-- Email Input -->
      <div>
        <label for="email">Email:</label>
        <input id="email" type="email" v-model="user.email" />
      </div>
      <!-- Goals Textarea -->
      <div>
        <label for="goals">Goals:</label>
        <textarea id="goals" placeholder="Write your goals and motivations here!" v-model="user.goals"></textarea>
      </div>
      <!-- Navigation Bar Colour Swatches -->
      <div>
        <label>Navigation Bar Colour:</label>
        <div class="color-selector">
          <div
            v-for="color in navbarColors"
            :key="color.name"
            class="color-swatch"
            :style="{ backgroundColor: color.hex }"
            @click="selectNavbarColor(color.hex)"
            :class="{ selected: user.navbar_color === color.hex }"
          ></div>
        </div>
      </div>
      <!-- Main Content Colour Swatches -->
      <div>
        <label>Main Content Colour:</label>
        <div class="color-selector">
          <div
            v-for="color in contentColors"
            :key="color.name"
            class="color-swatch"
            :style="{ backgroundColor: color.hex }"
            @click="selectContentColor(color.hex)"
            :class="{ selected: user.main_content_color === color.hex }"
          ></div>
        </div>
      </div>
      <!-- Update Profile Button -->
      <button type="submit">Update Profile</button>
    </form>
    <!-- Status Message Display -->
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

    const navbarColors = [
    { name: 'Crimson', hex: '#DC143C' },
    { name: 'Red', hex: '#f44336' },
    { name: 'Tomato', hex: '#FF6347' },
    { name: 'Coral', hex: '#FF7F50' },
    { name: 'DarkOrange', hex: '#FF8C00' },
    { name: 'Orange', hex: '#ff9800' },
    { name: 'Gold', hex: '#FFD700' },
    { name: 'Yellow', hex: '#ffeb3b' },
    { name: 'Amber', hex: '#ffc107' },
    { name: 'Lime', hex: '#cddc39' },
    { name: 'Light Green', hex: '#8bc34a' },
    { name: 'Green', hex: '#4caf50' },
    { name: 'Teal', hex: '#009688' },
    { name: 'Cyan', hex: '#00bcd4' },
    { name: 'Light Blue', hex: '#03a9f4' },
    { name: 'Blue', hex: '#2196f3' },
    { name: 'SlateBlue', hex: '#6A5ACD' },
    { name: 'Indigo', hex: '#3f51b5' },
    { name: 'Purple', hex: '#9c27b0' },
    { name: 'Orchid', hex: '#DA70D6' },
    { name: 'Deep Purple', hex: '#673ab7' },
    { name: 'Pink', hex: '#e91e63' },
    { name: 'HotPink', hex: '#FF69B4' },
    { name: 'LightCoral', hex: '#F08080' },
    { name: 'DarkSalmon', hex: '#E9967A' },
    { name: 'Chocolate', hex: '#D2691E' },
    { name: 'Brown', hex: '#795548' },
    { name: 'Light Grey', hex: '#d3d3d3' },
    { name: 'Grey', hex: '#9e9e9e' },
    { name: 'Blue Grey', hex: '#607d8b' },
    ];

    const contentColors = [
    { name: 'Crimson', hex: '#DC143C' },
    { name: 'Red', hex: '#f44336' },
    { name: 'Tomato', hex: '#FF6347' },
    { name: 'Coral', hex: '#FF7F50' },
    { name: 'DarkOrange', hex: '#FF8C00' },
    { name: 'Orange', hex: '#ff9800' },
    { name: 'Gold', hex: '#FFD700' },
    { name: 'Yellow', hex: '#ffeb3b' },
    { name: 'Amber', hex: '#ffc107' },
    { name: 'Lime', hex: '#cddc39' },
    { name: 'Light Green', hex: '#8bc34a' },
    { name: 'Green', hex: '#4caf50' },
    { name: 'Teal', hex: '#009688' }, 
    { name: 'Cyan', hex: '#00bcd4' },
    { name: 'Light Blue', hex: '#03a9f4' },
    { name: 'Blue', hex: '#2196f3' },
    { name: 'SlateBlue', hex: '#6A5ACD' }, // main default
    { name: 'Indigo', hex: '#3f51b5' }, // navbar default
    { name: 'Purple', hex: '#9c27b0' },
    { name: 'Orchid', hex: '#DA70D6' },
    { name: 'Deep Purple', hex: '#673ab7' },
    { name: 'Pink', hex: '#e91e63' },
    { name: 'HotPink', hex: '#FF69B4' },
    { name: 'LightCoral', hex: '#F08080' },
    { name: 'DarkSalmon', hex: '#E9967A' },
    { name: 'Chocolate', hex: '#D2691E' },
    { name: 'Brown', hex: '#795548' },
    { name: 'Light Grey', hex: '#d3d3d3' },
    { name: 'Grey', hex: '#9e9e9e' },
    { name: 'Blue Grey', hex: '#607d8b' },
    ];

    const selectNavbarColor = (hex) => {
      localUser.value.navbar_color = hex;
    };

    const selectContentColor = (hex) => {
      localUser.value.main_content_color = hex;
    };

    const updateProfile = async () => {
      statusMessage.value = "";

      await nextTick();

      if (JSON.stringify(localUser.value) === JSON.stringify(profileStore.user)) {
        statusMessage.value = "No changes made.";
        return;
      }

      const updateResult = await profileStore.updateProfile({ ...localUser.value });
      if (updateResult) {
        statusMessage.value = "Profile updated successfully!";
      } else {
        statusMessage.value = "Failed to update profile.";
      }
    };

    onMounted(async () => {
      await profileStore.fetchUserProfile();
      localUser.value = JSON.parse(JSON.stringify(profileStore.user));
    });

    return {
      user: localUser,
      updateProfile,
      statusMessage,
      navbarColors,
      contentColors,
      selectNavbarColor,
      selectContentColor,
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

.ProfileFormTitle {
  text-align: center;
}

.color-selector {
  display: flex;
  flex-wrap: wrap;
  margin-top: 8px;
  background-color: white;
  padding: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.color-swatch {
  width: 30px;
  height: 30px;
  margin-right: 4px;
  margin-bottom: 4px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: border-color 0.3s ease;
}

.color-swatch:hover {
  border-color: #000;
}

.color-swatch.selected {
  border-color: #000;
}
</style>
