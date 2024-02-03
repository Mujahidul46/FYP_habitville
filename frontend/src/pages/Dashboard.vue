<template>
  <div class="habit-tracker">
    <ToDoList />
  </div>
</template>

<script>
import { onMounted } from 'vue';
import { useToDoStore } from '@/stores/useToDoStore';
import ToDoList from '@/components/ToDoList.vue'; 

export default {
  name: 'Dashboard',
  components: {
    ToDoList,
  },
  setup() {
    const todoStore = useToDoStore();

    onMounted(() => {
      todoStore.fetchCSRFToken();
      todoStore.fetchToDos();
    });

    return {
      todoStore,
    };
  },
};
</script>
