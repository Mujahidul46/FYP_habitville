<template>
  <div class="dashboard-container">
    <DailyHabits class="habits" />
    <ToDoList class="todos" />
    <LifeRewards class="rewards" /> 
  </div>
</template>


<script>
import { onMounted } from 'vue';
import { useToDoStore } from '@/stores/useToDoStore';
import { useHabitsStore } from '@/stores/useHabitsStore';
import { useRewardsStore } from '@/stores/useRewardsStore'; 
import ToDoList from '@/components/ToDoList.vue';
import DailyHabits from '@/components/DailyHabits.vue';
import LifeRewards from '@/components/LifeRewards.vue'; 

export default {
  name: 'Dashboard',
  components: {
    ToDoList,
    DailyHabits,
    LifeRewards,
  },
  setup() {
    const todoStore = useToDoStore();
    const habitsStore = useHabitsStore();
    const rewardsStore = useRewardsStore();

    onMounted(() => {
      todoStore.fetchCSRFToken();
      todoStore.fetchToDos();
      habitsStore.fetchHabits();
      rewardsStore.fetchRewards();
    });

    return {
      todoStore,
      habitsStore,
      rewardsStore,
    };
  },
};
</script>

<style>
.dashboard-container {
  display: flex; 
  justify-content: space-between; 
  align-items: flex-start; 
  gap: 2em;
  height: 100%;
  width: 100%;
  padding: 0 1em;
}

.dashboard-container > .habits {
  flex-basis: 40%;
}

.dashboard-container > .todos {
  flex-basis: 30%;
}

.dashboard-container > .rewards {
  flex-basis: 30%;
}


@media (max-width: 768px) {
  .dashboard-container {
    flex-direction: column; 
  }
  .dashboard-container > .habits,
  .dashboard-container > .todos,
  .dashboard-container > .rewards {
    flex: none;
    width: 100%;
  }
}
</style>
