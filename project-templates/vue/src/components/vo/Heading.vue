<script setup>
const props = defineProps([
    'depth',
])

const tag = props.depth > 6 ? 'h6' : `h${props.depth}`

</script>
<template>
    <component :is="tag">
        <slot></slot>
    </component>
</template>