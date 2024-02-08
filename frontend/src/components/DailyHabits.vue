<template>
  <div class="habit-tracker-container">
    <!-- Go forward or back 4 days, and "Add Habit" button.  -->
    <div class="controls">
      <button class="nav-arrow" @click="changeDate(4)" v-if="!isMostRecentDate">←</button>
      <button class="nav-arrow" @click="changeDate(-4)" v-if="!isOldestDate">→</button>
      <button class="add-habit-btn" @click="showAddHabitModal = true">Add Habit</button>
    </div>

    <!-- Modal that shows after "Add Habit" clicked -->
    <div v-if="showAddHabitModal" class="modal-backdrop" @click.self="closeModal">
      <div class="modal-content">
        <h2 class="form-title">Create Habit</h2>
        <form @submit.prevent="createHabit">
          <label for="titleInput">Title<span class="required-asterisk">*</span></label>
          <input id="titleInput" v-model="newHabit.title" placeholder="Add a title" required>
          <label for="notesInput">Notes</label>
          <textarea id="notesInput" v-model="newHabit.notes" placeholder="Add notes"></textarea>
          <div class="modal-footer">
            <button type="button" @click="closeModal">Cancel</button>
            <button type="submit">Create</button>
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
      return dates;
    });

    const isOldestDate = computed(() => {
      const oldestDisplayedDate = displayedDates.value[displayedDates.value.length - 1];
      const oldestAllowableDate = subDays(new Date(), maxPastDays); 
      return oldestDisplayedDate.setHours(0, 0, 0, 0) <= oldestAllowableDate.setHours(0, 0, 0, 0);
    });

    const isMostRecentDate = computed(() => {
      const mostRecentDisplayedDate = displayedDates.value[0];
      return mostRecentDisplayedDate.setHours(0, 0, 0, 0) === new Date().setHours(0, 0, 0, 0);
    });


    function changeDate(days) {
      const newDate = addDays(currentDate.value, days);
      if (newDate.setHours(0, 0, 0, 0) <= new Date().setHours(0, 0, 0, 0)) {
        currentDate.value = newDate;
      }
    }

    function formatDate(date) {
      const dayOfWeek = format(date, 'E'); // E.g., Wed
      const dayOfMonth = format(date, 'd'); // E.g., 7, or 17, no leading 0 for single digit dates
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

</style>