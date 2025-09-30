<template>
  <div class="page">
    <div class="hero-container">
      <div class="hero">
        <div class="inputarea"></div>
        <div class="questionarea">
          <div class="answer-display"></div>
          <div class="textarea-and-button">
            <textarea
              name="questioninput"
              placeholder="What do you want to know from this document?"
              :disabled="documentUploaded ? true : false"
            ></textarea>
            <button class="ask-btn">Ask</button>
          </div>
        </div>
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
  min-height: calc(100svh - $navheight-desktop);
}

.hero-container {
  width: 100%;
  height: 100%;
  padding: 0 12svw;
}

.hero {
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 2fr;
  .answer-display {
    min-height: 300px;
    height: 100%;
    width: 100%;
    background: #fff;
    border: 1px solid blue;
    border-bottom: 0;
    border-top: 0;
    box-shadow: inset 0 0 30px 1px rgba(blue, 0.3);
  }
  .textarea-and-button {
    display: flex;
    textarea {
      width: 100%;
      height: 100px;
      border-radius: 0 0 0 15px;
      padding: 15px;
      resize: none;
      border: 1px solid blue;
    }
    .ask-btn {
      border-radius: 0 0 15px 0;
      min-width: 80px;
      border: 1px solid blue;
      background: blue;
      color: #fff;
      border-left: 0;
    }
  }
}
</style>
