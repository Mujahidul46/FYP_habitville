<template>
    <transition name="slide-fade">
      <div class="notification" v-if="show">
        {{ message }}
      </div>
    </transition>
  </template>
  
  <script>
  export default {
    props: {
      message: String,
      show: Boolean
    }
  }
  </script>
  
  <style scoped>
  @keyframes slideIn {
    0% {
      transform: translateX(100%);
      opacity: 0;
    }
    100% {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes fadeOut {
    0% {
      opacity: 1;
    }
    100% {
      opacity: 0;
    }
  }
  
  .slide-fade-enter-active {
    animation: slideIn 0.5s ease-out forwards;
  }
  .slide-fade-leave-active {
    animation: fadeOut 0.5s ease-out forwards;
  }
  
  .notification {
  position: fixed;
  top: var(--notification-top, 70px);
  right: 20px; 
  background-color: #e7ce42; 
  color: #000000; 
  padding: 10px 20px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 1050;
}
  </style>
  