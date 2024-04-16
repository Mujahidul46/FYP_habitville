<template>
  <div class="habit-tracker-container">
    <!-- Add Habit Button -->
    <button class="add-habit-btn" @click="openAddHabitModal">Add Habit</button>

    <div v-if="habits.length">
      <!-- Date Navigation -->
      <div class="date-navigation">
        <!-- Left Arrow -->
        <!--<button class="nav-arrow left-arrow" @click="changeDate(4)" :class="{'invisible': isMostRecentDate}">←</button>-->
        <button class="nav-arrow left-arrow" @click="changeDate(4)">←</button>
        <!-- Date Header -->
        <div class="date-header">
          <div class="date-cell-placeholder"></div> <!-- Placeholder div for alignment -->
          <div class="date-cell-placeholder"></div> <!-- Placeholder div for alignment -->
          <div class="date-cell-placeholder"></div> <!-- Placeholder div for alignment -->
          <div class="date-cell-placeholder"></div> <!-- Placeholder div for alignment -->
          <div class="date-cell" v-for="date in displayedDates" :key="date" v-html="formatDate(date)"></div>
          <div class="date-cell-placeholder placeholder-adjustment"></div> <!-- Placeholder div for alignment -->
        </div>
        <!-- Right Arrow -->
        <button class="nav-arrow right-arrow" @click="changeDate(-4)" :class="{'invisible': isOldestDate}">→</button>
      </div>
    </div>

    <!-- Modal for Adding Habit -->
    <div v-if="isAddHabitModalVisible" class="modal-backdrop">
      <div class="modal-content">
        <h2 class="form-title">Create Habit</h2>
        <form @submit.prevent="createHabit">
          <!-- Habit Title Input -->
          <label for="titleInput">Title<span class="required-asterisk">*</span></label>
          <input id="titleInput" v-model="newHabit.title" placeholder="Add a title" required>
          <!-- Habit Categories Select -->
          <fieldset class="categories-section">
            <legend>Categories</legend>
            <div class="categories-container">
              <div v-for="category in categories" :key="category.id" class="category-item">
                <input type="checkbox" :id="'add-' + category.name" :value="category.id" v-model="selectedCategories" class="category-checkbox">
                <label :for="'add-' + category.name" class="category-label">{{ category.name }}</label>
              </div>
            </div>
          </fieldset>
          <!-- Habit Notes Input -->
          <label for="notesInput">Notes</label>
          <textarea id="notesInput" v-model="newHabit.notes" placeholder="Add notes"></textarea>
          <!-- Habit Difficulty Select -->
          <label for="difficultySelect">Difficulty</label>
          <select id="difficultySelect" v-model="selectedDifficulty">
            <option value="TR">Trivial</option>
            <option value="EA">Easy</option>
            <option value="ME">Medium</option>
            <option value="HA">Hard</option>
          </select>
          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" @click="closeAddHabitModal">Cancel</button>
            <button type="submit">Create</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Habit Grid Display -->
    <div v-if="truncatedHabits.length" class="habit-grid">
      <!-- Habit Rows -->
      <div v-for="habit in truncatedHabits" :key="habit.id" class="habit-row">
        <!-- Habit Name -->
        <div class="habit-name" @click="() => openEditHabitModal(habit)">{{ habit.title }}</div>
        <!-- Habit Completion Cells -->
        <div v-for="date in displayedDates" :key="`${habit.id}-${date}`" class="habit-cell">
          <button @click="() => toggleHabitCompletion(habit, date)" class="habit-button">
            <!-- Icons for habit status -->
            <i v-if="getHabitCompletionStatus(habit, date)" class="fas fa-tree"></i>
            <i v-else-if="isDateToday(date)" class="fas fa-seedling"></i>
            <img v-else :src="deadTreeIcon" alt="Dead Tree" class="icon-dead-tree"/>
          </button>
        </div>
      </div>
    </div>

    <!-- Message if No Habits -->
    <div v-else class="empty-habit-list">
      <div class="empty-habit-content">
        <h3 class="empty-title">You have no daily habits</h3>
        <p>Add a new habit to start earning Habit Points (HP) and Life Points (LP)!</p>
      </div>
    </div>

      <!-- Edit Habit Modal -->
    <div v-if="isEditHabitModalVisible && editingHabit" class="modal-backdrop">
      <div class="modal-content">
        <h2 class="form-title">Edit Habit</h2>
        <form @submit.prevent="submitHabitEdit">
          <!-- Edit Habit Title Input -->
          <label for="editTitleInput">Title<span class="required-asterisk">*</span></label>
          <input id="editTitleInput" v-model="editingHabit.title" placeholder="Edit title" required>
          <!-- Categories Section for Editing -->
          <fieldset class="categories-section">
            <legend>Categories</legend>
            <div class="categories-container">
              <div v-for="category in categories" :key="category.id" class="category-item">
                <input type="checkbox" :id="'edit-' + category.id" :value="category.id" v-model="editingSelectedCategories" class="category-checkbox">
                <label :for="'edit-' + category.id" class="category-label">{{ category.name }}</label>
              </div>
            </div>
          </fieldset>
          <!-- Edit Habit Notes Input -->
          <label for="editNotesInput">Notes</label>
          <textarea id="editNotesInput" v-model="editingHabit.notes" placeholder="Edit notes"></textarea>
          <!-- Edit Habit Difficulty Select -->
          <label for="editDifficultySelect">Difficulty</label>
          <select id="editDifficultySelect" v-model="selectedDifficulty">
            <option value="TR">Trivial</option>
            <option value="EA">Easy</option>
            <option value="ME">Medium</option>
            <option value="HA">Hard</option>
          </select>
          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="delete-edit-habit-btn" @click="confirmDelete(editingHabit)">Delete</button>
            <button type="button" @click="closeEditHabitModal">Cancel</button>
            <button type="submit">Save Changes</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Habit Confirmation Modal -->
    <div v-if="isDeleteConfirmVisible" class="modal-backdrop">
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
import { format, subDays, addDays, isToday } from 'date-fns';
import deadTreeIcon from '@/assets/dead_tree_1.png';
import completeHabitSound from '@/assets/sounds/complete_habit.mp3';
import wateringCanIcon from '@/assets/watering_can_1.png';
import { watchEffect } from 'vue';
import { useProfileStore } from '@/stores/useProfileStore';

export default {
  name: 'DailyHabits',
  setup() {
    const habitsStore = useHabitsStore();
    const isAddHabitModalVisible = ref(false); 
    const isEditHabitModalVisible = ref(false); 
    const isDeleteConfirmVisible = ref(false); 
    const currentDate = ref(new Date());
    const maxPastDays = 60;
    const selectedDifficulty = ref('ME');
    const selectedCategories = ref([]);

    const habits = computed(() => habitsStore.habits);
    const editingHabit = computed(() => habitsStore.editingHabit);

    const editingSelectedCategories = ref([]);

    const categories = computed(() => habitsStore.categories);
    const profileStore = useProfileStore();

    watchEffect(() => {
      document.documentElement.style.setProperty('--container-bg-color', profileStore.user.main_content_color);
    });

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

    const completeHabitSoundEffect = new Audio(completeHabitSound);

    const truncatedHabits = computed(() => { // no longer than 2 lines for a habit name (37 characters)
      if (!habits.value) {
        return []; 
      }
      return habits.value.map(habit => {
        if (habit && habit.title) {
          return {
            ...habit,
            title: habit.title.length > 37 ? habit.title.substring(0, 37) + '...' : habit.title
          };
        }
        return habit; 
      });
    });

    function playSound() {
      // restarts sound from beginning
      completeHabitSoundEffect.currentTime = 0;
      completeHabitSoundEffect.play().catch(error => console.error("Failed to play sound", error));
    }

    function changeDate(days) {
      const newDate = addDays(currentDate.value, days);
      if (newDate.setHours(0, 0, 0, 0) <= new Date().setHours(0, 0, 0, 0)) {
        currentDate.value = newDate;
      }
    }

    function formatDate(date) {
      const dayOfWeek = format(date, 'E').toUpperCase();
      const dayOfMonth = format(date, 'd');
      return `<span class="day-of-week">${dayOfWeek}</span><span class="day-of-month">${dayOfMonth}</span>`;
    }

    function toggleHabitCompletion(habit, date) {
      if (!getHabitCompletionStatus(habit, date)) {
        playSound();
      }
      habitsStore.updateHabitCompletion(habit.id, date.toISOString().split('T')[0], !getHabitCompletionStatus(habit, date));
    }

    function getHabitCompletionStatus(habit, date) {
      return habit.completions.some(completion => completion.date === date.toISOString().split('T')[0] && completion.completed);
    }

    function createHabit() {
      habitsStore.newHabit.categories = selectedCategories.value;
      habitsStore.createHabit(selectedDifficulty.value);
      closeAddHabitModal();
    }

    function closeAddHabitModal() {
      isAddHabitModalVisible.value = false;
      habitsStore.resetNewHabit();
    }

    function openAddHabitModal() {
      isAddHabitModalVisible.value = true;
      selectedDifficulty.value = 'ME'; // Resets to medium difficulty
      selectedCategories.value = [];
    }

    function openEditHabitModal(habit) {
      const fullHabit = habits.value.find(h => h.id === habit.id); // find full habit object by using its id
      habitsStore.editHabit(fullHabit);
      editingSelectedCategories.value = [...fullHabit.categories];
      isEditHabitModalVisible.value = true;
    }

    function submitHabitEdit() {
      if (editingHabit.value) {
        const updatedHabitData = {
          title: editingHabit.value.title,
          notes: editingHabit.value.notes,
          difficulty: selectedDifficulty.value,
          categories: editingSelectedCategories.value,
        };
        habitsStore.updateHabit(editingHabit.value.id, updatedHabitData);
        closeEditHabitModal();
      }
    }


    function closeEditHabitModal() {
      isEditHabitModalVisible.value = false;
      habitsStore.editingHabit = null;
    }

    function confirmDelete(habit) {
      isDeleteConfirmVisible.value = true;
      habitsStore.editingHabit = habit;
    }

    function cancelDelete() {
      isDeleteConfirmVisible.value = false;
    }

    function isDateToday(date) {
      return isToday(date);
    }

    async function deleteHabit() {
      if (habitsStore.editingHabit) {
        await habitsStore.deleteHabit(habitsStore.editingHabit.id);
        isDeleteConfirmVisible.value = false;
        closeEditHabitModal();
      }
    }

    function editHabit(habit) {
      habitsStore.editHabit(habit);
      selectedDifficulty.value = habit.difficulty;
      isEditHabitModalVisible.value = true;
    }

    onMounted(() => {
      habitsStore.fetchHabits();
      habitsStore.fetchCategories();
    });

    return {
      isAddHabitModalVisible,
      closeAddHabitModal,
      openAddHabitModal,
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
      isEditHabitModalVisible,
      openEditHabitModal,
      submitHabitEdit,
      closeEditHabitModal,
      editingHabit,
      deleteHabit,
      isDeleteConfirmVisible,
      confirmDelete,
      cancelDelete,
      isDateToday,
      deadTreeIcon,
      wateringCanIcon,
      selectedDifficulty,
      truncatedHabits,
      selectedCategories,
      categories,
      editingSelectedCategories,
    };
  },
};
</script>

<style scoped>
.habit-tracker-container {
  min-height: 600px;
  border: 2px solid rgba(0, 0, 0, 0.1);
  margin-right: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 1em;
  background-color: var(--container-bg-color);
}

.nav-arrow {
  padding: 0.5em;
  background-color: var(--container-bg-color);
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  filter: brightness(85%);
}

.add-habit-btn {
  display: block;
  margin-left: auto;
  padding: 0.5em;
  background-color: var(--container-bg-color);
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 1em;
  filter: brightness(85%);
  border-radius: 0.45em;
}

.date-navigation {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.date-header {
  display: flex;
  gap: 0.5em;
  flex-grow: 1;
  justify-content: center;
}

.habit-grid {
  display: grid;
  grid-template-columns: 2fr repeat(5, 1fr);
  align-items: center;
  gap: 0em; /* no gaps between the cells to avoid cursor flickering */
}

.date-header,
.habit-row {
  display: contents;
}




.date-cell, .habit-cell {
  text-align: center;
  padding: 1em; 
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 73px; 
  font-weight: bold;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  margin: -5px; /* cells overlap so default cursor never shows (no flickering between cursors) */
}

.date-cell {
  cursor: default; 
}

.habit-cell {
  cursor: url('../assets/watering_can_1.png') 20 45, auto; 
  border: 1px solid var(--container-bg-color); /* need this otherwise cursor flickers */
}

.habit-cell:hover {
  cursor: url('../assets/watering_can_1.png') 20 45, auto; 
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
  cursor: default; 
  display: flex;
  align-items: center;
}

.habit-name:hover {
  border-color: #faa404;
}

.habit-cell .habit-button {
  background-color: transparent;
  border: none;
  cursor: inherit; 
  font-size: 1.5em;
}

.form-title {
  text-align: center;
  margin-top: 0; 
  margin-bottom: 1rem; 
}

.invisible {
  visibility: hidden; 
}

.empty-habit-list {
  text-align: center;
  margin-top: 10em;
  color: var(--container-bg-color);
  filter: brightness(0.5);
}

.empty-habit-content h3 {
  margin-bottom: 0.5em; 
}

.empty-habit-content p {
  font-style: italic;
}

.habit-cell i {
  color: #4CAF50;
  -webkit-text-stroke: 1px rgb(0, 0, 0);
}

.habit-cell i.fa-seedling {
  color: #96a75c;
  -webkit-text-stroke: 1px rgb(0, 0, 0);
}

.icon-dead-tree {
  width: 30px; 
  height: auto;
  position: relative;
  top: -4px;
  filter: drop-shadow(1px 1px 0 rgb(0, 0, 0));
}

select {
  width: 100%;
  padding: 8px 12px;
  margin-top: 5px;
  margin-bottom: 15px;
  background-color: white;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 16px;
  color: #495057;
  appearance: none; 
  -webkit-appearance: none; 
  -moz-appearance: none; 
}

/* Dropdown - Downwards arrow indicator */
select {
  background-image: url('data:image/svg+xml;utf8,<svg fill="black" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"/></svg>');
  background-repeat: no-repeat;
  background-position: right 8px top 50%;
  background-size: 16px;
}

option {
  padding: 10px;
}

select:hover,
select:focus {
  border-color: #80bdff;
  outline: none; 
}

.placeholder-adjustment {
  width: 9px;
}

.categories-section {
  border: 1px solid #ced4da;
  padding: 8px;
  border-radius: 4px;
  margin: 10px 0 20px;
  background-color: #FFFFFF;
}

.category-item {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.category-label {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  margin-top: -15px;
  line-height: 1.5;
  width: calc(1000%);
}
</style>