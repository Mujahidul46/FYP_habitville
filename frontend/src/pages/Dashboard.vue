<template>
  <div class="dashboard-container">
    <DailyHabits />
    <ToDoList />
  </div>
</template>


<script>
import { onMounted } from 'vue';
import { useToDoStore } from '@/stores/useToDoStore';
import { useHabitsStore } from '@/stores/useHabitsStore';
import ToDoList from '@/components/ToDoList.vue';
import DailyHabits from '@/components/DailyHabits.vue';

export default {
  name: 'Dashboard',
  components: {
    ToDoList,
    DailyHabits
  },
  setup() {
    const todoStore = useToDoStore();
    const habitsStore = useHabitsStore();

    onMounted(() => {
      todoStore.fetchCSRFToken();
      todoStore.fetchToDos();
      habitsStore.fetchHabits(); 
    });

    return {
      todoStore,
      habitsStore,
    };
  },
};
</script>

<style>
.dashboard-container {
  display: flex; 
  justify-content: center; 
  align-items: flex-start; 
  gap: 2em; 
}

@media (max-width: 768px) {
  .dashboard-container {
    flex-direction: column; 
  }
}
</style>
