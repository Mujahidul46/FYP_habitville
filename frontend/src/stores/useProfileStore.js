import { defineStore } from 'pinia';

export const useProfileStore = defineStore('profile', {
  state: () => ({
    user: {
      username: '',
      email: '',
      goals: '',
      habit_points: 0,  
      life_points: 0.00,
      navbar_color: '#8bc34a',
      main_content_color: '#009688',
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
          this.user = {
            ...this.user,
            ...userData,
            habit_points: parseInt(userData.habit_points, 10) || 0,
            life_points: parseFloat(userData.life_points) || 0.00,
            navbar_color: userData.navbar_color,
            main_content_color: userData.main_content_color,
          };
          console.log("Fetched user data:", this.user); 
        } else {
          console.error(
            "Failed to fetch user data:",
            response.status,
            response.statusText
          );
          this.statusMessage = "Failed to fetch user profile.";
        }
      } catch (error) {
        console.error("Error during fetch:", error);
        this.statusMessage = "An error occurred while fetching the user profile.";
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
          const updatedUserData = await response.json();
          this.user = {
            ...this.user,
            ...updatedUserData,
            habit_points: parseInt(updatedUserData.habit_points, 10) || 0,
            life_points: parseFloat(updatedUserData.life_points) || 0.00,
            navbar_color: updatedUserData.navbar_color,
            main_content_color: updatedUserData.main_content_color,
          };
          this.statusMessage = "Profile updated successfully";
          return true;
        } else {
          this.statusMessage = "Failed to update profile. Please try again.";
          return false;
        }
      } catch (error) {
        console.error("Error during profile update:", error);
        this.statusMessage = "An error occurred while updating the profile.";
        return false;
      }
    },   
    updatePoints(hp, lp) {
      this.user.habit_points += parseInt(hp, 10);
      const parsedLP = parseFloat(lp);
      if (!isNaN(parsedLP)) {
        this.user.life_points += parsedLP;
      }
    },
    spendLifePoints(cost) {
      const lifePointsCost = parseFloat(cost);
      if (!isNaN(lifePointsCost)) {
        this.user.life_points -= lifePointsCost;
        this.user.life_points = parseFloat(this.user.life_points.toFixed(2));
      }
    },
      
    }
});