<template>
  <div id="app">
    <header class="app-header">
      <h1>Royalty-Free Image Search</h1>
      <p>Search across Pexels, Pixabay, Unsplash, Wikipedia and more</p>
    </header>

    <div class="search-container">
      <div class="search-bar">
        <input 
          type="text" 
          v-model="searchQuery" 
          @keyup.enter="searchImages"
          placeholder="Search for images..."
          :disabled="isLoading"
        />
        <button @click="searchImages" :disabled="isLoading">
          <span v-if="isLoading">Searching...</span>
          <span v-else>Search</span>
        </button>
      </div>

      <div class="filter-options">
        <div class="source-filters">
          <h3>Sources:</h3>
          <div>
            <label>
              <input type="checkbox" v-model="allSources" @change="toggleAllSources">
              All Sources
            </label>
            <label v-for="source in availableSources" :key="source">
              <input 
                type="checkbox" 
                :value="source" 
                v-model="selectedSources"
                @change="handleSourceChange"
              >
              {{ source }}
            </label>
          </div>
        </div>

        <div class="per-page-selector">
          <h3>Results per source:</h3>
          <select v-model="perPage">
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="30">30</option>
          </select>
        </div>
      </div>
    </div>

    <div class="results-container" v-if="searchPerformed">
      <div v-if="isLoading" class="loading">
        <div class="spinner"></div>
        <p>Searching across multiple sources...</p>
      </div>

      <div v-else-if="errorMessage" class="error-message">
        <p>{{ errorMessage }}</p>
      </div>

      <div v-else-if="images.length === 0" class="no-results">
        <p>No images found for "{{ lastSearchQuery }}". Try a different search term.</p>
      </div>

      <div v-else class="results-info">
        <p>Found {{ images.length }} images for "{{ lastSearchQuery }}"</p>
      </div>

      <div class="image-grid" v-if="images.length > 0">
        <ImageCard 
          v-for="image in images" 
          :key="image.id" 
          :image="image"
          @select-image="selectImage"
        />
      </div>
    </div>

    <!-- Image Preview Modal -->
    <ImageModal 
      :image="selectedImage" 
      @close="closeModal" 
      v-if="selectedImage"
    />
  </div>
</template>

<script>
import ImageCard from './components/ImageCard.vue';
import ImageModal from './components/ImageModel.vue';

export default {
  name: 'App',
  components: {
    ImageCard,
    ImageModal
  },
  data() {
    return {
      searchQuery: '',
      lastSearchQuery: '',
      images: [],
      isLoading: false,
      errorMessage: '',
      searchPerformed: false,
      selectedImage: null,
      perPage: 10,
      availableSources: ['Pexels', 'Pixabay', 'Unsplash', 'Wikipedia'],
      selectedSources: ['Pexels', 'Pixabay', 'Unsplash', 'Wikipedia'],
      allSources: true,
      apiBaseUrl: process.env.VUE_APP_API_URL || 'http://localhost:5002/api'
    };
  },
  methods: {
    async searchImages() {
      if (!this.searchQuery.trim()) {
        this.errorMessage = 'Please enter a search term';
        return;
      }

      this.isLoading = true;
      this.errorMessage = '';
      this.searchPerformed = true;
      this.lastSearchQuery = this.searchQuery;
      
      try {
        // Build the sources parameter
        const sourcesParam = this.allSources ? 'all' : this.selectedSources.join(',').toLowerCase();
        
        const response = await fetch(
          `${this.apiBaseUrl}/search?query=${encodeURIComponent(this.searchQuery)}&per_page=${this.perPage}&sources=${sourcesParam}`
        );
        
        if (!response.ok) {
          throw new Error(`Server returned ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        this.images = data.results;
        
        // Sort results by source for better grouping
        this.images.sort((a, b) => a.source.localeCompare(b.source));
      } catch (error) {
        console.error('Error fetching images:', error);
        this.errorMessage = `Failed to search for images: ${error.message}`;
        this.images = [];
      } finally {
        this.isLoading = false;
      }
    },
    
    selectImage(image) {
      this.selectedImage = image;
    },
    
    closeModal() {
      this.selectedImage = null;
    },
    
    toggleAllSources() {
      if (this.allSources) {
        this.selectedSources = [...this.availableSources];
      } else {
        this.selectedSources = [];
      }
    },
    
    handleSourceChange() {
      this.allSources = this.selectedSources.length === this.availableSources.length;
    }
  }
};
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body.modal-open {
  overflow: hidden;
}

#app {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.app-header {
  text-align: center;
  margin-bottom: 30px;
}

.app-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.app-header p {
  color: #7f8c8d;
  font-size: 1.1rem;
}

.search-container {
  margin-bottom: 30px;
}

.search-bar {
  display: flex;
  margin-bottom: 15px;
}

.search-bar input {
  flex: 1;
  padding: 12px 15px;
  font-size: 1rem;
  border: 2px solid #ddd;
  border-radius: 4px 0 0 4px;
  outline: none;
  transition: border-color 0.3s;
}

.search-bar input:focus {
  border-color: #3498db;
}

.search-bar button {
  padding: 0 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s;
}

.search-bar button:hover {
  background-color: #2980b9;
}

.search-bar button:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.filter-options {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 15px;
  background-color: #ecf0f1;
  border-radius: 4px;
}

.source-filters, .per-page-selector {
  margin-right: 20px;
}

.source-filters h3, .per-page-selector h3 {
  margin-bottom: 10px;
  font-size: 1rem;
  color: #2c3e50;
}

.source-filters label {
  margin-right: 15px;
  display: inline-block;
  cursor: pointer;
}

.per-page-selector select {
  padding: 5px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  background-color: white;
}

.loading {
  text-align: center;
  padding: 50px 0;
}

.spinner {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #3498db;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  padding: 20px;
  background-color: #f8d7da;
  color: #721c24;
  border-radius: 4px;
  margin-bottom: 20px;
}

.no-results {
  text-align: center;
  padding: 50px 0;
  color: #7f8c8d;
}

.results-info {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #e8f4fd;
  border-radius: 4px;
  font-weight: bold;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .filter-options {
    flex-direction: column;
  }
  
  .source-filters, .per-page-selector {
    margin-bottom: 15px;
    width: 100%;
  }
  
  .image-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}
</style>