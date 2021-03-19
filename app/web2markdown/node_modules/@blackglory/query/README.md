# query

A module for querying elements from pages.

## Install

```sh
npm install --save @blackglory/query
# or
yarn add @blackglory/query
```

## Usage

```ts
import { query, css, xpath } from '@blackglory/query'

const elements = query(
  css`main`
, xpath`//h2[text()="Title"]`
, xpath`../div`
)
```

## API

### query

```ts
type SelectorResult =
| void
| null
| undefined
| Element
| Iterable<Element>

type Selector =
| ((parent: Element) => SelectorResult)
| ((this: Document, parent: Element) => SelectorResult)
| Selector[]

function query<T extends Element>(this: void | Document, ...selectors: Selector[]): T[]
```

### css

```ts
function css<T extends Element>(strings: TemplateStringsArray, ...values: string[]): (parent: ParentNode) => Iterable<T>
```

### xpath

```ts
function xpath<T extends Element>(strings: TemplateStringsArray, ...values: string[]): (this: Document, parent: Node) => Iterable<T>
```
