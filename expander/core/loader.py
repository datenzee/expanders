from rdflib import Namespace, Graph

from expander.core.duo.ContainerComponent import ContainerComponent
from expander.core.duo.HeadingComponent import HeadingComponent
from expander.core.duo.IterativeContainerComponent import IterativeContainerComponent
from expander.core.duo.ParagraphComponent import ParagraphComponent
from expander.core.duo.TitleComponent import TitleComponent

DUO = Namespace('http://www.semanticweb.org/janslifka/ontologies/2022/2/datenzee-ui-ontology#')
RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')


class Loader:
    def __init__(self, file):
        self.file = file
        self.graph = None
        self.components = []

    def load(self):
        g = Graph()
        try:
            g.parse(self.file, format='turtle')
            self.graph = g
            self._load()
        except FileNotFoundError:
            pass

    def _load(self):
        app = next(self.graph.subjects(RDF.type, DUO.App))

        root_component = next(self.graph.objects(app, DUO.rootComponent))

        self._create_component(root_component)

        for component in self.components:
            print(component)

    def _create_component(self, component):
        component_name = component.split('#')[-1]
        component_types = list(self.graph.objects(component, RDF.type))

        if DUO.Container in component_types:
            children = []
            child = next(self.graph.objects(component, DUO.containerContains))

            while child:
                child_component = next(self.graph.objects(child, DUO.containerListFirst))
                children.append(self._create_component(child_component))

                rest = list(self.graph.objects(child, DUO.containerListRest))
                if len(rest) > 0:
                    child = rest[0]
                else:
                    child = None

            created_component = ContainerComponent(component_name, children)

        elif DUO.IterativeContainer in component_types:
            predicate = next(self.graph.objects(component, DUO.iterativeContainerPredicate))
            content = next(self.graph.objects(component, DUO.iterativeContainerContent))
            content_component = self._create_component(content)
            created_component = IterativeContainerComponent(component_name, content_component, predicate)

        elif DUO.TitleComponent in component_types:
            title_predicate = next(self.graph.objects(component, DUO.titleComponentPredicate))
            created_component = TitleComponent(component_name, title_predicate)

        elif DUO.HeadingComponent in component_types:
            content = next(self.graph.objects(component, DUO.plainTextComponentContent))
            created_component = HeadingComponent(component_name, content)

        elif DUO.ParagraphComponent in component_types:
            content = next(self.graph.objects(component, DUO.plainTextComponentContent))
            created_component = ParagraphComponent(component_name, content)

        else:
            raise AttributeError(f'Unknown component type: {component_types}')

        self.components.append(created_component)
        return created_component
