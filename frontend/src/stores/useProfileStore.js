import { defineStore } from 'pinia';

export const useProfileStore = defineStore('profile', {
  state: () => ({
    user: {
      username: '',
      email: '',
      goals: '',
    },
    statusMessage: ''
  }),
  getters: {
  },
  actions: {
    async fetchUserProfile() {
      try {
        const response = await fetch("http://localhost:8000/user/", {
          method: "GET",
          credentials: "include",
        });

        if (response.ok) {
            const userData = await response.json();
            console.log("Fetched user data:", userData); 
            this.user = userData;
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
    },
    async updateProfile(userData) {
      try {
        const response = await fetch("http://localhost:8000/user/update/", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(userData),
          credentials: "include",
        });
    
        if (response.ok) {
          const data = await response.json();
          this.user = data; 
          this.statusMessage = "Profile updated successfully"; 
          return true; 
        } else {
          this.statusMessage = "Failed to update profile. Please try again.";
          return false; 
        }
      } catch (error) {
        this.statusMessage = "An error occurred while updating the profile.";
        return false; 
      }
    },
    
      
    }
});
