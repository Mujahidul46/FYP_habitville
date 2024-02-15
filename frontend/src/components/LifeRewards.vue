<template>
    <div class="life-rewards-container">
      <h2>Life Rewards</h2>
      <form @submit.prevent="addReward">
        <div class="form-group">
          <label for="rewardName">Reward Name</label>
          <input type="text" id="rewardName" v-model="newReward.name" required>
        </div>
        <div class="form-group">
          <label for="rewardNotes">Notes (Optional)</label>
          <textarea id="rewardNotes" v-model="newReward.notes"></textarea>
        </div>
        <div class="form-group">
          <label for="rewardCost">Cost (Life Points)</label>
          <input type="number" id="rewardCost" v-model.number="newReward.cost" required min="1">
        </div>
        <button type="submit">Add Reward</button>
      </form>
      
      <div class="rewards-list">
        <h3>Your Rewards</h3>
        <ul>
          <li v-for="reward in rewards" :key="reward.id">
            {{ reward.name }} - {{ reward.cost }} LP
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import { useRewardsStore } from '@/stores/useRewardsStore';
  
  export default {
    name: 'LifeRewards',
    data() {
      return {
        newReward: {
          name: '',
          notes: '',
          cost: 0,
        },
      };
    },
    computed: {
      rewards() {
        return useRewardsStore().rewards;
      }
    },
    methods: {
      async addReward() {
        const rewardsStore = useRewardsStore();
        await rewardsStore.fetchCSRFToken();
        await rewardsStore.addReward(this.newReward);

        this.newReward = { name: '', notes: '', cost: 0 };
      },
    },
    mounted() {
      const rewardsStore = useRewardsStore();
      rewardsStore.fetchRewards();
    },
  };
  </script>
  
  <style scoped>
  .life-rewards-container {
    min-height: 600px;
    border: 2px solid #4CAF50;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    padding: 1em;
    background-color: #bcdbba;
    position: relative;
  }
  
  .form-group {
    margin-bottom: 1em;
  }
  
  .form-group label {
    display: block;
  }
  
  .life-rewards-container input,
  .life-rewards-container textarea {
    margin-bottom: 0.5em;
    padding: 0.5em;
    border: 1px solid #ccc;
    width: 100%;
  }
  
  .life-rewards-container button {
    padding: 0.5em;
    background-color: #4CAF50;
    color: white;
    border: none;
  }
  
  .rewards-list {
    margin-top: 1em;
  }
  
  .rewards-list ul {
    list-style: none;
    padding: 0;
  }
  
  .rewards-list li {
    margin-bottom: 1em;
    padding: 1em;
    border-radius: 5px;
    background: #f0f0f0;
    overflow: hidden;
  }
  
  .rewards-list h3,
  .rewards-list p {
    word-wrap: break-word;
    overflow-wrap: break-word;
    margin: 0;
  }
  
  </style>
  