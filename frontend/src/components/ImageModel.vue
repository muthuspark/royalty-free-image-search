<template>
    <div class="modal" v-if="image" @click="$emit('close')">
      <div class="modal-content" @click.stop>
        <span class="close-button" @click="$emit('close')">&times;</span>
        <img :src="image.full_size" :alt="'Full size image from ' + image.source">
        <div class="modal-info">
          <h3>Image from {{ image.source }}</h3>
          <p>By: <a :href="image.photographer_url" target="_blank">{{ image.photographer }}</a></p>
          <p>Dimensions: {{ image.width }}×{{ image.height }}</p>
          <div class="modal-actions">
            <a :href="image.full_size" target="_blank" class="button">View Original</a>
            <a :href="image.source_url" target="_blank" class="button">View on {{ image.source }}</a>
            <button @click="copyAttributionText" class="button">Copy Attribution</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ImageModal',
    props: {
      image: {
        type: Object,
        default: null
      }
    },
    methods: {
      copyAttributionText() {
        if (!this.image) return;
        
        const attributionText = `Image by ${this.image.photographer} from ${this.image.source} - ${this.image.source_url}`;
        
        // Copy to clipboard
        navigator.clipboard.writeText(attributionText)
          .then(() => {
            alert('Attribution copied to clipboard!');
          })
          .catch(err => {
            console.error('Failed to copy attribution: ', err);
            alert('Failed to copy attribution text. Please try again.');
          });
      }
    },
    mounted() {
      // Prevent scrolling when modal is open
      document.body.classList.add('modal-open');
    },
    beforeUnmount() {
      // Re-enable scrolling when modal is closed
      document.body.classList.remove('modal-open');
    }
  }
  </script>
  
  <style scoped>
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 20px;
  }
  
  .modal-content {
    background-color: white;
    border-radius: 8px;
    max-width: 90%;
    max-height: 90%;
    overflow: auto;
    position: relative;
    display: flex;
    flex-direction: column;
  }
  
  .close-button {
    position: absolute;
    top: 10px;
    right: 15px;
    font-size: 2rem;
    color: white;
    cursor: pointer;
    text-shadow: 0 0 5px black;
    z-index: 10;
  }
  
  .modal-content img {
    max-width: 100%;
    max-height: 70vh;
    object-fit: contain;
  }
  
  .modal-info {
    padding: 20px;
  }
  
  .modal-info h3 {
    margin-bottom: 10px;
    color: #2c3e50;
  }
  
  .modal-actions {
    margin-top: 15px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  
  .button {
    display: inline-block;
    padding: 8px 15px;
    background-color: #3498db;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-size: 0.9rem;
    transition: background-color 0.3s;
    border: none;
    cursor: pointer;
  }
  
  .button:hover {
    background-color: #2980b9;
  }
  
  @media (max-width: 768px) {
    .modal-content {
      width: 95%;
    }
    
    .modal-actions {
      flex-direction: column;
    }
    
    .button {
      width: 100%;
      margin-bottom: 5px;
      text-align: center;
    }
  }
  </style>