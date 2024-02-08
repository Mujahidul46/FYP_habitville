<template>
  <div class="habit-tracker-container">
    
    <!-- Go forward or back 4 days, and "Add Habit" button.  -->
    <div class="controls">
      <button class="nav-arrow" @click="changeDate(-4)" v-if="!isOldestDate">←</button>
      <button class="nav-arrow" @click="changeDate(4)" v-if="!isMostRecentDate">→</button>
      <button class="add-habit-btn" @click="showAddHabitModal = true">Add Habit</button>
    </div>

    <!-- Modal that shows after "Add Habit" clicked -->
    <div v-if="showAddHabitModal" class="modal">
      <div class="modal-backdrop" @click="closeModal"></div>
      <div class="modal-content">
        <form @submit.prevent="createHabit">
          <div class="form-group">
            <label for="title">Title*:</label>
            <input type="text" id="title" v-model="newHabit.title" required>
          </div>
          <div class="form-group">
            <label for="notes">Notes:</label>
            <textarea id="notes" v-model="newHabit.notes"></textarea>
          </div>
          <div class="modal-footer">
            <button type="button" @click="closeModal">Cancel</button>
            <button type="submit">Submit</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Habit grid display -->
    <div class="habit-grid">
      <!-- Column headers for dates -->
      <div class="date-header">
        <!-- No habit header -->
        <div class="date-cell-placeholder"></div>
        <!-- Date cells -->
        <div class="date-cell" v-for="date in displayedDates" :key="date" v-html="formatDate(date)"></div>

      </div>

      <!-- Rows for habits and tick/cross status -->
      <div v-for="habit in habits" :key="habit.id" class="habit-row">
        <div class="habit-name">{{ habit.title }}</div>
        <!-- tick/cross cells -->
        <div v-for="date in displayedDates" :key="`${habit.id}-${date}`" class="habit-cell">
          <button @click="toggleHabitCompletion(habit, date)">
            {{ getHabitCompletionStatus(habit, date) ? '✓' : '✕' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { ref, computed, onMounted } from 'vue';
import { useHabitsStore } from '@/stores/useHabitsStore';
import { format, subDays, addDays } from 'date-fns';

export default {
  name: 'DailyHabits',
  setup() {
    const habitsStore = useHabitsStore();
    const showAddHabitModal = ref(false);
    const currentDate = ref(new Date());
    const maxPastDays = 60;

    const habits = computed(() => habitsStore.habits);

    const displayedDates = computed(() => { // array of today and past 3 days
      let dates = [];
      for (let i = 0; i < 4; i++) {
        dates.push(subDays(currentDate.value, i));
      }
      return dates.reverse();
    });

    const isOldestDate = computed(() => {
      const oldestDisplayedDate = displayedDates.value[0];
      const oldestAllowableDate = subDays(new Date(), maxPastDays - 3); 
      return oldestDisplayedDate.setHours(0, 0, 0, 0) <= oldestAllowableDate.setHours(0, 0, 0, 0);
    });


    const isMostRecentDate = computed(() => {
      const mostRecentDisplayedDate = displayedDates.value[displayedDates.value.length - 1];
      return mostRecentDisplayedDate.setHours(0, 0, 0, 0) >= new Date().setHours(0, 0, 0, 0);
    });


    function changeDate(days) {
      const newDate = addDays(currentDate.value, days);
      if (newDate <= new Date()) {
        currentDate.value = newDate;
      }
    }

    function formatDate(date) {
      const dayOfWeek = format(date, 'E'); // E.g. Wed
      const dayOfMonth = format(date, 'dd'); // E.g. 07
      return `<span class="day-of-week">${dayOfWeek}</span><span class="day-of-month">${dayOfMonth}</span>`;
    }


    function toggleHabitCompletion(habit, date) { // 'X' -> tick or vice versa
      habitsStore.updateHabitCompletion(habit.id, date.toISOString().split('T')[0], !getHabitCompletionStatus(habit, date));
    }

    function getHabitCompletionStatus(habit, date) { // checks if tick or cross
      return habit.completions.some(completion => completion.date === date.toISOString().split('T')[0] && completion.completed);
    }

    function createHabit() {
      habitsStore.createHabit();
      closeModal(); 
    }

    function closeModal() {
      showAddHabitModal.value = false;
      habitsStore.resetNewHabit(); 
    }

    onMounted(() => {
      habitsStore.fetchHabits();
    });

    return {
      showAddHabitModal,
      closeModal, 
      habits,
      newHabit: habitsStore.newHabit,
      displayedDates,
      isOldestDate,
      isMostRecentDate,
      changeDate,
      formatDate,
      toggleHabitCompletion,
      getHabitCompletionStatus,
      createHabit,
    };
  },
};
</script>

<style scoped>
.habit-tracker-container {
  width: 500px; 
  min-height: 600px;
  border: 2px solid #4CAF50;
  margin-right: 20px; 
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  padding: 1em;
  background-color: #bcdbba; 
  float: left; 
}

.controls {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1em;
}

.controls .nav-arrow,
.controls .add-habit-btn {
  padding: 0.5em;
  background-color: #8bc34a; 
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}



.habit-grid {
  display: grid;
  grid-template-columns: 200px repeat(4, 1fr); 
  gap: 0.5em; 
  align-items: center;
}

.date-header,
.habit-row {
  display: contents; 
}

.date-cell,
.habit-cell {
  text-align: center;
  padding: 0.5em;
  display: flex;
  flex-direction: column; 
  align-items: center;
  justify-content: center;
  min-width: 60px; 
}

.date-cell {
  border-right: 1px solid #ccc;
}

.date-cell:last-child,
.habit-cell:last-child {
  border-right: none;
}

.day-of-week,
.day-of-month {
  display: block; 
}

.habit-cell:not(:last-child) {
  border-right: 1px solid #ccc; 
}


.habit-name {
  grid-column: 1 / 2; 
  flex: none; 
}

.habit-cell button {
  background-color: transparent;
  border: none;
  cursor: pointer;
}


.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999; 
}

.modal-backdrop {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.8); 
}

.modal-content {
  background-color: #FFF;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
  width: auto;
  max-width: 500px;
  z-index: 10000; 
}

.modal-content input,
.modal-content textarea {
  width: calc(100% - 20px);
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.modal-footer {
  display: flex;
  justify-content: space-between;
}

.modal-footer button {
  margin-left: 10px;
  margin-right: 10px;
}

.modal-footer button[type="submit"] {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.modal-footer button[type="button"] {
  border: none;
  padding: 10px 20px;
  cursor: pointer;
}

</style>