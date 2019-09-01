# markdown 안에 jinja2 코드 넣기

jekyll, flask를 보면 이런 식으로 생긴 코드가 있는데 jinja2 문법이라고 알고 있다. 

```liquid
{%raw%}
{% if site.mathjax %}
{%endraw%}
```

이거를 그대로 markdown code block으로 넣으면 신기하게 rendering된 상태로 나온다는 걸 알았다.
이를 소스 코드 그대로 보여주는 법은 어떻게 검색어를 넣어야할지 감이 잘 안와서 다른 사람 blog에서 가져왔다.
저처럼 검색어가 잘 안 떠오르시는 분들에게 도움이 되길 바란다. 
 
![](/attachments/markdown-liquid.png)

편의상 그림으로 코드를 올린다.
`%raw%`를 써야만 저 코드가 실행되지 않는 것으로 보인다.
신기하게도 저 `%raw%`라는 코드는 텍스트로 표기가 불가능한 것 같다.
여러모로 해봐도 사라진다.  

그리고 `liquid`라는 언어를 지정해주면 컬러링이 된다. 이 또한 새롭게 알게된 사실이었고 pycharm에선 아직 liquid는 auto completion에 없다.
 