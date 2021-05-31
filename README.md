# Opal

**Opal.to** is a bookmarking service that enable to extend context of imported web article. The context extension is provided by two-way link system, blocks quotations and article annotations from other users.

https://opal.to/

### Project

The goal is to try to create a network of interconnected documents, inside a centralized platform. When a user import and read an article, can find on the sidebar  other articles linking to it, annotations on the article made by other users and links to the article (with surrounding context) in other notes not directly related to the article.

- Opal.to allow to import web articles. Article content is converted in *Markdown* format and the content is divided in *blocks*. ( Instapaper, Pocket and similar)
- When an article is imported, the extracted content is compared with the previous version (if present) and in case a new version is created. (GIT)
- Article are stored with a single unique URL. So, the article will always be available and all the quotation (or links) would not be broken in the future (Web Archive)
- User can read and annotate articles in private or public mode. (Medium, Roam)
  - Notes are *Markdown-blocks* formatted and are capable to embed tweet, videos, etc.
  - Notes are also capable of interconnecting with other documents using quotation and direct links.
- User can highlight articles portion and they will be saved. Future feature is to see the highlight on the article from other users in the community.

#### Related reading

- [Xanadu project by T.H. Nelson](https://www.xanadu.net/NOWMORETHANEVER/XuSum99.html)
- [Web original proposal](https://www.w3.org/History/1989/proposal.html)

![Imgur](https://imgur.com/iBOz5bf.png)
![Imgur](https://imgur.com/6bXtky8.png)
![Imgur](https://imgur.com/jl98SC8.png)

## Technology

React frontend tested with Chrome/Firefox/Safari, Python backend, Node.js service for fetching and processing web articles.

### Frontend
- React SSG - [Next.js](https://nextjs.org/)
- Markdown - [Unified.js](https://unifiedjs.com/)
- React Hooks data fatching and caching - [SWR](https://swr.vercel.app/)
- Styling - [styled-components](https://styled-components.com/)

### Backend
- Python Framework - [FastAPI](https://fastapi.tiangolo.com/)
- ORM - [SQLAlchemy](https://www.sqlalchemy.org/)

### Markdown Articles Service
- Node [node.js](https://nodejs.org/en/)
- Custom version of [Mozilla readability library](https://github.com/mozilla/readability)

### Database
- [PostgreSQL](https://www.postgresql.org/)

## Development

#### Frontend
```
npm install
npm run dev
```
Open `http://localhost:3000` in a browser

#### Backend
Setup the requirements in a virtual env
```
uvicorn app:app --reload --env-file .env
```
