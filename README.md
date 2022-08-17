# Datenzee Expanders

## Installation

```
$ make install
```

## Usage

Expand and build the application:

```
$ expander <type> <path-to-owl> <path-to-out-dir>
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
http://localhost:8081/?data=https://api.datenzee.ds-wizard.org/questionnaires/4dac4509-f0a3-4346-b7ce-586a3098b100/documents/preview&root=https://demo.ds-wizard.org/questionnaires/00f2e7b7-a1c8-42a1-a2fc-2f93dbdbaa76
```
