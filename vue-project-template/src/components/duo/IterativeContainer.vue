<script setup>
import * as $rdf from 'rdflib'

const props = defineProps([
    'graph',
    'depth',
    'object',
    'predicate',
])

const objects = props.graph?.match(props.object, props.predicate) || []

const absoluteUrlRegex = /(?:^[a-z][a-z0-9+\.-]*:|\/\/)/
const wrapObject = (obj) => {
    const url = obj.object.value
    if (url.match(absoluteUrlRegex)) {
        return $rdf.sym(url)
    } else {
        return new $rdf.BlankNode(url)
    }
}
</script>
<template>
    <div>
        <div v-for="(obj, index) in objects" :key="index">
            <slot :depth="depth" :object="wrapObject(obj)"></slot>
        </div>
    </div>
</template>