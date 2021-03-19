import Readability from './Readability'
import axios from 'axios'
import { JSDOM } from 'jsdom'
import createDOMPurify from 'dompurify'
import unified from 'unified'
import parse from 'rehype-parse'
import sanitize from 'hast-util-sanitize'
import toMdast from 'hast-util-to-mdast'
import toMarkdown from 'mdast-util-to-markdown'
import table from 'mdast-util-gfm-table'
import visit from 'unist-util-visit-parents'

const URL_R = /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/

const BLOCK_TYPES = [
  'paragraph',
  'blockquote',
  'heading',
  'code',
  'table',
]

const META_PROPERTIES = [
  'og:title',
  'og:description',
  'og:locale',
  'og:type',
  'og:url',
  'og:image',
  'article:tag',
]

const args = process.argv.slice(2)

function extractMeta(document) {
  const properties = {}

  META_PROPERTIES.forEach(prop => {
    const metas = document.head.querySelectorAll(`[property="${prop}"][content]`)
    const name = prop.split(':')[1]

    if (metas && metas.length > 0) {
      if (metas.length > 1) {
        properties[name] = [...metas].map(el => el.content)
      } else {
        properties[name] = metas[0].content
      }
    }
  })
  
  return properties
}

function parseHTML(html) {
  const hast = unified()
    .use(parse)
    .use(sanitize)
    .parse(html)

  const mdast = toMdast(hast)
  const blocks = []
  let count = 0

  visit(mdast, BLOCK_TYPES, (node, ancestors) => {
    const last = ancestors[ancestors.length - 1]
    let list = null
    let indent = 0
    const properties = {}
    const links = []

    if (node.hasOwnProperty('position')) {
      delete node['position']
    }

    const isList = last && last.type === 'listItem'

    if (isList) {
      // Count list intentation
      const listIndent = ancestors.filter(a => a.type === 'listItem').length - 1
      indent = listIndent
    }

    properties['raw'] = toMarkdown(node, {extensions: [table.toMarkdown()]})
    
    visit(node, null, (childNode) => {
      if (childNode.type === 'link') {
        links.push(childNode.url)
      }
    })

    if (links.length > 0) {
      properties['links'] = links
    }

    blocks.push({
      ...node,
      type: node.type,
      position: count,
      indent,
      list,
      properties,
    })

    count += 1
  })

  return blocks
}

if (args.length === 1 && URL_R.test(args[0])) {
  const url = args[0]

  axios.get(url).then((response) => {
    const html = response.data

    // DOMPurify process on node require a DOM
    const _window = new JSDOM('').window
    const DOMPurify = createDOMPurify(_window)
    // Whole document with head for retrieve the title of the documnent
    const cleanHTML = DOMPurify.sanitize(html, {
      WHOLE_DOCUMENT: true,
      ADD_URI_SAFE_ATTR: ['property'],
      ADD_TAGS: ['head', 'meta'],
      ADD_ATTR: ['content', 'property'],
    })
    
    const doc = new JSDOM(cleanHTML)
    const document = doc.window.document

    // Remove all not visible elements from parsing
    // Doesn't work becase axios download only the webpage excluding all the 
    // CSS coming from outside. We need to find a way to donwload external css
    // and aplly css rules inline

    // document.querySelectorAll('*').forEach((el) => {
    //   const style = doc.window.getComputedStyle(el)

    //   if (el.id === 'comments_body') {
    //     console.log('trovato!!!')
    //     console.log(style.display)
    //   }

    //   if (style.display === 'none') {
    //     el.remove()
    //   }
    // })

    const reader = new Readability(document)
    const article = reader.parse()

    const blocks = parseHTML(article.content)
    const meta = extractMeta(document)
    
    console.log(JSON.stringify({ blocks, raw: article, meta }))
  }).catch((e) => {
    console.error(e)
  })
} else if (args.length === 2 && URL_R.test(args[0]) && args[1].trim() === 'DEBUG') {
  const url = args[0]

  axios.get(url).then((response) => {
    const html = response.data

    // DOMPurify process on node require a DOM
    const _window = new JSDOM('').window
    const DOMPurify = createDOMPurify(_window)

    // Whole document with head for retrieve the title of the documnent
    const cleanHTML = DOMPurify.sanitize(html, {
      WHOLE_DOCUMENT: true,
      ADD_URI_SAFE_ATTR: ['property'],
      ADD_TAGS: ['head', 'meta'],
      ADD_ATTR: ['content', 'property'],
    })
    
    const doc = new JSDOM(cleanHTML)
    const document = doc.window.document

    // console.log(extractMeta(document))

    const reader = new Readability(document)
    const article = reader.parse()

    console.log(JSON.stringify(article))
  }).catch((e) => {
    console.error(e)
  })
}
