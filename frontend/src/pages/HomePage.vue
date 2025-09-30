<template>
  <div class="page">
    <div class="hero">
      <div class="hero-container">
        <textarea
          name="questioninput"
          placeholder="What do you want to know from this document?"
          :disabled="documentUploaded ? true : false"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const documentUploaded = ref(false);
</script>

<style lang="scss" scoped>
.page {
  width: 100%;
  min-height: 100svh;
  background-color: #000;
}

.hero-container {
  width: 100%;
  height: 100%;
}

.hero {
}
</style>
