<template>
  <div class="habit-tracker-container">
    
    <button class="add-habit-btn" @click="showAddHabitModal = true">Add Habit</button>

    <!-- Date Navigation -->
    <div class="date-navigation">
      <!-- Left Arrow -->
      <button class="nav-arrow left-arrow" @click="changeDate(4)" :class="{'invisible': isMostRecentDate}">←</button>
      <!-- Date Header -->
      <div class="date-header">
        <div class="date-cell-placeholder"></div> <!-- Placeholder div for alignment -->
        <div class="date-cell" v-for="date in displayedDates" :key="date" v-html="formatDate(date)"></div>
        <div class="date-cell-placeholder"></div> <!-- Placeholder div for alignment -->
      </div>
      <!-- Right Arrow -->
      <button class="nav-arrow right-arrow" @click="changeDate(-4)" :class="{'invisible': isOldestDate}">→</button>
    </div>

    <!-- Modal for addingh abit -->
    <div v-if="showAddHabitModal" class="modal-backdrop">
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
      <!-- Rows for habits and tick/cross status -->
      <div v-for="habit in habits" :key="habit.id" class="habit-row">
        <div class="habit-name" @click="openEditHabitModal(habit)">{{ habit.title }}</div>
        <div v-for="date in displayedDates" :key="`${habit.id}-${date}`" class="habit-cell">
          <button @click="toggleHabitCompletion(habit, date)">
            {{ getHabitCompletionStatus(habit, date) ? '✓' : '✕' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Edit habit modal -->
    <div v-if="showEditHabitModal && editingHabit" class="modal-backdrop">
      <div class="modal-content">
        <h2 class="form-title">Edit Habit</h2>
        <form @submit.prevent="submitHabitEdit">
          <label for="editTitleInput">Title<span class="required-asterisk">*</span></label>
          <input id="editTitleInput" v-model="editingHabit.title" placeholder="Edit title" required>
          <label for="editNotesInput">Notes</label>
          <textarea id="editNotesInput" v-model="editingHabit.notes" placeholder="Edit notes"></textarea>
          <div class="modal-footer">
            <button type="button" class="delete-edit-habit-btn" @click="confirmDelete(editingHabit)">Delete</button>
            <button type="button" @click="closeEditModal">Cancel</button>
            <button type="submit">Save Changes</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete habit confirmation modal -->
    <div v-if="showDeleteConfirm" class="modal-backdrop">
      <div class="modal-content">
        <h2 class="form-title">Are you sure you want to delete this habit? This action cannot be undone.</h2>
        <div class="modal-footer">
          <button type="button" @click="cancelDelete">Cancel</button>
          <button type="button" @click="deleteHabit">Delete</button>
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
    const showEditHabitModal = ref(false);
    const showDeleteConfirm = ref(false);
    const currentDate = ref(new Date());
    const maxPastDays = 60;

    const habits = computed(() => habitsStore.habits);

    const editingHabit = computed(() => habitsStore.editingHabit);

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
      const dayOfWeek = format(date, 'E').toUpperCase(); // e.g., WED, TUE, uppercase days
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


    function openEditHabitModal(habit) {
      habitsStore.editHabit(habit);
      showEditHabitModal.value = true;
    }


    function submitHabitEdit() { 
      if (habitsStore.editingHabit) {
        const { id, ...updatedHabitData } = habitsStore.editingHabit;
        habitsStore.updateHabit(id, updatedHabitData);
        closeEditModal();
      }
    }

    function closeEditModal() {
      showEditHabitModal.value = false;
      habitsStore.editingHabit = null; 
    }

    function confirmDelete(habit) {
      showDeleteConfirm.value = true; 
      habitsStore.editingHabit = habit;
    }

    function cancelDelete() { // hides the delete confirmation modal
      showDeleteConfirm.value = false; 
    }

    async function deleteHabit() {
      if (habitsStore.editingHabit) {
        try {
          await habitsStore.deleteHabit(habitsStore.editingHabit.id); // calls stores delete habit
          showDeleteConfirm.value = false; 
          closeEditModal(); 
        } catch (error) {
          console.error('Failed to delete habit:', error);
        }
      }
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
      showEditHabitModal,
      openEditHabitModal,
      submitHabitEdit,
      closeEditModal,
      editingHabit,
      deleteHabit,
      showDeleteConfirm,
      confirmDelete,
      cancelDelete,

    };
  },
};
</script>

<style scoped>
.habit-tracker-container {
  width: 750px; 
  min-height: 600px;
  border: 2px solid #4CAF50;
  margin-right: 20px; 
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  padding: 1em;
  background-color: #bcdbba; 
  float: left; 
}

.nav-arrow {
  padding: 0.5em;
  background-color: #8bc34a; 
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-habit-btn {
  display: block;
  margin-left: auto;
  padding: 0.5em;
  background-color: #8bc34a; 
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 1em;
}

.date-navigation {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1em;
}

.date-header {
  display: flex;
  gap: 0.5em; 
  flex-grow: 1;
  justify-content: center;
}

.habit-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr); 
  align-items: center;
  gap: 0.5em;
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
  font-weight: bold; 
  font-family: 'Helvetica Neue', Arial, sans-serif; 
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
  word-break: break-word;
  hyphens: auto;
  font-weight: bold; 
  font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; 
  transition: border-color 0.3s ease; 
  padding: 10px; 
  border: 2px solid transparent; 
  border-radius: 6px; 
  cursor: pointer; 
  display: flex;
  align-items: center; 
}

.habit-name:hover {
  border-color: #faa404; 
}


.habit-cell button {
  background-color: transparent;
  border: none;
  cursor: pointer;
}

.form-title {
  text-align: center;
  margin-top: 0; 
  margin-bottom: 1rem; 
}

.invisible {
  visibility: hidden; 
}

</style>