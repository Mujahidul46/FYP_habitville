<template>
    <div>
      <button @click="showAddHabitModal">Add Habit</button>
      <div v-if="showHabitForm">
        <!-- Habit Form -->
        <form @submit.prevent="submitHabit">
          <input type="text" v-model="newHabit.title" placeholder="Habit Title" required>
          <textarea v-model="newHabit.notes" placeholder="Notes (optional)"></textarea>
          <button type="submit">Save Habit</button>
        </form>
      </div>
  
      <!-- Habits list -->
      <ul>
        <li v-for="habit in habits" :key="habit.id">
          {{ habit.title }}
          <button @click="toggleHabitCompletion(habit)">
            {{ habit.completed ? '✓' : 'X' }}
          </button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import { ref, toRefs } from 'vue';
  import { useHabitsStore } from '@/stores/useHabitsStore';
  
  export default {
    name: 'DailyHabits',
    setup() {
      const habitsStore = useHabitsStore();
      const { csrfToken, newHabit, habits } = toRefs(habitsStore);
      const showHabitForm = ref(false);
  
      const showAddHabitModal = () => {
        showHabitForm.value = true;
      };
  
      const submitHabit = async () => {
        await habitsStore.addHabit();
        await habitsStore.fetchHabits(); 
      };
  
      const toggleHabitCompletion = async (habit) => {
        await habitsStore.updateHabitStatus(habit);
      };
  
      habitsStore.fetchHabits();
  
      return {
        csrfToken,
        newHabit,
        habits,
        showHabitForm,
        showAddHabitModal,
        submitHabit,
        toggleHabitCompletion,
      };
    },
  };
  </script>
  