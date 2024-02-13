import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    notifications: [],
    maxNotifications: 3, // Maximum number of notifications to show at once
  }),
  actions: {
    addNotification(message) {
      const newNotification = {
        id: Date.now(),
        message: message,
        show: true,
      };

      this.notifications.push(newNotification);

      setTimeout(() => {
        this.removeNotification(newNotification.id); // keeps notifcation list from overflowing
      }, 3000); // Each notification stays for 3 seconds

      // Limit the number of notifications shown at once
      if (this.notifications.length > this.maxNotifications) {
        this.notifications = this.notifications.slice(-this.maxNotifications); // Keep only the last 3 items
      }
    },

    removeNotification(notificationId) { // removes notification using notifcationId
      this.notifications = this.notifications.filter(notification => notification.id !== notificationId);
    },
  },
});
