<script setup>
const props = defineProps([
    'text',
    'depth',
])

const tag = props.depth > 6 ? 'h6' : `h${props.depth}`

</script>
<template>
    <component :is="tag">{{ text }}</component>
</template>