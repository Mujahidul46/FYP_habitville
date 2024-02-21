<template>
  <div id="game-container">
    <div v-if="!gameReady" class="loading-message">Loading...</div>
    <button v-if="gameReady" @click="playMinigame" class="play-minigame-button">Play "Lucky Catch" Minigame</button>
  </div>
</template>

<script>
import Phaser from 'phaser';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      game: null,
      gameReady: false,
    };
  },
  setup() {
    const router = useRouter();

    // Go to the FishingMinigame route
    const playMinigame = () => {
      router.push({ name: 'FishingMinigame' });
    };

    return { playMinigame };
  },
  mounted() {
    this.initPhaserGame();
  },
  methods: {
    initPhaserGame() {
      const vm = this;

      const config = {
        type: Phaser.AUTO,
        parent: 'game-container',
        width: 1920,
        height: 976,
        physics: {
          default: 'arcade',
          arcade: {
            gravity: { y: 0 },
            debug: false,
          },
        },
        scene: {
          preload() {
            this.load.tilemapTiledJSON('simple-map', 'map/SimpleMap.json');
            this.load.image('ground', 'spritesheets/ground_spritesheet.png');
            this.load.image('objects', 'spritesheets/objects_spritesheet.png');
            this.load.image('buildings', 'spritesheets/premade_buildings_spritesheet.png');
            this.load.image('lake', 'spritesheets/roguelikeSheet_transparent.png');
          },
          create() {
            const map = this.make.tilemap({ key: 'simple-map' });
            const groundTiles = map.addTilesetImage('Ground_tileset', 'ground');
            const objectsTileset = map.addTilesetImage('objects_tileset', 'objects');
            const buildingsTileset = map.addTilesetImage('premade_buildings_tileset', 'buildings');
            const lakeTileset = map.addTilesetImage('roguelikeSheet_transparent', 'lake');

            map.createLayer('PlainGrass', groundTiles, 0, 0);
            map.createLayer('Flowers', groundTiles, 0, 0);
            map.createLayer('Road', groundTiles, 0, 0);
            map.createLayer('SquareRocks', groundTiles, 0, 0);
            map.createLayer('Trees', objectsTileset, 0, 0);
            map.createLayer('Lamppost', objectsTileset, 0, 0);
            map.createLayer('Bench', objectsTileset, 0, 0);
            map.createLayer('House', buildingsTileset, 0, 0);
            map.createLayer('Lake', lakeTileset, 0, 0);

            this.cameras.main.setBounds(0, 0, map.widthInPixels, map.heightInPixels);
            this.cameras.main.setZoom(1);
            this.cameras.main.centerOn(map.widthInPixels / 2, map.heightInPixels / 2);

            vm.gameReady = true;
          },
        },
      };

      this.game = new Phaser.Game(config);
    },
  },
};
</script>

<style scoped>
#game-container {
  width: 100%;
  max-width: 1920px;
  max-height: 100vh;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.loading-message {
  position: absolute;
  color: #fff;
  font-size: 2em;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

canvas {
  max-width: 100%;
  max-height: 100vh;
  object-fit: contain;
}


.play-minigame-button {
    position: absolute;
    top: calc(50% + 40px);
    left: calc(50% + 460px);
    transform: translate(-50%, -50%);
    z-index: 10;

    padding: 10px 20px;
    background: #4CAF50;
    background: -webkit-linear-gradient(to right, #66BB6A, #43A047);
    background: linear-gradient(to right, #66BB6A, #43A047);
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

    transition: background 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
  }

  .play-minigame-button:hover, .play-minigame-button:focus {
    background: linear-gradient(to right, #43A047, #66BB6A);
    transform: translate(-50%, -50%) scale(1.05);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
  }
</style>
