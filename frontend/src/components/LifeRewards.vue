<template>
  <div class="life-rewards-container">
    <h2>Rewards</h2>
    <button class="add-reward-btn" @click="openModalForNewReward">Add Reward</button>

    <!-- Rewards list -->
    <div class="rewards-list">
      <ul>
        <li v-for="reward in rewards" :key="reward.id" class="reward-item" @click="openModalForReward(reward)">
          <div class="reward-title">{{ reward.name }}</div>
          <div class="reward-cost" @click.stop="spendReward(reward)">
            <i class="fas fa-heart pixelated-heart"></i>
            <div class="cost-amount">{{ formatCost(reward.cost) }}</div>
          </div>
        </li>
      </ul>
    </div>

    <!-- Empty rewards list text -->
    <div v-if="!rewards.length" class="empty-rewards-list">
      <div class="empty-rewards-content">
        <h3 class="emptyTitle">You have no Rewards</h3>
        <p>Spend your Habit Points on real-life treats. E.g. "Watch a TV show episode" or "Enjoy a coffee break".</p>
      </div>
    </div>

    <!-- Modal for adding or editing reward details -->
    <div v-if="showModal" class="modal-backdrop">
      <div class="modal-content">
        <h2 class="form-title">{{ selectedReward ? 'Edit Reward' : 'Add Reward' }}</h2>
        <form @submit.prevent="addOrUpdateReward">
          <label for="rewardName">Title*</label>
          <input id="rewardName" v-model="rewardForm.name" placeholder="Add a title" required>

          <label for="rewardNotes">Notes</label>
          <textarea id="rewardNotes" v-model="rewardForm.notes" placeholder="Add notes"></textarea>

          <label for="rewardCost">Life Points*</label>
          <input id="rewardCost" type="number" v-model.number="rewardForm.cost" placeholder="0" min="0" required>

          <div class="modal-footer">
            <button type="button" @click="closeModal()">Cancel</button>
            <button type="submit">{{ selectedReward ? 'Update' : 'Add' }} Reward</button>
            <!-- Only show the delete button when editing an existing reward -->
            <button v-if="selectedReward" type="button" class="delete-reward-btn" @click="showDeleteConfirmation(selectedReward.id)">Delete</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Confirmation Modal for Deleting Reward -->
    <div v-if="showDeleteConfirm" class="modal-backdrop">
      <div class="modal-content">
        <h2 class="form-title">Are you sure you want to delete this reward? This action cannot be undone.</h2>
        <div class="modal-footer">
          <button type="button" @click="cancelDelete">Cancel</button>
          <button type="button" @click="confirmDelete">Delete</button>
        </div>
      </div>
    </div>


  </div>
</template>

<script>
import { useRewardsStore } from '@/stores/useRewardsStore';
import { useNotificationStore } from '@/stores/useNotificationStore';

export default {
  name: 'LifeRewards',
  data() {
    return {
      showModal: false,
      showDeleteConfirm: false,
      rewardForm: {
        id: null,
        name: '',
        notes: '',
        cost: 0,
      },
      selectedReward: null,
      rewardToDelete: null,
    };
  },
  computed: {
    rewards() {
      const rewardsStore = useRewardsStore();
      return rewardsStore.rewards.map(reward => ({
        ...reward,
        cost: parseFloat(reward.cost),
      }));
    },
  },
  methods: {
    resetForm() {
      this.rewardForm = { id: null, name: '', notes: '', cost: 0 };
      this.selectedReward = null;
    },
    async addOrUpdateReward() {
      const rewardsStore = useRewardsStore();
      await rewardsStore.fetchCSRFToken();

      if (this.selectedReward) {
        await rewardsStore.updateReward(this.rewardForm);
      } else {
        await rewardsStore.addReward(this.rewardForm);
      }

      this.closeModal();
    },
    openModalForNewReward() {
      this.resetForm();
      this.showModal = true;
      this.selectedReward = null;
    },
    openModalForReward(reward) {
      this.selectedReward = reward;
      this.rewardForm = { ...reward };
      this.showModal = true;
    },
    showDeleteConfirmation(rewardId) {
      this.rewardToDelete = rewardId;
      this.showDeleteConfirm = true;
    },
    async confirmDelete() {
      const rewardsStore = useRewardsStore();
      if (this.rewardToDelete) {
        await rewardsStore.deleteReward(this.rewardToDelete);
        this.showDeleteConfirm = false;
        this.rewardToDelete = null;
      }
      this.closeModal();
    },
    cancelDelete() {
      this.showDeleteConfirm = false;
      this.rewardToDelete = null;
    },
    closeModal() {
      this.showModal = false;
      this.showDeleteConfirm = false;
      this.resetForm();
    },
    formatCost(cost) {
      return Number.isInteger(cost) ? cost.toString() : cost.toFixed(2);
    },
    async spendReward(reward) {
      const rewardsStore = useRewardsStore();
      try {
        await rewardsStore.spendReward(reward.id, reward.cost);
        rewardsStore.fetchRewards();
      } catch (error) {
        console.error("Error in spendReward method:", error);
        const notificationStore = useNotificationStore();
        notificationStore.addNotification("An error occurred while trying to spend Life Points.");
      }
    },
    async addOrUpdateReward() {
      const rewardsStore = useRewardsStore();
      await rewardsStore.fetchCSRFToken();

      if (this.selectedReward) {
        try {
          const success = await rewardsStore.updateReward(this.rewardForm);
          if (success) {
            const notificationStore = useNotificationStore();
            notificationStore.addNotification(`Reward updated successfully.`);
          }
        } catch (error) {
          console.error('Error updating reward:', error);
        }
      } else {
        try {
          const success = await rewardsStore.addReward(this.rewardForm);
          if (success) {
            const notificationStore = useNotificationStore();
            notificationStore.addNotification(`Reward added successfully.`);
          }
        } catch (error) {
          console.error('Error adding new reward:', error);
        }
      }

      this.closeModal();
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
  border: 2px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  padding: 1em;
  background-color: var(--container-bg-color);
  position: relative;
}

.form-title {
  text-align: center;
  margin-top: 0;
  margin-bottom: 1rem;
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

.rewards-list {
  margin-top: 1em;
}

.rewards-list ul {
  list-style: none;
  padding: 0;
}

.rewards-list li {
  transition: border-color 0.3s ease;
  cursor: pointer;
  padding: 10px;
  padding-right: 5px;
  border: 2px solid transparent;
  border-radius: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: inherit;
}

.rewards-list li:hover {
  border-color: #faa404;
}

.reward-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.reward-title {
  flex-grow: 1;
  max-width: calc(100% - 120px);
  overflow: hidden;
  text-overflow: ellipsis;
}

.reward-cost {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  width: 100px;
}

.pixelated-heart {
  font-size: 24px;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}
.cost-amount {
  margin-top: 4px;
  text-align: center;
  max-width: 100%;
  overflow: hidden;
}

.add-reward-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0.5em;
  background-color: var(--container-bg-color); 
  color: white;
  border: none;
  cursor: pointer;
  z-index: 2;
  filter: brightness(85%);
  border-radius: 0.45em;
}

.modal-footer button {
  padding: 0.5em;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

.modal-footer .delete-reward-btn {
  padding: 0.5em;
  background-color: #f44336; 
  color: white;
  border: none;
  cursor: pointer;
}

.empty-rewards-list {
  text-align: center;
  margin-top: 10em; 
  color: var(--container-bg-color);
  filter: brightness(0.5);
}

.empty-rewards-content h3 {
  margin-bottom: 0.5em; 
}

.empty-rewards-content p {
  font-style: italic; 
}


</style>