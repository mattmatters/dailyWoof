<template>
    <div class="story">
        <img class="small" v-bind:src="image">
        <h3 class="story-title">{{ title }}</h3>
        <p class="description">{{ description }}</p>
        <button v-if="!showStory" v-on:click="show"> More </button>
        <p v-if="showStory" class="story-body">{{ story }}</p>

    </div>
</template>

<script>
export default {
  name: 'Story',
  props: [
    'image',
    'title',
    'description',
    'story',
  ],
  data: () => ({ showStory: false }),
  methods: {
    show() {
      this.showStory = !this.showStory;
    },
  },
};
</script>

<style scoped>
 .story {
     background-color: #4b3f72;
     border-radius: 1em;
     padding: 1em;
     margin: 1em;
 }

 p {
     color: #119da4;
 }

 .story-title {
     font-weight: bold;
     color: #ffc857;
 }

 .story-body {
     text-align: left;
     white-space: pre-wrap;
     word-wrap: break-word;
     font-family: inherit;
 }

 a {
     color: #196473;
 }

 .small {
     width: 50%;
 }
</style>
