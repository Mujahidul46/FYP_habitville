import { defineStore } from 'pinia';
import { useProfileStore } from './useProfileStore';
import { useNotificationStore } from './useNotificationStore';

export const useHabitsStore = defineStore('habits', {
  state: () => ({
    csrfToken: '',
    habits: [],
    categories: [],
    newHabit: {
      title: '',
      notes: '',
      difficulty: 'ME',
      categories: [],
    },
    editingHabit: null,
  }),
  getters: {
  },
  actions: {
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
    async fetchHabits() {
      try {
        const response = await fetch("http://localhost:8000/list-habits/", {
          credentials: 'include'
        });
        if (response.ok) {
          let fetchedHabits = await response.json();
          this.habits = fetchedHabits.map(habit => ({
            ...habit,
            completions: habit.completions || []
          }));
        } else {
          console.error('Failed to fetch habits:', await response.text());
        }
      } catch (error) {
        console.error('Error fetching habits:', error);
      }
    },
    async createHabit(selectedDifficulty) {
      console.log('Sending new habit with:', JSON.stringify(this.newHabit));
      this.newHabit.difficulty = selectedDifficulty;
      try {
        const response = await fetch("http://localhost:8000/create-habit/", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.csrfToken,
          },
          body: JSON.stringify({
            ...this.newHabit,
            categories: this.newHabit.categories,
          }),
          credentials: 'include',
        });
        if (response.ok) {
          const createdHabit = await response.json();
          createdHabit.completions = [];
          this.habits.push(createdHabit);
          this.resetNewHabit();
        } else {
          console.error('Failed to create habit:', await response.text());
        }
      } catch (error) {
        console.error('Error creating habit:', error);
      }
    },
    resetNewHabit() {
      this.$patch({
        newHabit: {
          title: '',
          notes: '',
          difficulty: 'ME',
          categories: [],
        }
      });
    },
    async updateHabitCompletion(habitId, date, completed) {
      try {
        const response = await fetch(`http://localhost:8000/update-habit-completion/${habitId}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.csrfToken,
          },
          body: JSON.stringify({ date, completed }),
          credentials: 'include',
        });
        if (response.ok) {
          let habit = this.habits.find(h => h.id === habitId);
          let responseData = await response.json();
          if (habit) {
            habit.completions = habit.completions || []; 
            let completion = habit.completions.find(c => c.date === date);
            if (completion) {
              completion.completed = completed;
            } else {
              habit.completions.push({ date, completed });
            }
            
            if (completed && responseData.hp_earned > 0) {
              const profileStore = useProfileStore();
              profileStore.updatePoints(responseData.hp_earned, responseData.lp_earned);

              this.showPointsEarnedNotification(responseData.hp_earned, responseData.lp_earned);
            }
          }
        } else {
          console.error('Failed to update habit completion:', await response.text());
        }
      } catch (error) {
        console.error('Error updating habit completion:', error);
      }
    },

    async updateHabit(habitId, updatedHabitData) {
      console.log(`Updating habit id ${habitId} with:`, updatedHabitData);
      updatedHabitData.categories = Array.from(updatedHabitData.categories);
      try {
        const response = await fetch(`http://localhost:8000/update-habit/${habitId}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.csrfToken,
          },
          body: JSON.stringify(updatedHabitData),
          credentials: 'include',
        });
        if (response.ok) {
          const updatedHabit = await response.json();
          const habitIndex = this.habits.findIndex(h => h.id === habitId);
          if (habitIndex !== -1) {
            this.habits[habitIndex] = { ...this.habits[habitIndex], ...updatedHabit };
          }
        } else {
          console.error('Failed to update habit:', await response.text());
        }
      } catch (error) {
        console.error('Error updating habit:', error);
      }
    },
    
    editHabit(habit) {
      this.editingHabit = { ...habit };
    },
    async deleteHabit(habitId) {
      try {
        const response = await fetch(`http://localhost:8000/delete-habit/${habitId}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': this.csrfToken,
          },
          credentials: 'include',
        });
        if (response.ok) {
          this.habits = this.habits.filter(habit => habit.id !== habitId); // filter out deleted habit from array
        } else {
          console.error('Failed to delete habit:', await response.text());
        }
      } catch (error) {
        console.error('Error deleting habit:', error);
      }
    },
    showPointsEarnedNotification(hp, lp) {
      const notificationStore = useNotificationStore();
      let message = `You earned ${hp} Habit Points`;
      if (lp > 0) { // Add life points part of message only if more than 0 were earned
        message += ` and ${lp.toFixed(2)} Life Points`;
      }
      message += '!';
      notificationStore.addNotification(message);
    },
    async fetchCategories() {
      try {
        const response = await fetch("http://localhost:8000/list-categories/", {
          credentials: 'include'
        });
        if (response.ok) {
          this.categories = await response.json();
        } else {
          console.error('Failed to fetch categories:', await response.text());
        }
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
  },
});