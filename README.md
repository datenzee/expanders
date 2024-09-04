# Datenzee Expanders

## Installation

```
$ make install
```

## Usage

Expand and build the application:

```
$ expander <type> <root-component> <path-to-owl> <path-to-out-dir>
```

Where type can be

- `vue`
- `doc`

Expand and run dev mode:

```
$ expander --dev <type> <path-to-owl> <path-to-out-dir>
```

By default the application is running on http://localhost:8081/.

You can use GET parameters to specify data source and root node in the graph with:

- `data` - full URL of the data
- `root` - full IRI of the root node in the graph

**Example**
```
http://localhost:8081/?data=https://datenzee.ds-wizard.org/wizard-api/questionnaires/9a710add-11b7-4544-a432-82727b45eca6/documents/preview
```

## License

This project is licensed under the Apache License v2.0 - see the [LICENSE](LICENSE) file for more details.
