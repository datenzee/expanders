from rdflib import Namespace, Graph

from expander.core.duio.ContainerComponent import ContainerComponent
from expander.core.duio.HeadingComponent import HeadingComponent
from expander.core.duio.IterativeContainerComponent import IterativeContainerComponent
from expander.core.duio.ParagraphComponent import ParagraphComponent

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

            created_component = ContainerComponent(component_name, children)

        elif DUIO.IterativeContainer in component_types:
            predicate = next(self.graph.objects(component, DUIO.iterativeContainerPredicate))
            content = next(self.graph.objects(component, DUIO.iterativeContainerContent))
            content_component = self._create_component(content)
            created_component = IterativeContainerComponent(component_name, content_component, predicate)

        elif DUIO.HeadingComponent in component_types:
            predicate = self._load_content_component_predicate(component)
            text = self._load_content_component_text(component)
            created_component = HeadingComponent(component_name, predicate, text)

        elif DUIO.ParagraphComponent in component_types:
            predicate = self._load_content_component_predicate(component)
            text = self._load_content_component_text(component)
            created_component = ParagraphComponent(component_name, predicate, text)

        else:
            raise AttributeError(f'Unknown component type: {component_types}')

        self.components.append(created_component)
        return created_component

    def _load_content_component_predicate(self, component):
        for predicate in self.graph.objects(component, DUIO.contentComponentPredicate):
            return predicate
        return None

    def _load_content_component_text(self, component):
        for component_content in self.graph.objects(component, DUIO.contentComponentContent):
            return next(self.graph.objects(component_content, DUIO.textContentValue))
        return None
