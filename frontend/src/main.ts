import { createApp } from 'vue'
import { createPinia } from 'pinia';

import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

// Preload game assets
function preloadAssets() {
  const images = [
    '/spritesheets/ground_spritesheet.png',
    '/spritesheets/objects_spritesheet.png',
  ];

  images.forEach((src) => {
    const img = new Image();
    img.src = src;
  });


  fetch('/map/SimpleMap.json').then((response) => {
    if (!response.ok) {
      console.error('Failed to preload map JSON');
    }
  });
}

preloadAssets();

const app = createApp(App)

app.use(createPinia());
app.use(router)

app.mount('#app')
