"use strict";

var _Readability = _interopRequireDefault(require("./Readability"));

var _axios = _interopRequireDefault(require("axios"));

var _jsdom = require("jsdom");

var _dompurify = _interopRequireDefault(require("dompurify"));

var _unified = _interopRequireDefault(require("unified"));

var _rehypeParse = _interopRequireDefault(require("rehype-parse"));

var _hastUtilSanitize = _interopRequireDefault(require("hast-util-sanitize"));

var _hastUtilToMdast = _interopRequireDefault(require("hast-util-to-mdast"));

var _mdastUtilToMarkdown = _interopRequireDefault(require("mdast-util-to-markdown"));

var _mdastUtilGfmTable = _interopRequireDefault(require("mdast-util-gfm-table"));

var _unistUtilVisitParents = _interopRequireDefault(require("unist-util-visit-parents"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && Symbol.iterator in Object(iter)) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

var URL_R = /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/;
var BLOCK_TYPES = ['paragraph', 'blockquote', 'heading', 'code', 'table'];
var META_PROPERTIES = ['og:title', 'og:description', 'og:locale', 'og:type', 'og:url', 'og:image', 'article:tag'];
var args = process.argv.slice(2);

function extractMeta(document) {
  var properties = {};
  META_PROPERTIES.forEach(function (prop) {
    var metas = document.head.querySelectorAll("[property=\"".concat(prop, "\"][content]"));
    var name = prop.split(':')[1];

    if (metas && metas.length > 0) {
      if (metas.length > 1) {
        properties[name] = _toConsumableArray(metas).map(function (el) {
          return el.content;
        });
      } else {
        properties[name] = metas[0].content;
      }
    }
  });
  return properties;
}

function parseHTML(html) {
  var hast = (0, _unified["default"])().use(_rehypeParse["default"]).use(_hastUtilSanitize["default"]).parse(html);
  var mdast = (0, _hastUtilToMdast["default"])(hast);
  var blocks = [];
  var count = 0;
  (0, _unistUtilVisitParents["default"])(mdast, BLOCK_TYPES, function (node, ancestors) {
    var last = ancestors[ancestors.length - 1];
    var list = null;
    var indent = 0;
    var properties = {};
    var links = [];

    if (node.hasOwnProperty('position')) {
      delete node['position'];
    }

    var isList = last && last.type === 'listItem';

    if (isList) {
      // Count list intentation
      var listIndent = ancestors.filter(function (a) {
        return a.type === 'listItem';
      }).length - 1;
      indent = listIndent;
    }

    properties['raw'] = (0, _mdastUtilToMarkdown["default"])(node, {
      extensions: [_mdastUtilGfmTable["default"].toMarkdown()]
    });
    (0, _unistUtilVisitParents["default"])(node, null, function (childNode) {
      if (childNode.type === 'link') {
        links.push(childNode.url);
      }
    });

    if (links.length > 0) {
      properties['links'] = links;
    }

    blocks.push(_objectSpread(_objectSpread({}, node), {}, {
      type: node.type,
      position: count,
      indent: indent,
      list: list,
      properties: properties
    }));
    count += 1;
  });
  return blocks;
}

if (args.length === 1 && URL_R.test(args[0])) {
  var url = args[0];

  _axios["default"].get(url).then(function (response) {
    var html = response.data; // DOMPurify process on node require a DOM

    var _window = new _jsdom.JSDOM('').window;
    var DOMPurify = (0, _dompurify["default"])(_window); // Whole document with head for retrieve the title of the documnent

    var cleanHTML = DOMPurify.sanitize(html, {
      WHOLE_DOCUMENT: true,
      ADD_URI_SAFE_ATTR: ['property'],
      ADD_TAGS: ['head', 'meta'],
      ADD_ATTR: ['content', 'property']
    });
    var doc = new _jsdom.JSDOM(cleanHTML);
    var document = doc.window.document; // Remove all not visible elements from parsing
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

    var reader = new _Readability["default"](document);
    var article = reader.parse();
    var blocks = parseHTML(article.content);
    var meta = extractMeta(document);
    console.log(JSON.stringify({
      blocks: blocks,
      raw: article,
      meta: meta
    }));
  })["catch"](function (e) {
    console.error(e);
  });
} else if (args.length === 2 && URL_R.test(args[0]) && args[1].trim() === 'DEBUG') {
  var _url = args[0];

  _axios["default"].get(_url).then(function (response) {
    var html = response.data; // DOMPurify process on node require a DOM

    var _window = new _jsdom.JSDOM('').window;
    var DOMPurify = (0, _dompurify["default"])(_window); // Whole document with head for retrieve the title of the documnent

    var cleanHTML = DOMPurify.sanitize(html, {
      WHOLE_DOCUMENT: true,
      ADD_URI_SAFE_ATTR: ['property'],
      ADD_TAGS: ['head', 'meta'],
      ADD_ATTR: ['content', 'property']
    });
    var doc = new _jsdom.JSDOM(cleanHTML);
    var document = doc.window.document; // console.log(extractMeta(document))

    var reader = new _Readability["default"](document);
    var article = reader.parse();
    console.log(JSON.stringify(article));
  })["catch"](function (e) {
    console.error(e);
  });
}