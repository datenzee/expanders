<script setup>
import * as $rdf from 'rdflib'

const props = defineProps([
    'graph',
    'depth',
    'object',
    'predicate',
])

const objects = props.graph?.match(props.object, props.predicate) || []
const blankNode = (obj) => new $rdf.BlankNode(obj.object.value)
</script>
<template>
    <div>
        <div v-for="(obj, index) in objects" :key="index">
            <slot :depth="depth" :object="blankNode(obj)"></slot>
        </div>
    </div>
</template>