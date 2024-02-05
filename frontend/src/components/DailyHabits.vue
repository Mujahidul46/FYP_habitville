<template>
  <div class="habit-tracker-container">
    <div class="habit-list-container">
      <button class="add-habit-btn" @click="showAddHabitModal">Add Habit</button>
      <div v-if="showHabitForm" class="modal-backdrop">
        <!-- Habit Form form -->
        <div class="modal-content">
          <h2 class="form-title">Create Habit</h2>
          <form @submit.prevent="submitHabit">
            <input type="text" v-model="newHabit.title" placeholder="Habit Title*" required>
            <textarea v-model="newHabit.notes" placeholder="Notes"></textarea>
            <div class="modal-footer">
              <button type="button" @click="showHabitForm = false">Cancel</button>
              <button type="submit">Save Habit</button>
            </div>
          </form>
        </div>
      </div>
  
      <ul v-if="!showHabitForm">
        <li v-for="habit in habits" :key="habit.id" class="habit-item">
          <div class="habit-content">
            <h3>{{ habit.title }}</h3>
            <p>{{ habit.notes }}</p>
          </div>
          <button class="habit-status-btn" @click="toggleHabitCompletion(habit)">
            {{ habit.completed ? '✓' : 'X' }}
          </button>
        </li>
      </ul>
    </div>
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
        showHabitForm.value = false; 
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
  

  <style scoped>
  .habit-tracker-container {
    width: 500px; 
    min-height: 600px;
    border: 2px solid #4CAF50;
    margin: auto;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    padding: 1em;
    background-color: #bcdbba;
    position: relative;
  }

  .habit-list-container {
  padding-top: 50px; 
}
  
  .add-habit-btn {
    position: absolute;
    top: 20px;
    right: 20px;
    cursor: pointer;
    padding: 0.5em;
    background-color: #8bc34a;
    color: white;
    border: none;
    transition: background-color 0.3s ease;
  }
  
  .add-habit-btn:hover {
    background-color: #add681;
  }
  
  .habit-item {
    transition: border-color 0.3s ease;
    cursor: pointer;
    padding: 10px;
    border: 2px solid transparent;
    border-radius: 10px;
    display: flex;
    align-items: center;
    background-color: #bcdbba; 
    margin-bottom: 1em;
  }
  
  .habit-item:hover {
    border-color: #faa404;
  }
  
  .habit-content {
    flex-grow: 1;
    padding: 5px;
    text-align: left;
  }
  
  .habit-content h3 {
    word-break: break-all;
    margin: 0;
    font-size: 18px;
  }
  
  .habit-content p {
    word-break: break-all;
    margin: 0;
    font-size: 14px;
  }
  
  .habit-status-btn {
    padding: 0.5em;
    margin-left: 10px;
    background-color: #4CAF50; 
    color: white;
    border: none;
  }
  
  </style>
  