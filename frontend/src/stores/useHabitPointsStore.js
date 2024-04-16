import { defineStore } from 'pinia';
import { useProfileStore } from '@/stores/useProfileStore';

export const useHabitPointsStore = defineStore('habitPoints', {
  state: () => ({
    habitPoints: 0
  }),
  getters: {
  },
  actions: {
    async fetchHabitPoints() {
      try {
        const response = await fetch("http://localhost:8000/user/", {
          method: "GET",
          credentials: "include",
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          const data = await response.json();
          this.habitPoints = data.habit_points;
        } else {
          console.error('Failed to fetch habit points:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error during fetch:', error);
      }
    },
    async spendHabitPointsForMinigame(csrfToken) {
        if (this.habitPoints < 100) {
          alert('Not enough habit points to play the minigame.');
          throw new Error('Not enough habit points');
        }
  
        try {
          const response = await fetch("http://localhost:8000/spend-habit-points-for-minigame/", {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken
            },
            credentials: 'include',
            body: JSON.stringify({})
          });
  
          const data = await response.json();
          if (response.ok) {
            this.habitPoints = data.new_habit_points;
            
            const profileStore = useProfileStore();
            profileStore.spendHabitPoints(100);
          } else {
            console.error('Failed to spend habit points:', data.message);
            alert(data.message);
          }
        } catch (error) {
          console.error('Error spending habit points:', error);
          alert('An error occurred while spending habit points.');
        }
      }
  }
});
