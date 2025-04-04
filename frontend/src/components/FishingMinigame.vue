<template>
  <div id="fishing-minigame-container">
    <div id="timer-container">{{ timerDisplay }}</div>
  </div>
  <div id="fullscreen-toggle-container">
    <button @click="toggleFullscreen">
      <i class="fas fa-expand-arrows-alt"></i> Fullscreen
    </button>
    <div class="button-spacing"></div>
    <button @click="goBackToVillage">
      Go Back to Village
    </button>
  </div>
</template>

<script>
import Phaser from 'phaser';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      game: null,
      backgroundMusic: null,
      fisherman: null,
      lineGraphics: null,
      isFishing: false,
      tooFarWarningText: null,
      currentFishingSpot: null,
      currentExclamation: null,
      timingBarMovingUp: true,
      barYPosition: window.innerHeight / 2,
      successMessageText: null,
      failMessageText: null,
      timer: 300, // 5 mins
      timerInterval: null, // ref to timer interval id
      timerDisplay: '',
    };
  },
  setup() {
    const router = useRouter();
    return {};
  },
  mounted() {
    // Start the timer
    this.timerInterval = setInterval(() => {
      if (this.timer > 0) {
        this.timer--;
        this.timerDisplay = this.formatTimerDisplay(this.timer);
      } else {
        this.stopTimer();
        this.goBackToVillage(); // return to village route
      }
    }, 1000);
    
    this.backgroundMusic = new Audio('/music/Sakura-Girl-Peach-chosic.com_.mp3');
    this.backgroundMusic.loop = true;
    this.backgroundMusic.play();

    var config = {
      type: Phaser.AUTO,
      parent: 'fishing-minigame-container',
      width: window.innerWidth,
      height: window.innerHeight,
      pixelArt: true,
      physics: {
        default: 'arcade',
        arcade: {
          gravity: { y: 0 },
          debug: false
        }
      },
      scale: {
      mode: Phaser.Scale.RESIZE,
      parent: 'fishing-minigame-container',
      autoCenter: Phaser.Scale.CENTER_BOTH,
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

      // Load the fisherman fishing animation spritesheet
      this.load.spritesheet('fisherman_fishing', '/fishing_minigame_assets/1 Fisherman/Fisherman_fish_no_line.png', {
          frameWidth: 48,
          frameHeight: 48,
      });

      // Load the fishing spot inactive image (fish has not bit)
      this.load.image('fishingSpotInactive', '/fishing_minigame_assets/3 Objects/fishing_spot_inactive.png');

      // Load the fishing spot active image (fish HAS bit)
      this.load.image('fishingSpotActive', '/fishing_minigame_assets/3 Objects/fishing_spot_active.png');
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
      this.cameras.main.setZoom(4); // Adjust the zoom level as needed (1=full map, change back to 3 if anything breaks)

      this.cameras.main.setBounds(0, 0, map.widthInPixels, map.heightInPixels);

      // Walking animation
      this.anims.create({ key: 'walking', frames: this.anims.generateFrameNumbers('fisherman', { start: 0, end: 5 }), frameRate: 10, repeat: -1 });

      // Idle animation
      this.anims.create({ key: 'idle', frames: this.anims.generateFrameNumbers('fisherman_idle', { start: 0, end: 3 }), frameRate: 2, repeat: -1 });

      // Fishing animation
      this.anims.create({
          key: 'fishing',
          frames: this.anims.generateFrameNumbers('fisherman_fishing', { start: 0, end: 3 }),
          frameRate: 2,
          repeat: -1
      });

      // Fishing line
      this.lineGraphics = this.add.graphics({ lineStyle: { width: 2, color: 0x0000ff } });

      // Initialize tooFarWarningText
      this.tooFarWarningText = this.add.text(0, 0, "I'm too far away from that spot!", {
        fontFamily: 'Arial',
        fontSize: '30px',
        fill: '#ffffff',
        align: 'center',
      }).setOrigin(0.5, 1).setVisible(false);

      // Initialize successMessageText
      this.successMessageText = this.add.text(0, 0, "You caught a fish!", {
        fontFamily: 'Arial',
        fontSize: '30px',
        fill: '#ff0',
        align: 'center',
      }).setOrigin(0.5, 1).setVisible(false);

      const successMessages = [
        "With reflexes like these, I'm certain I was a cat in my past life...",
        "Wow! A beautiful rainbow trout!",
        "Yes! It's a hefty bass!",
        "Wow! A rare golden carp!",
        "Amazing catch! That's a big one!",
        "I've got skill, that's a fine salmon!",
        "Incredible! I caught a mythical koi!",
        "What a catch! A swift and sleek pike!",
        "I've got a giant catfish!",
        "Spectacular! A vibrant and colorful parrotfish!",
        "I did it! That's a rare and elusive sturgeon!",
        "Just a regular old perch, but every catch counts!",
        "Ah, a common carp. It's no trophy, but fishing is fishing.",
        "A small trout. Not the biggest fish in the sea, but it's a start.",
        "Managed to snag a little bream. It's all about patience.",
        "A modest-sized bass. That was fun to catch!",
        "Caught a tiny catfish. It's cute, in a slimy, whiskered way.",
        "An average-sized pike. Not the monster of the lake, but it put up a good fight.",
        "A little sunfish. It's no giant, but it sure is sunny."
      ];

      // Initialize failMessageText
      this.failMessageText = this.add.text(0, 0, "The fish got away!", {
        fontFamily: 'Arial',
        fontSize: '30px',
        fill: '#f00',
        align: 'center',
      }).setOrigin(0.5, 1).setVisible(false);


      // Fishing spots
      const originalSpotLocations = map.getObjectLayer('fishingSpots').objects.slice();

      const fishingSpotLocations = Phaser.Utils.Array.Shuffle(originalSpotLocations.slice()); // Clone and shuffle spots
      this.fishingSpotsActive = [];

      const addSpot = () => {
        if (this.fishingSpotsActive.length < 10) {
          if (fishingSpotLocations.length === 0) {
            // Refill and shuffle the locations from the original spots
            fishingSpotLocations.push(...Phaser.Utils.Array.Shuffle(originalSpotLocations.slice()));
          }
          const spotLocation = fishingSpotLocations.pop(); // Get and remove a location from the array
          const spot = this.physics.add.sprite(spotLocation.x, spotLocation.y, 'fishingSpotInactive').setInteractive();

          let biteTimer;

          spot.on('pointerdown', () => {
            if (this.isFishing) {
              console.log("Minigame is active. Ignoring additional clicks on spots.");
              return; // Early exit if a minigame is already active
            }
            console.log("Fishing spot clicked.");

            // cant fish two spots in one go
            if (this.currentFishingSpot && this.currentFishingSpot !== spot) {
              this.resetFishingInteraction();
            }

            // Get distance between the fisherman and the fishing spot
            const distance = Phaser.Math.Distance.Between(this.fisherman.x, this.fisherman.y, spot.x, spot.y);

            const maxCastingDistance = 200;

            // Checks if fisherman is too far from the fishing spot
            if (distance > maxCastingDistance) {
              const messages = [
                "Oops, a bit too far for me.",
                "Need to close in on the spot.",
                "Distance is too great for a good cast.",
                "No way I'm reaching that from here.",
                "Not within casting range!",
                "I should try stepping forward.",
                "A few steps closer and I can cast.",
                "Even with a super stretchy arm, I couldn't reach that!",
                "My fishing line isn't made of rubber bands, you know.",
                "Is this what they meant by 'long-distance relationship'?",
                "I'd need a fishing drone to reach that spot.",
                "Trying to cast that far is a bigger fantasy than my fishing skills."
            ];

                const randomMessage = Phaser.Utils.Array.GetRandom(messages);

                if (this.warningText) {
                    this.warningText.destroy(); // Destroy existing message if exists
                }

                this.tooFarWarningText.setText(randomMessage);

                this.tooFarWarningText.setPosition(this.cameras.main.scrollX + this.cameras.main.width / 2, this.cameras.main.scrollY + 50);
                this.tooFarWarningText.setDepth(100);
                console.log("Attempting to show text message");
                this.tooFarWarningText.setVisible(true);

                // Hide the text after 3 seconds
                this.time.delayedCall(3000, () => {
                    this.tooFarWarningText.setVisible(false);
                });

                return;
            }

            console.log("Starting fishing. Waiting for fish to bite...");
            this.isFishing = true;
            this.disableAllFishingSpots();
            this.currentFishingSpot = spot;
            spot.setTexture('fishingSpotInactive');

            startBiteTimer(spot);

            // Get direction to face based on the fishing spot's location
            if (spot.x > this.fisherman.x) {
              // face right
              this.fisherman.flipX = false;
            } else {
              // face left
              this.fisherman.flipX = true;
            }
            this.lineGraphics.clear();

            // Calculate the offset based on the fisherman's facing direction
            let offsetX = this.fisherman.flipX ? -19 : 19;
            let offsetY = 2;

            this.lineGraphics.lineStyle(2, 0x0000ff, 1);
            this.lineGraphics.beginPath();
            this.lineGraphics.moveTo(this.fisherman.x + offsetX, this.fisherman.y + offsetY);
            this.lineGraphics.lineTo(spot.x, spot.y);
            this.lineGraphics.closePath();
            this.lineGraphics.strokePath();

            this.fisherman.anims.play('fishing');
          });

          // disable interaction on all fishing spots
          this.disableAllFishingSpots = () => {
            this.fishingSpotsActive.forEach(spot => {
                spot.disableInteractive();
            });
          };

          // enable interaction on all fishing spots
          this.enableAllFishingSpots = () => {
              this.fishingSpotsActive.forEach(spot => {
                  spot.setInteractive();
              });
          };
          this.fishingSpotsActive.push(spot);

          // Generate a random delay between 10 and 20 seconds
          const randomDelay = Phaser.Math.Between(10000, 20000);
          this.time.delayedCall(randomDelay, () => {
            if (biteTimer) {
              console.log("Bite timer removed or expired.");
              biteTimer.remove();
            }
            // Check if the spot is currently active
            if (spot.active) {
              // Check if the minigame is not active or if the clicked spot is different from the one currently in use
              if (!this.isFishing || this.currentFishingSpot !== spot) {
                spot.destroy();
                console.log("Fishing spot destroyed due to inactivity or player engagement elsewhere.");
                // Remove the destroyed spot from the active spots list by filtering
                this.fishingSpotsActive = this.fishingSpotsActive.filter(activeSpot => activeSpot !== spot);
              } else {
                console.log("Fishing spot remains active due to ongoing minigame.");
              }
            }
            addSpot.call(this); // Add new spot continuously
          });

        }
      };
      const startBiteTimer = (spot) => {
        const initiateBite = () => {
            if (!spot || !spot.active) {
                console.log("Spot is no longer active or has been destroyed.");
                return; // Early return if the spot is inactive or destroyed
            }
            console.log("Fish is about to bite.");
            spot.setTexture('fishingSpotActive');

            this.currentExclamation = this.add.text(spot.x, spot.y+40, '!', {
                fontFamily: 'Arial',
                fontSize: '64px',
                fill: '#ffffff',
                stroke: '#000000',
                strokeThickness: 6,
            }).setOrigin(0.5, 1).setDepth(101);


            let exclamationTimeout = this.time.delayedCall(2000, () => {
              if (this.currentExclamation) {
                this.currentExclamation.destroy();
                this.currentExclamation = null;
              }
              if (spot.active) {
                  console.log("Missed the bite. Waiting for the next bite.");
                  spot.setTexture('fishingSpotInactive');
                  this.clearMinigameGraphics();
                  spot.disableInteractive();
                  startBiteTimer.call(this, spot); // reset timer to give player another chance
              }
            });

            spot.setInteractive().once('pointerdown', () => {
                if (this.currentExclamation) {
                  this.currentExclamation.destroy();
                  this.currentExclamation = null;
                }  
                exclamationTimeout.remove();
                this.clearMinigameGraphics();
                spot.disableInteractive();
                // start minigame
                startTimingMinigame.call(this);
            });
        };

        this.clearMinigameGraphics = () => {
          if (this.timingBar) {
              this.timingBar.clear();
              this.timingBar.destroy();
              this.timingBar = null;
          }
          if (this.greenStrip) {
              this.greenStrip.clear();
              this.greenStrip.destroy();
              this.greenStrip = null;
          }
          if (this.yellowBar) {
              this.yellowBar.clear();
              this.yellowBar.destroy();
              this.yellowBar = null;
          }
        };


        this.checkMinigameSuccess = () => {
            if (this.randomGreenStripStartY === undefined) {
              console.error("randomGreenStripStartY is not defined yet.");
              return false;
            }
  
            const yellowBarTop = this.yellowBarYPosition;
            const yellowBarBottom = this.yellowBarYPosition + 20;
            const greenStripTop = this.randomGreenStripStartY;
            const greenStripBottom = this.randomGreenStripStartY + 50;
            
            console.log(`Yellow Bar: Top=${yellowBarTop}, Bottom=${yellowBarBottom}`);
            console.log(`Green Strip: Top=${greenStripTop}, Bottom=${greenStripBottom}`);

            //return yellowBarBottom >= greenStripTop && yellowBarTop <= greenStripBottom; // yellow bar doesnt have to be FULLY inside
            return yellowBarTop >= greenStripTop && yellowBarBottom <= greenStripBottom; // yellow bar has to be FULLY inside
          };

          this.input.on('pointerdown', () => {
            if (!this.isFishing || !this.greenStrip || !this.yellowBar) return;

            const success = this.checkMinigameSuccess();
            if (success) {
              console.log("User won the minigame");
              const randomSuccessMessage = Phaser.Utils.Array.GetRandom(successMessages);
              // Display success message
              if (this.successMessageText) {
                this.successMessageText.setText(randomSuccessMessage);
                this.successMessageText.setPosition(this.cameras.main.scrollX + this.cameras.main.width / 2, this.cameras.main.scrollY + 100);
                this.successMessageText.setDepth(101);
                this.successMessageText.setVisible(true);
                this.time.delayedCall(3000, () => {
                    this.successMessageText.setVisible(false);
                });
              }
            } else {
              console.log("User lost minigame");
              // Display fail message
              if (this.failMessageText) {
                  this.failMessageText.setPosition(this.cameras.main.scrollX + this.cameras.main.width / 2, this.cameras.main.scrollY + 100);
                  this.failMessageText.setDepth(101);
                  this.failMessageText.setVisible(true);
                  this.time.delayedCall(3000, () => {
                      this.failMessageText.setVisible(false);
                  });
              }
            }
            this.enableAllFishingSpots();
  
            // Clear the graphics and reset the minigame state
            this.clearMinigameGraphics();
            this.isFishing = false;
            this.lineGraphics.clear();

            // destroy the current fishing spot after the minigame is over
            if (this.currentFishingSpot && this.currentFishingSpot.active) {
              this.currentFishingSpot.destroy();
              console.log("Current fishing spot destroyed after minigame conclusion.");
              // Remove destroyed spot from the active spots list
              this.fishingSpotsActive = this.fishingSpotsActive.filter(activeSpot => activeSpot !== this.currentFishingSpot);
              this.currentFishingSpot = null;
            }
            this.resetFishingInteraction();
          });

        // Reset previous fishing interaction
        this.resetFishingInteraction = () => {
          if (this.currentExclamation) {
            this.currentExclamation.destroy();
            this.currentExclamation = null;
          }
          if (this.currentFishingSpot) {
            this.currentFishingSpot.setTexture('fishingSpotInactive');
            this.currentFishingSpot.disableInteractive();
            if (this.currentFishingSpot.biteTimer) {
              this.currentFishingSpot.biteTimer.remove();
              this.currentFishingSpot.biteTimer = null;
            }
            this.currentFishingSpot = null;
          }
          if (this.lineGraphics) {
            this.lineGraphics.clear();
          }

          this.fishingSpotsActive.forEach(spot => {
            spot.setTexture('fishingSpotInactive'); // reset visually to image with less ripples
            spot.setInteractive(); // Can interact again with spots 
          });
          this.isFishing = false;
        };

        

        const startTimingMinigame = () => {
          const offsetX = 100; // used to move bars slightly to right
          const viewportCenterX = this.cameras.main.worldView.x + this.cameras.main.worldView.width / 2 + offsetX;

          const viewportCenterY = this.cameras.main.worldView.y + this.cameras.main.worldView.height / 2;

          this.barYPosition = viewportCenterY - 100;

          this.timingBar = this.add.graphics({ fillStyle: { color: 0x0000ff } });
          this.timingBar.fillRect(viewportCenterX - 5, this.barYPosition, 10, 200);

          const blueBarStartY = this.barYPosition;
          const blueBarEndY = this.barYPosition + 200;
          const greenStripHeight = 50;
          const maxGreenStripStartY = blueBarEndY - greenStripHeight;

          this.randomGreenStripStartY = Phaser.Math.Between(blueBarStartY, maxGreenStripStartY);

          this.greenStrip = this.add.graphics({ fillStyle: { color: 0x00ff00 } });
          this.greenStrip.fillRect(viewportCenterX - 5, this.randomGreenStripStartY, 10, greenStripHeight);

          // Create the moving yellow bar
          this.yellowBar = this.add.graphics({ fillStyle: { color: 0xffff00 } });
          this.yellowBarYPosition = Phaser.Math.Between(this.barYPosition + 10, maxGreenStripStartY - 30);
          this.yellowBar.fillRect(viewportCenterX - 5, this.yellowBarYPosition, 10, 20);
      };

      this.updateMinigame = () => {
        const speed = 2; // make this randomised later

        if (this.timingBarMovingUp) {
            this.yellowBarYPosition -= speed;
        } else {
            this.yellowBarYPosition += speed;
        }

        if (this.yellowBarYPosition <= this.barYPosition || this.yellowBarYPosition + 20 >= this.barYPosition + 200) {
            this.timingBarMovingUp = !this.timingBarMovingUp;
        }

        const offsetX = 100; // has to be same offset as used in startTimingMinigame
        const viewportCenterX = this.cameras.main.worldView.x + this.cameras.main.worldView.width / 2 + offsetX;

        if (this.yellowBar) {
            this.yellowBar.clear();
            this.yellowBar.fillRect(viewportCenterX - 5, this.yellowBarYPosition, 10, 20);
        }
      };

        // Delay before the fish bites again, 2-8 seconds
        spot.biteTimer = this.time.delayedCall(Phaser.Math.Between(2000, 8000), initiateBite);
      };
      Array.from({ length: 10 }).forEach(addSpot);
    }

    function update() {
      let velocityX = 0;
      let velocityY = 0;
      const speed = 130;

      // Check for user movement input
      if (this.cursors.left.isDown || this.WASDKeys.left.isDown || this.cursors.right.isDown || this.WASDKeys.right.isDown || this.cursors.up.isDown || this.WASDKeys.up.isDown || this.cursors.down.isDown || this.WASDKeys.down.isDown) {
        if(this.isFishing) {
          console.log("Player moved. Resetting fishing state.");
          this.lineGraphics.clear();
          this.isFishing = false; // fishing state is reset
        }

        // Check if there's a current fishing spot with an active timer (i.e. player fishing it)
        if (this.currentFishingSpot && this.currentFishingSpot.biteTimer) {
          console.log("Resetting bite timer due to player movement.");
          if (this.currentFishingSpot.active) {
              this.currentFishingSpot.biteTimer.remove();
              this.currentFishingSpot.setTexture('fishingSpotInactive'); // change the image to one with less ripples
          }
          this.currentFishingSpot.biteTimer = null;
          this.currentFishingSpot = null;
        }
      }

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

      // Update the position of tooFarWarningText based on the fisherman's position
      if (this.tooFarWarningText.visible) {
        // counteract zoom effect so text is not low quality
        const scale = 1 / this.cameras.main.zoom;
        this.tooFarWarningText.setScale(scale);
        

        const textOffsetY = -40;
        this.tooFarWarningText.x = this.fisherman.x;
        this.tooFarWarningText.y = this.fisherman.y + textOffsetY * scale;
      }

      // successfully catch fish test
      if (this.successMessageText.visible) {
        const scale = 1 / this.cameras.main.zoom;
        this.successMessageText.setScale(scale);
        const successTextOffsetY = -50;
        this.successMessageText.x = this.fisherman.x - 5;
        this.successMessageText.y = this.fisherman.y + successTextOffsetY * scale;
      }

      // fail to catch fish text
      if (this.failMessageText.visible) {
          const scale = 1 / this.cameras.main.zoom;
          this.failMessageText.setScale(scale);
          const failTextOffsetY = -50;
          this.failMessageText.x = this.fisherman.x - 5;
          this.failMessageText.y = this.fisherman.y + failTextOffsetY * scale;
      }

      if (this.currentExclamation && this.currentExclamation.visible) {
          const exclamationScale = 1 / this.cameras.main.zoom;
          this.currentExclamation.setScale(exclamationScale);

          if (this.currentFishingSpot) {
              const exclamationOffsetX = 0;
              const exclamationOffsetY = -50;
              this.currentExclamation.x = this.currentFishingSpot.x + exclamationOffsetX * exclamationScale;
              this.currentExclamation.y = this.currentFishingSpot.y + exclamationOffsetY * exclamationScale;
          } else {
              console.log("currentFishingSpot is null, cannot update exclamation mark position.");
              this.currentExclamation.setVisible(false);
          }
        }

      if (!this.isFishing){
        if (velocityX !== 0 || velocityY !== 0) {
          this.fisherman.anims.play('walking', true);
        } else {
          // Plays idle animation when the fisherman is not moving
          this.fisherman.anims.play('idle', true);
        }
      }

      if (this.isFishing) {
          this.updateMinigame();
      }

    }
  },
  methods: {
    toggleFullscreen() {
      const container = document.getElementById('fishing-minigame-container');
      if (!document.fullscreenElement) {
        if (container.requestFullscreen) {
          container.requestFullscreen();
        } else if (container.mozRequestFullScreen) { /* Firefox */
          container.mozRequestFullScreen();
        } else if (container.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
          container.webkitRequestFullscreen();
        } else if (container.msRequestFullscreen) { /* IE/Edge */
          container.msRequestFullscreen();
        }
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.mozCancelFullScreen) { /* Firefox */
          document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
          document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { /* IE/Edge */
          document.msExitFullscreen();
        }
      }
    },
    formatTimerDisplay(seconds) {
      const min = Math.floor(seconds / 60);
      const sec = seconds % 60;
      return `${min}:${sec.toString().padStart(2, '0')}`;
    },
    
    stopTimer() {
      if (this.timerInterval) {
        clearInterval(this.timerInterval);
        this.timerInterval = null;
      }
    },
    goBackToVillage() {
      this.$router.push({ name: 'VillageMap' });
    },
  },
  beforeUnmount() {
    console.log("Destroying Phaser game");
    if (this.game) {
      this.game.destroy(true);
    }
    if (this.backgroundMusic) {
      this.backgroundMusic.pause();
      this.backgroundMusic.currentTime = 0;
    }
    this.stopTimer();
  },

};
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  overflow: hidden;
  width: 100vw;
  height: 100vh;
}

#fishing-minigame-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
}

#fullscreen-toggle-container {
  position: fixed;
  top: 10px;
  right: 10px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

#fullscreen-toggle-container button {
  background-color: #bfbfbf;
  color: #333333;
  border: 2px solid #dfdfdf;
  padding: 8px 16px;
  font-size: 14px;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
  display: flex;
  align-items: center;
  gap: 5px;
}

#fullscreen-toggle-container button:hover {
  background-color: #adacac;
  color: #000000;
}

button i {
  margin-right: 5px;
}

.body {
  overflow: hidden;
  margin: 0;
}

.button-spacing {
  margin-bottom: 10px;
}

#timer-container {
  position: absolute;
  top: 10px;
  left: 10px;
  color: #fff;
  background-color: rgba(14, 150, 188, 0.75);
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 1.15rem;
  z-index: 1001;
}

</style>