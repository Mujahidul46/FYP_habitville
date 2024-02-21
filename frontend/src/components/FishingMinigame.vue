<template>
  <div id="fishing-minigame-container"></div>
</template>

<script>
import Phaser from 'phaser';

export default {
  data() {
    return {
      game: null,
      fisherman: null,
    };
  },
  mounted() {
    var config = {
      type: Phaser.AUTO,
      parent: 'fishing-minigame-container',
      width: 1920,
      height: 976,
      pixelArt: true,
      physics: {
        default: 'arcade',
        arcade: {
          gravity: { y: 0 },
          debug: false
        }
      },
      scene: {
        preload: preload,
        create: create,
        update: update
      }
    };

    this.game = new Phaser.Game(config);

    function preload() {
      this.load.image('tiles', '/spritesheets/roguelikeSheet_transparent.png');
      this.load.image('waterTiles', '/spritesheets/WaterSpritesheet.png');
      this.load.tilemapTiledJSON('map', '/map/FishingMinigameIslandMap.json');

      // Load the fisherman sprite
      this.load.spritesheet('fisherman', '/fishing_minigame_assets/1 Fisherman/Fisherman_walk.png', {
        frameWidth: 48,
        frameHeight: 48,
      });

      // Load the fisherman idle sprite
      this.load.spritesheet('fisherman_idle', '/fishing_minigame_assets/1 Fisherman/Fisherman_idle.png', {
        frameWidth: 48,
        frameHeight: 48,
      });
    }

    function create() {
      this.cursors = this.input.keyboard.createCursorKeys();

      this.WASDKeys = this.input.keyboard.addKeys({
        up: Phaser.Input.Keyboard.KeyCodes.W,
        down: Phaser.Input.Keyboard.KeyCodes.S,
        left: Phaser.Input.Keyboard.KeyCodes.A,
        right: Phaser.Input.Keyboard.KeyCodes.D,
      });
      const map = this.make.tilemap({ key: 'map' });
      const tileset = map.addTilesetImage('roguelikeSheet_transparent', 'tiles');
      const waterTileset = map.addTilesetImage('WaterSpritesheet', 'waterTiles');

      // Create map layers
      const grassLayer = map.createLayer('grass', tileset, 0, 0);
      const waterLayer = map.createLayer('water', waterTileset, 0, 0);
      const treesLayer = map.createLayer('trees', tileset, 0, 0);



      // Collision for water tiles and fisherman
      waterLayer.setCollisionByProperty({ isWater: true });

      // Adds the fisherman sprite to the game
      this.fisherman = this.physics.add.sprite(100, 100, 'fisherman', 0);

      this.fisherman.body.setSize(30, 35, false);
      this.fisherman.body.setOffset(0, 13);
      
      // Set the world bounds to match the size of this map
      this.physics.world.bounds.width = map.widthInPixels;
      this.physics.world.bounds.height = map.heightInPixels;

      // Enable physics for the fisherman
      this.physics.add.existing(this.fisherman);
      this.fisherman.body.setCollideWorldBounds(true); // Prevents fisherman from going out of the map

      // Add collision between the fisherman and the waterLayer
      this.physics.add.collider(this.fisherman, waterLayer);

      // Camera that follows the fisherman
      this.cameras.main.startFollow(this.fisherman, true, 0.5, 0.5);
      this.cameras.main.setZoom(3); // Adjust the zoom level as needed

      this.cameras.main.setBounds(0, 0, map.widthInPixels, map.heightInPixels);

      // Walking animation
      this.anims.create({
        key: 'walking',
        frames: this.anims.generateFrameNumbers('fisherman', { start: 0, end: 5 }),
        frameRate: 10,
        repeat: -1
      });

      // Idle animation
      this.anims.create({
        key: 'idle',
        frames: this.anims.generateFrameNumbers('fisherman_idle', { start: 0, end: 3 }),
        frameRate: 5,
        repeat: -1
      });
    }

    function update() {
      let velocityX = 0;
      let velocityY = 0;
      const speed = 130;

      if (this.cursors.left.isDown || this.WASDKeys.left.isDown) {
        velocityX -= speed;
        this.fisherman.flipX = true; // Flip the sprite to face left when walking left
        this.fisherman.body.setOffset(18, 13);
      } else if (this.cursors.right.isDown || this.WASDKeys.right.isDown) {
        velocityX += speed;
        this.fisherman.flipX = false;
        this.fisherman.body.setOffset(0, 13);
      }

      if (this.cursors.up.isDown || this.WASDKeys.up.isDown) {
        velocityY -= speed;
      } else if (this.cursors.down.isDown || this.WASDKeys.down.isDown) {
        velocityY += speed;
      }

      // Normalize the velocity vector if moving diagonally (so speed is correct)
      if (velocityX !== 0 && velocityY !== 0) {
        velocityX *= Math.SQRT1_2;
        velocityY *= Math.SQRT1_2;
      }

      this.fisherman.setVelocity(velocityX, velocityY);

      if (velocityX !== 0 || velocityY !== 0) {
        this.fisherman.anims.play('walking', true);
      } else {
        // Plays idle animation when the fisherman is not moving
        this.fisherman.anims.play('idle', true);
      }
    }
  },
  beforeUnmount() {
    console.log("Destroying Phaser game");
    if (this.game) {
      this.game.destroy(true);
    }
  },

};
</script>

<style>
#fishing-minigame-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
