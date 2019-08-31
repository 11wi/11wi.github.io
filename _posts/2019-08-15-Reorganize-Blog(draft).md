---
category: 일상
---


# 무엇가 글로 쓰는 것의 의미

요즘 업무 시간을 따져보면 개발보다 문서화를 더 열심히 하고 있다. 게다가 친절한 글쓰기를 위해 한 번 쓰고 넘기지 않고
독자가 이해할 수 있을지 확인하고 수정하는 iteration이 시간 오래 걸린다.

그래도 이게 써놓고나면 나한테도 유용하고 누군가에게 설명할 때도 편리하다.
특히 요즘 기억력이 매우 떨어지고 있어서 한 달 전 코드를 보면 '과거의 내가 굉장히 똑똑했구나' 
감탄하며 가져다 쓰곤 한다.

한편으론 왜 글을 이렇게 밖에 못 썼을까 아쉬운 마음도 든다. 시간은 오래 걸리는데 생각만큼 퀄리티가 안 나온다.

그래도 글을 쓰는 이유는 결국 글을 잘 써야만 한다는 목표의식도 있고, 글을 쓰면서 
무형의 마음이 유형의 글로 정제되어 성장한다는 감각이 있기 때문이다. 
누구에게나 blog를 만들고 어떤 글이라도 올려보는 건 도움이 되는 활동일 것이다.  
  
요즘 드는 생각은 블로그에 일기처럼 짧은 일상 글을 쓰고 싶다. 
막상 혼자 보는 일기는 지속하기가 어렵고, 막 보여주긴 또 그러니까 누군가 보는듯 마는듯한 이 공간이 좋을 것 같다. 
그래서 이제 새로운 글에 알맞게 블로그를 개편해보려한다.

깔끔한 현재 레이아웃을 대체로 유지하되, 카테고리 구분이 쉬운 template로 교체해보자. 
그리고 댓글 기능도 고려했는데 역시 안 넣는게 좋을 것 같다. 
아직 관리 운영할 여력은 없는 것 같다. 
나중에 생각하면 추가하는 게 좋을듯.


## how-to

웹 개발에는 익숙치 않다보니 template 바꾸는 방법도 검색했지만 아주 친절한 문서는 찾지 못했다. 
~~그래서 초보도 따라할 수 있는 jekyll theme 변경법을 남겨본다.~~

그냥 template 파일을 덮어쓰니까 일단 작동은 한다... 거기에 몇가지 customize하면 충분할 것 같다.

1. [사이드바에 카테고리 구분 추가](#사이드바에-카테고리-구분-추가)
1. [폰트 변경](#폰트-변경)
1. [웹 최상단 icon 추가](#웹-최상단-icon-추가)


내가 쓰는 [theme](https://github.com/scotte/jekyll-clean)은 sidebar가 이미 구현되어 있다. 
살펴보면 그냥 `_includes/links-list.html` 을 보라는 뜻이다. 
```html
<div class="sidebar well">
{% include links-list.html %}
</div>
```

[이 분이 쓰신 글을](https://hoisharka.github.io/jekyll/2017/12/03/jekyll-category-001/) 참조하여 category를 화면에 뿌리는 것까지는 성공.
```html
-- _includes/links-list.html --
<h1>Category</h1>
<ul>

{% for category in site.categories %}
<li>
    <a href="{{ root_url }}/{{ site.category_dir }}#{{ category | first }}">
        <span class="name">{{ category | first }}</span> <span class="badge">{{ category | last | size }}</span>
    </a>
</li>
{% endfor %}

</ul>

```

![](images/blog-category-success.PNG)



이미지 크기가 post의 div 박스보다 더 크게 나오지 않도록 `theme.css`에 추가해주고
```css
img {
  max-width: 100%;
}
```

[블로그 글](https://seongkyun.github.io/others/2019/01/03/MathJax/) 따라 손쉽게 수식을 표현해주는 mathjax 기능을 넣었다.


code block의 이상한 coloring도 고쳐야지..