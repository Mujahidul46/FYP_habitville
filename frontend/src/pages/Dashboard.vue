<template>
  <div class="dashboard">
    <ToDoList />
    <DailyHabits />
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