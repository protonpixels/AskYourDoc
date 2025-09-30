<template>
  <div class="page">
    <div class="hero-container">
      <div class="hero">
        <div class="inputarea">
          <div class="header">
            <h1>Upload Your Docs</h1>
            <h2>Ask Questions and Get Answers</h2>
            <div class="file-selector">
              <div class="file-input-wrapper">
                <input
                  type="file"
                  ref="fileInputRef"
                  @change="handleFileSelect"
                  class="file-input"
                  :accept="accept"
                  :multiple="multiple"
                />
                <button @click="triggerFileInput" class="custom-button">
                  Choose File
                </button>
                <span v-if="selectedFile" class="file-name">
                  {{ selectedFile.name }}
                </span>
                <span v-else class="placeholder">No file chosen</span>
              </div>

              <div v-if="multiple && selectedFiles.length" class="file-list">
                <h4>Selected Files:</h4>
                <ul>
                  <li v-for="(file, index) in selectedFiles" :key="index">
                    {{ file.name }} ({{ formatFileSize(file.size) }})
                    <button @click="removeFile(index)" class="remove-btn">
                      Remove
                    </button>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
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
import { ref, defineProps, computed } from "vue";

const props = defineProps({
  accept: {
    type: String,
    default: "*/*",
  },
  multiple: {
    type: Boolean,
    default: false,
  },
  maxFiles: {
    type: Number,
    default: null,
  },
});

const emit = defineEmits(["files-selected", "file-removed"]);

const fileInputRef = ref(null);
const selectedFile = ref(null);
const selectedFiles = ref([]);

const triggerFileInput = () => {
  fileInputRef.value?.click();
};

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files);

  if (props.multiple) {
    // Check max files limit
    if (
      props.maxFiles &&
      selectedFiles.value.length + files.length > props.maxFiles
    ) {
      alert(`Maximum ${props.maxFiles} files allowed`);
      return;
    }

    selectedFiles.value = [...selectedFiles.value, ...files];
    selectedFile.value = null;
  } else {
    selectedFile.value = files[0];
    selectedFiles.value = [];
  }

  // Reset input to allow selecting same file again
  event.target.value = "";

  emit(
    "files-selected",
    props.multiple ? selectedFiles.value : selectedFile.value
  );
};

const removeFile = (index) => {
  const removedFile = selectedFiles.value[index];
  selectedFiles.value.splice(index, 1);
  emit("file-removed", removedFile);
  emit("files-selected", selectedFiles.value);
};

const formatFileSize = (bytes) => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};

// Expose methods to parent component if needed
defineExpose({
  clearFiles: () => {
    selectedFile.value = null;
    selectedFiles.value = [];
  },
  getFiles: () => (props.multiple ? selectedFiles.value : selectedFile.value),
});
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

  .inputarea {
    padding-top: calc($navheight-desktop * 0.382);
    text-align: start;

    .file-input-wrapper {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 15px;
    }

    .file-input {
      display: none;
    }

    .custom-button {
      padding: 10px 20px;
      background: #007bff;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      transition: background-color 0.2s;
    }

    .custom-button:hover {
      background: #0056b3;
    }

    .file-name {
      color: #28a745;
      font-weight: 500;
    }

    .placeholder {
      color: #6c757d;
    }

    .file-list {
      margin-top: 15px;
    }

    .file-list ul {
      list-style: none;
      padding: 0;
      margin: 0;
    }

    .file-list li {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 12px;
      margin: 5px 0;
      background: #f8f9fa;
      border: 1px solid #dee2e6;
      border-radius: 4px;
    }

    .remove-btn {
      padding: 4px 8px;
      background: #dc3545;
      color: white;
      border: none;
      border-radius: 3px;
      cursor: pointer;
      font-size: 12px;
    }

    .remove-btn:hover {
      background: #c82333;
    }

    h1 {
      font-size: 28px;
      margin-bottom: calc($navheight-desktop * 0.382);
    }
    h2 {
      font-size: 20px;
      margin-bottom: calc($navheight-desktop * 0.382);
    }
  }
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
