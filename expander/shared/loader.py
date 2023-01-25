from rdflib import Namespace, Graph, URIRef

from expander.shared.vo.Condition import Condition
from expander.shared.vo.Container import Container
from expander.shared.vo.Content import Content
from expander.shared.vo.DataComponent import DataComponent
from expander.shared.vo.DataComponentWrapper import DataComponentWrapper
from expander.shared.vo.Date import Date
from expander.shared.vo.DateTime import DateTime
from expander.shared.vo.Email import Email
from expander.shared.vo.Emphasis import Emphasis
from expander.shared.vo.Heading import Heading
from expander.shared.vo.IterativeContainer import IterativeContainer
from expander.shared.vo.Strong import Strong
from expander.shared.vo.Time import Time
from expander.shared.vo.Url import Url

VO = Namespace('http://purl.org/datenzee/view-ontology#')
RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')

NODE_TYPES = (
    VO.Condition,
    VO.Container,
    VO.Emphasis,
    VO.Heading,
    VO.IterativeContainer,
    VO.Strong,
)

LEAF_TYPES = (
    VO.DataComponentWrapper,
    VO.Content,
    VO.Date,
    VO.DateTime,
    VO.Email,
    VO.Time,
    VO.URL
)


class Loader:
    def __init__(self, root_component, source=None, data=None):
        self.root_component = URIRef(root_component)
        self.root_component_name = root_component.split('#')[-1]
        self.source = source
        self.data = data
        self.graph = None
        self.data_components = []
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
        self._create_data_component(self.root_component)

    def _create_data_component(self, data_component):
        component_name = data_component.split('#')[-1]
        component_types = list(self.graph.objects(data_component, RDF.type))

        if VO.DataComponent not in component_types:
            raise Exception(f'The root component {component_name} is not a Data Component')

        if self._data_component_exists(component_name):
            return

        data_component_content = next(self.graph.objects(data_component, VO.dataComponentContent))
        content_component = self._create_component(data_component_content)

        self.data_components.append(DataComponent(component_name, content_component))

    def _create_component(self, component):
        component_name = component.split('#')[-1]
        component_types = list(self.graph.objects(component, RDF.type))

        if self._is_node(component_types):
            return self._create_node(component_name, component_types, component)
        elif self._is_leaf(component_types):
            return self._create_leaf(component_name, component_types, component)
        else:
            raise Exception(f'Component {component_name} is neither Node nor Leaf')

    def _is_node(self, component_types):
        return any(type in NODE_TYPES for type in component_types)

    def _is_leaf(self, component_types):
        return any(type in LEAF_TYPES for type in component_types)

    def _create_leaf(self, component_name, component_types, component):
        order = next(self.graph.objects(component, VO.order))

        if VO.DataComponentWrapper in component_types:
            predicate = next(self.graph.objects(component, VO.dataComponentPredicate))
            data_component = next(self.graph.objects(component, VO.dataComponent))
            self._create_data_component(data_component)

            wrapper = DataComponentWrapper(component_name, order, predicate, data_component)
            self.components.append(wrapper)
            return wrapper
        else:
            predicate = self._load_content_component_predicate(component)
            content = self._load_content_component_content(component)

            if VO.Date in component_types:
                date = Date(component_name, order, predicate, content)
                self.components.append(date)
                return date

            elif VO.DateTime in component_types:
                date_time = DateTime(component_name, order, predicate, content)
                self.components.append(date_time)
                return date_time

            elif VO.Email in component_types:
                email = Email(component_name, order, predicate, content)
                self.components.append(email)
                return email

            elif VO.Time in component_types:
                time = Time(component_name, order, predicate, content)
                self.components.append(time)
                return time

            elif VO.URL in component_types:
                url = Url(component_name, order, predicate, content)
                self.components.append(url)
                return url

            elif VO.Content in component_types:
                c = Content(component_name, order, predicate, content)
                self.components.append(c)
                return c

            else:
                raise Exception('Unknown leaf type')

    def _create_node(self, component_name, component_types, component):
        order = next(self.graph.objects(component, VO.order))
        is_block = next(self.graph.objects(component, VO.isBlock))

        def create_children(predicate=VO.contains):
            children = []
            for child in self.graph.objects(component, predicate):
                children.append(self._create_component(child))
            return sorted(children, key=lambda c: c.order)

        if VO.Condition in component_types:
            condition_predicate = next(self.graph.objects(component, VO.conditionPredicate))
            condition_value = next(self.graph.objects(component, VO.conditionValue))
            contains_positive = create_children(VO.conditionContainsPositive)
            contains_negative = create_children(VO.conditionContainsNegative)

            container = Condition(component_name, order, is_block, condition_predicate, condition_value,
                                  contains_positive, contains_negative)
            self.components.append(container)
            return container

        elif VO.Container in component_types:
            container = Container(component_name, order, is_block, create_children())
            self.components.append(container)
            return container

        elif VO.Emphasis in component_types:
            emphasis = Emphasis(component_name, order, is_block, create_children())
            self.components.append(emphasis)
            return emphasis

        elif VO.Heading in component_types:
            heading = Heading(component_name, order, is_block, create_children())
            self.components.append(heading)
            return heading

        elif VO.IterativeContainer in component_types:
            iterative_container_predicate = next(self.graph.objects(component, VO.iterativeContainerPredicate))
            iterative_container = IterativeContainer(component_name, order, is_block, create_children(),
                                                     iterative_container_predicate)
            self.components.append(iterative_container)
            return iterative_container

        elif VO.Strong in component_types:
            strong = Strong(component_name, order, is_block, create_children())
            self.components.append(strong)
            return strong

        else:
            raise Exception('Unknown node type')

    def _load_content_component_predicate(self, component):
        for predicate in self.graph.objects(component, VO.contentPredicate):
            return predicate
        return None

    def _load_content_component_content(self, component):
        for text_content in self.graph.objects(component, VO.contentContent):
            return next(self.graph.objects(text_content, VO.textContentValue))
        return None

    def _data_component_exists(self, component_name):
        for data_component in self.data_components:
            if data_component.name == component_name:
                return True
        return False
