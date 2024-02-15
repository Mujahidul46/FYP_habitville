import { defineStore } from 'pinia';

export const useRewardsStore = defineStore('rewards', {
  state: () => ({
    rewards: [],
    csrfToken: '',
  }),
  actions: {
    async fetchRewards() {
      try {
        const response = await fetch("http://localhost:8000/list-rewards/", {
          method: 'GET',
          credentials: 'include',
        });
        if (response.ok) {
          this.rewards = await response.json();
        } else {
          console.error('Failed to fetch rewards:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching rewards:', error);
      }
    },
    async addReward(newReward) {
      try {
        const response = await fetch("http://localhost:8000/create-reward/", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.csrfToken,
          },
          body: JSON.stringify(newReward),
          credentials: 'include',
        });
        if (response.ok) {
          await this.fetchRewards();
        } else {
          console.error('Failed to add reward:', response.statusText);
        }
      } catch (error) {
        console.error('Error adding reward:', error);
      }
    },
    async fetchCSRFToken() {
      try {
        const response = await fetch("http://localhost:8000/csrf/", {
          credentials: 'include'
        });
        const data = await response.json();
        this.csrfToken = data.csrfToken;
      } catch (error) {
        console.error('Error fetching CSRF token:', error);
      }
    },
  },
});
