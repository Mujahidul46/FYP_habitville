import { defineStore } from 'pinia';

export const useStatisticsStore = defineStore('statistics', {
  state: () => ({
    categoryProgress: [],
    statusMessage: ''
  }),
  actions: {
    async fetchCategoryProgress() {
      this.statusMessage = '';
      try {
        const response = await fetch("http://localhost:8000/category-progress/", {
          method: "GET",
          credentials: "include",
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          this.categoryProgress = await response.json();
          console.log("Fetched category progress data:", this.categoryProgress);
        } else {
          console.error("Failed to fetch category progress data:", response.status, response.statusText);
          this.statusMessage = `Failed to fetch category progress data: ${response.statusText}`;
        }
      } catch (error) {
        console.error("Error during fetch:", error);
        this.statusMessage = "An error occurred while fetching the category progress data.";
      }
    }
  }
});
