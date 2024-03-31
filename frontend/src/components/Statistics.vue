<template>
    <div class="statistics">
      <div v-for="(progress, index) in categoryProgress" :key="index" class="progress-category">
        <h3>{{ progress.category_name }}</h3>
        <div class="progress-bar-container">
          <div
            class="progress-bar"
            :style="{ width: progressPercentage(progress) + '%' }"
          ></div>
        </div>
        <p>Level: {{ progress.level }} | EXP: {{ progress.current_exp }} / {{ progress.exp_to_next_level }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import { useStatisticsStore } from '@/stores/useStatisticsStore';
  import { onMounted, computed } from 'vue';
  
  export default {
    name: 'Statistics',
    setup() {
      const statisticsStore = useStatisticsStore();
  
      onMounted(() => {
        statisticsStore.fetchCategoryProgress();
      });
  
      const categoryProgress = computed(() => statisticsStore.categoryProgress);
  
      // calculates the percentage of the progress bar
      const progressPercentage = (progress) => {
        console.log('EXP: ', progress.current_exp, 'Next Level: ', progress.exp_to_next_level);
        if (progress.exp_to_next_level === 0) {
            return 100; 
        }
        return (progress.current_exp / progress.exp_to_next_level) * 100;
      };

      return {
        categoryProgress,
        progressPercentage,
      };
    },
  };
  </script>
  
<style scoped>
.statistics {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
  gap: 20px;
  padding: 20px;
  justify-content: center;
}

.progress-category {
  background: white;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 15px;
  box-sizing: border-box;
}

.progress-bar-container {
  background-color: #eee;
  border-radius: 4px;
  height: 20px;
  margin-bottom: 10px;
}

.progress-bar {
  background-color: #4caf50;
  height: 100%;
  border-radius: 4px;
}
</style>