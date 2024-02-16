import { defineStore } from 'pinia';
import { useProfileStore } from './useProfileStore';
import { useNotificationStore } from './useNotificationStore';

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
          return true;
        } else {
          console.error('Failed to add reward:', response.statusText);
          return false;
        }
      } catch (error) {
        console.error('Error adding reward:', error);
        return false;
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
    async spendReward(rewardId, cost) {
      try {
        const response = await fetch(`http://localhost:8000/spend-reward/${rewardId}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.csrfToken,
          },
          body: JSON.stringify({ cost: cost }),
          credentials: 'include',
        });
        const responseData = await response.json();
        const notificationStore = useNotificationStore();
    
        if (response.ok) {
          const profileStore = useProfileStore();
          profileStore.spendLifePoints(cost);
          notificationStore.addNotification(`You spent ${cost} Life Points.`);
    
          this.fetchRewards();
          profileStore.fetchUserProfile();
        } else {
          notificationStore.addNotification(responseData.message);
        }
      } catch (error) {
        console.error('Error spending reward:', error);
        const notificationStore = useNotificationStore();
        notificationStore.addNotification("An error occurred while trying to spend Life Points.");
      }
    },
    async deleteReward(rewardId) {
      try {
        const response = await fetch(`http://localhost:8000/delete-reward/${rewardId}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': this.csrfToken,
          },
          credentials: 'include',
        });
        if (response.ok) {
          await this.fetchRewards();
          const notificationStore = useNotificationStore();
          notificationStore.addNotification("Reward successfully deleted.");
        } else {
          console.error('Failed to delete reward:', response.statusText);
          const notificationStore = useNotificationStore();
          notificationStore.addNotification("Failed to delete reward.");
        }
      } catch (error) {
        console.error('Error deleting reward:', error);
        const notificationStore = useNotificationStore();
        notificationStore.addNotification("An error occurred while trying to delete the reward.");
      }
    },
    async updateReward(updatedReward) {
      try {
        const response = await fetch(`http://localhost:8000/update-reward/${updatedReward.id}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.csrfToken,
          },
          body: JSON.stringify({
            name: updatedReward.name,
            notes: updatedReward.notes,
            cost: updatedReward.cost,
          }),
          credentials: 'include',
        });
        const responseData = await response.json();
        const notificationStore = useNotificationStore();

        if (response.ok) {
          this.rewards = this.rewards.map(reward => 
            reward.id === updatedReward.id ? { ...reward, ...responseData } : reward
          );
          notificationStore.addNotification(`Reward updated successfully.`);
        } else {
          console.error('Failed to update reward:', response.statusText);
          notificationStore.addNotification(responseData.message);
        }
      } catch (error) {
        console.error('Error updating reward:', error);
        const notificationStore = useNotificationStore();
        notificationStore.addNotification("An error occurred while trying to update the reward.");
      }
    },
  },
});
