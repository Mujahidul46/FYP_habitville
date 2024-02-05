import { defineStore } from 'pinia';

export const useHabitsStore = defineStore('habits', {
  state: () => ({
    csrfToken: '',
    newHabit: {
      title: '',
      notes: ''
    },
    habits: [],
    currentView: 'habits',
    showHabitForm: false,
    editingHabit: null,
  }),
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
        const response = await fetch("http://localhost:8000/habits/", {
          credentials: 'include'
        });
        if (response.ok) {
          const fetchedHabits = await response.json();
          this.habits = fetchedHabits;
        } else {
          console.error('Failed to fetch habits:', await response.text());
        }
      } catch (error) {
        console.error('Error fetching habits:', error);
      }
    },
    async addHabit() {
      try {
        const response = await fetch("http://localhost:8000/habits/create/", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.csrfToken,
          },
          body: JSON.stringify(this.newHabit),
          credentials: 'include',
        });
        if (response.ok) {
          const createdHabit = await response.json();
          this.habits.push(createdHabit);
          this.resetForm(); 
          this.showHabitForm = false;
        } else {
          console.error('Failed to add habit:', await response.text());
        }
      } catch (error) {
        console.error('Error adding habit:', error);
      }
    },
    async updateHabitStatus(habit) {
      try {
        const response = await fetch(`http://localhost:8000/habits/update/${habit.id}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.csrfToken,
          },
          body: JSON.stringify({ completed: !habit.completed }),
          credentials: 'include',
        });
        if (response.ok) {
          const updatedHabit = await response.json();
          const index = this.habits.findIndex(h => h.id === habit.id);
          if (index !== -1) {
            this.habits[index] = updatedHabit;
          }
        } else {
          console.error('Failed to update habit status:', await response.text());
        }
      } catch (error) {
        console.error('Error updating habit status:', error);
      }
    },
    resetForm() {
      this.newHabit.title = '';
      this.newHabit.notes = '';
      this.editingHabit = null;
    },
  }
});
