<script setup>
import * as $rdf from 'rdflib'
import data from './data'
import RootContainer from '@/components/gen/Container_Root.vue'
import {reactive} from "@vue/reactivity";
import axios from "axios";

const state = reactive({
    object: null,
    graph: null,
    loading: true,
    error: null,
})

const url = new URL(window.location.href)

const root = url.searchParams.get('root') || 'https://demo.ds-wizard.org/questionnaires/00f2e7b7-a1c8-42a1-a2fc-2f93dbdbaa76'
state.object = $rdf.sym(root)

const createGraph = (turtle) => {
    try {
      const graph = new $rdf.IndexedFormula()
      $rdf.parse(turtle, graph, state.object.uri, 'text/turtle')
      state.graph = graph
      state.loading = false
    } catch (error) {
      state.loading = false
      state.error = error.toString()
    }
}

const dataUrl = url.searchParams.get('data')
if (dataUrl) {
    axios
        .get(dataUrl)
        .then((result) => {
            createGraph(result.data)
        })
} else {
    createGraph(data)
}
</script>
<template>
    <main>
        <div v-if="state.loading">Loading...</div>
        <div v-else-if="state.error" class="text-danger">{{ state.error }}</div>
        <RootContainer v-else :graph="state.graph" :depth="0" :object="object"/>
    </main>
</template>
