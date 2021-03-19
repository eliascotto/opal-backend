# extra-dom

Utilities for DOM.

## Install

```sh
npm install --save extra-dom
# or
yarn add extra-dom
```

## API

### flatMap

```ts
function flatMap(node: Node, fn: (node: Node) => Node[]): Node[]
```

Traverse the node tree and do `flatMap`.

- `[]`: remove current node
- `[node]`: replace current node
- `[node1, node2, ...nodeN]`: replace current node with more nodes

### map

```ts
function map(node: Node, fn: (node: Node) => Node): Node
```

Traverse the node tree and do `map`.

### filter

```ts
function filter(node: Node, predicate: (node: Node) => boolean): Node | null
```

Traverse the node tree and do `filter`.

### unwrap

```ts
function unwrap(node: Node, predicate: (node: Node) => boolean): Node[]
```

Traverse the node tree and do `unwrap`.

### parse

```ts
function parse(html: string): Node[]
```

### stringify

```ts
function stringify(nodes: Node[]): string
```

### normalize

```ts
function normalize(html: string): string
```

It is the shortcut for `stringify(parse(html))`.

### removeAllChildren

```ts
function removeAllChildren(node: Node): void
```

### removeAttributes

```ts
function removeAttributes(node: Node, predicate: (name: string) => boolean): void
```

### getBySelector

```ts
function getBySelector<T extends Element>(this: void | Element | Document, selectors: string): T
```

Return the first matched element.

If cannot find any elements, it throws.

### getAllBySelector

```ts
function getAllBySelector<T extends Element>(this: void | Element | Document, selectors: string): T[]
```

Return matched elements.

If cannot find any elements, it throws.

### isDocument

```ts
function isDocument(val: any): val is Document
```

### isElement

```ts
function isElement(val: any): val is Element
```

### NodeConstants

```ts
enum NodeConstants {
  ELEMENT_NODE
, ATTRIBUTE_NODE
, TEXT_NODE
, CDATA_SECTION_NODE
, ENTITY_REFERENCE_NODE
, ENTITY_NODE
, PROCESSING_INSTRUCTION_NODE
, COMMENT_NODE
, DOCUMENT_NODE
, DOCUMENT_TYPE_NODE
, DOCUMENT_FRAGMENT_NODE
, NOTATION_NODE
}
```

### XPathResultConstants {
  ANY_TYPE
, NUMBER_TYPE
, STRING_TYPE
, BOOLEAN_TYPE
, UNORDERED_NODE_ITERATOR_TYPE
, ORDERED_NODE_ITERATOR_TYPE
, UNORDERED_NODE_SNAPSHOT_TYPE
, ORDERED_NODE_SNAPSHOT_TYPE
, ANY_UNORDERED_NODE_TYPE
, FIRST_ORDERED_NODE_TYPE
}
