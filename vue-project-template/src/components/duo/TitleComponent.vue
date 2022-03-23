<script setup lang="ts">
import * as $rdf from 'rdflib'
import Heading from './Heading.vue'

const props = defineProps(['graph', 'depth', 'object', 'predicate'])

</script>
<template>
    <Heading :depth="depth" :text="graph?.match(object, predicate)[0]?.object.value" />
</template>
