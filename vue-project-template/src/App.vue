<script setup>
import * as $rdf from 'rdflib'
import data from './data'
import RootContainer from '@/components/gen/Container_Root.vue'

const object = $rdf.sym('https://demo.ds-wizard.org/questionnaires/00f2e7b7-a1c8-42a1-a2fc-2f93dbdbaa76')
const graph = new $rdf.IndexedFormula()
$rdf.parse(data, graph, object.uri, 'text/turtle')
</script>
<template>
  <main>
    <RootContainer :graph="graph" :depth="0" :object="object" />
  </main>
</template>
