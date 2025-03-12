<template>
    <div class="image-card">
      <div class="image-container">
        <img 
          :src="image.thumbnail" 
          :alt="'Image from ' + image.source"
          @click="$emit('select-image', image)"
          loading="lazy"
        />
        <div class="image-source">{{ image.source }}</div>
      </div>
      <div class="image-info">
        <div class="photographer">
          By: <a :href="image.photographer_url" target="_blank">{{ image.photographer }}</a>
        </div>
        <div class="dimensions">{{ image.width }}×{{ image.height }}</div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ImageCard',
    props: {
      image: {
        type: Object,
        required: true
      }
    }
  }
  </script>
  
  <style scoped>
  .image-card {
    background-color: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .image-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  }
  
  .image-container {
    position: relative;
    padding-top: 75%; /* 4:3 Aspect Ratio */
    overflow: hidden;
  }
  
  .image-container img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    cursor: pointer;
    transition: transform 0.3s;
  }
  
  .image-container img:hover {
    transform: scale(1.05);
  }
  
  .image-source {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
  }
  
  .image-info {
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
  }
  
  .photographer a {
    color: #3498db;
    text-decoration: none;
  }
  
  .photographer a:hover {
    text-decoration: underline;
  }
  
  .dimensions {
    color: #7f8c8d;
  }
  </style>