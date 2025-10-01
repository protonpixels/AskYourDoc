<template>
  <div class="page">
    <div class="hero-container">
      <div class="hero">
        <div class="inputarea">
          <div class="instructions">
            <p>Get Instant Insights From Your eBooks and documents</p>
            <ul>
              <li>1. Upload Your Document.</li>
              <li>2. Type Your Question.</li>
              <li>3. Click The Blue 'Ask' Button.</li>
            </ul>
          </div>
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
  background: $bg-dark-gradient;
}

.hero-container {
  width: 100%;
  min-height: inherit;
  padding: 0 9svw;

  .hero {
    height: 100%;
    display: flex;
    gap: 5svw;
    .questionarea {
      margin-top: 4svh;
      height: calc(99svh - $navheight-desktop - $footerheight-desktop);
      box-shadow: 0 0 30px 1px rgba($orange, 0.3);
      border-radius: 15px;
      width: 100%;
      .answer-display {
        height: 80%;
        width: 100%;
        background: rgba(#fff, 0.6);

        border-bottom: 0;
        border-radius: 15px 15px 0 0;
      }
      overflow: hidden;
      .textarea-and-button {
        display: flex;
        height: 20%;
        border-radius: 0 0 15px 15px;
        border: 8px solid #fff;
        background-color: #fff;
        box-shadow: 0 0 15px 1px rgba($orange, 0.3);
        textarea {
          width: 100%;
          height: 100%;
          padding: 15px;
          font-size: 18px;
          font-family: sans-serif;
          border: 0;

          resize: none;
        }
        .ask-btn {
          border-radius: 15px;
          min-width: 100px;
          border: 0;
          background: transparent;
          color: #fff;
          border-left: 0;
          background: linear-gradient($orange, $yellow);
          outline: none;
          transition: all 0.2s ease;
          box-shadow: inset 0 0 20px 1px lighten($yellow, 40%);
          &:hover {
            background: linear-gradient(-145deg, $orange, $yellow);
            text-shadow: 0 0 8px #fff;
          }

          &:active {
            background: linear-gradient(
              -145deg,
              darken($orange, 20%),
              darken($yellow, 20%)
            );
            box-shadow: inset 0 0 20px 1px darken($orange, 40%);
            color: $yellow;
          }
        }
      }
    }

    .inputarea {
      height: 100%;
      text-align: start;
      width: 40svw;
      .instructions {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin: 45px 0;
        p {
          color: $bg-dark;
          font-size: 22px;
          font-weight: bold;
        }
        ul {
          gap: 14px;
          display: flex;
          flex-direction: column;
          list-style-type: none;
        }
      }

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
    }
  }
}
</style>
