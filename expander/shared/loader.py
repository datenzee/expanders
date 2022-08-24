from rdflib import Namespace, Graph

from expander.shared.duio.ConditionComponent import ConditionComponent
from expander.shared.duio.ContainerComponent import ContainerComponent
from expander.shared.duio.EmphasisComponent import EmphasisComponent
from expander.shared.duio.HeadingComponent import HeadingComponent
from expander.shared.duio.IterativeContainerComponent import IterativeContainerComponent
from expander.shared.duio.StrongComponent import StrongComponent
from expander.shared.duio.TextComponent import TextComponent

DUIO = Namespace('http://purl.org/datenzee/ui-ontology#')
RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')


class Loader:
    def __init__(self, source=None, data=None):
        self.source = source
        self.data = data
        self.graph = None
        self.components = []

    def load(self):
        g = Graph()
        try:
            g.parse(source=self.source, data=self.data, format='turtle')
            self.graph = g
            self._load()
        except FileNotFoundError:
            pass

    def _load(self):
        app = next(self.graph.subjects(RDF.type, DUIO.App))

        root_component = next(self.graph.objects(app, DUIO.rootComponent))

        self._create_component(root_component)

        for component in self.components:
            print(component)

    def _create_component(self, component):
        component_name = component.split('#')[-1]
        component_types = list(self.graph.objects(component, RDF.type))
        component_is_block = next(self.graph.objects(component, DUIO.componentIsBlock))

        create_content_component = lambda constructor: self._create_content_component(
            component, constructor, component_name, component_is_block)

        if DUIO.Container in component_types:
            children = []
            child = next(self.graph.objects(component, DUIO.containerContains))

            while child:
                child_component = next(self.graph.objects(child, DUIO.containerListFirst))
                children.append(self._create_component(child_component))

                rest = list(self.graph.objects(child, DUIO.containerListRest))
                if len(rest) > 0:
                    child = rest[0]
                else:
                    child = None

            created_component = ContainerComponent(component_name, component_is_block, children)

        elif DUIO.IterativeContainer in component_types:
            predicate = next(self.graph.objects(component, DUIO.iterativeContainerPredicate))
            content = next(self.graph.objects(component, DUIO.iterativeContainerContent))
            content_component = self._create_component(content)
            created_component = IterativeContainerComponent(component_name, component_is_block, content_component,
                                                            predicate)

        elif DUIO.ConditionComponent in component_types:
            predicate = next(self.graph.objects(component, DUIO.conditionComponentPredicate))
            value = next(self.graph.objects(component, DUIO.conditionComponentValue))
            positive_content = next(self.graph.objects(component, DUIO.conditionComponentPositiveContent))
            negative_content = next(self.graph.objects(component, DUIO.conditionComponentNegativeContent))

            positive_content_component = self._create_component(positive_content)
            negative_content_component = self._create_component(negative_content)

            created_component = ConditionComponent(component_name, component_is_block, predicate, value,
                                                   positive_content_component, negative_content_component)


        elif DUIO.HeadingComponent in component_types:
            created_component = create_content_component(HeadingComponent)

        elif DUIO.TextComponent in component_types:
            created_component = create_content_component(TextComponent)

        elif DUIO.StrongComponent in component_types:
            created_component = create_content_component(StrongComponent)

        elif DUIO.EmphasisComponent in component_types:
            created_component = create_content_component(EmphasisComponent)

        else:
            raise AttributeError(f'Unknown component type: {component_types}')

        self.components.append(created_component)
        return created_component

    def _create_content_component(self, component, constructor, name, is_block):
        predicate = self._load_content_component_predicate(component)
        text = self._load_content_component_text(component)
        return constructor(name, is_block, predicate, text)

    def _load_content_component_predicate(self, component):
        for predicate in self.graph.objects(component, DUIO.contentComponentPredicate):
            return predicate
        return None

    def _load_content_component_text(self, component):
        for component_content in self.graph.objects(component, DUIO.contentComponentContent):
            return next(self.graph.objects(component_content, DUIO.textContentValue))
        return None
