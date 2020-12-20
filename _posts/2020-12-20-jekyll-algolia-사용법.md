---
published: false
category: dev
---
"jekyll algolia 사용법"을 검색해보면 minima theme에 `_config.yaml`을 수정하는 방법만 나와서
내부적으로 어떻게 돌아가는지 찾아본 결과를 공유한다.
(드디어 묵은 숙제를 건드렸다😎)

## algolia 실행 구조

algolia 검색 API는 data indexing, API call 두 가지로 파악할 수 있다. 사실 [이거](https://github.com/algolia/jekyll-algolia)와 [저거](https://github.com/algolia/jekyll-algolia-example)만 보면 충분하다.


### indexing

`bundle exec jekyll algolia`를 실행하면 `_post`의 data가 `_config.yaml`에 세팅된 algolia endpoint로 전송된다.
github blog 사용자는 이 커맨드를 ci 과정에서 (travis CI) 실행한다.

### API call

[여기](https://community.algolia.com/jekyll-algolia/blog.html) 설명이 있는데 쉽게 말하면 `_includes/algolia.html` 파일에 호출 코드를 심어 놓고 검색이 들어갈 div 태그의 id 값으로 호출 코드를 불러온다. `<div id="search-searchbar"></div>`와 ` <div id="search-hits">`가 그 값이다. 여기서도 `_config.yaml`를 통해 algolia endpoint를 찾는다.