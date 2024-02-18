<template>
  <div id="game-container">
    <div v-if="!gameReady" class="loading-message">Loading...</div>
  </div>
</template>

<script>
import Phaser from 'phaser';

export default {
  data() {
    return {
      game: null,
      gameReady: false,
    };
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
          },
          create() {
            const map = this.make.tilemap({ key: 'simple-map' });
            const groundTiles = map.addTilesetImage('Ground_tileset', 'ground');
            const objectsTileset = map.addTilesetImage('objects_tileset', 'objects');
            const buildingsTileset = map.addTilesetImage('premade_buildings_tileset', 'buildings');

            map.createLayer('PlainGrass', groundTiles, 0, 0);
            map.createLayer('Flowers', groundTiles, 0, 0);
            map.createLayer('Road', groundTiles, 0, 0);
            map.createLayer('SquareRocks', groundTiles, 0, 0);
            map.createLayer('Trees', objectsTileset, 0, 0);
            map.createLayer('Lamppost', objectsTileset, 0, 0);
            map.createLayer('Bench', objectsTileset, 0, 0);
            map.createLayer('House', buildingsTileset, 0, 0);
            
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
</style>
