---
category: dev
---

search service application architecture를 very seriously하게 study 하다보니 english가 편안할 지경이다.
아무나 내 고민좀 들어줬으면 좋겠다.

---

요구사항은 1. cloud 환경일 것이다..? 2. kubernetes 환경 3. dynamic하게 code 수정 가능 
4. 아직은 검색만 하지만 향후 추천 서비스도 가능하도록 확장성 있게 (?) 5. dynamic하게 api 생성/삭제/수정 (?)

앞으로 elasticsearch 기반 추천 시스템을 상상하면서 검색과 추천 서비스를 한 묶음으로 갈 예정인가보다.

---

처음 개발을 시작했을땐 요구사항 1~3만 알고 있었기 때문에 cloud를 잘 쓰는 법에만 관심이 있었다.
약 1달 간 aws를 겪으며 애플리케이션이 들어갈 환경 구성을 성공적으로 마무리했다 😙
그런데 요금통지서 쌔게 맞았다고 혼나고 다 삭제하니 남은건 yaml 파일 몇개 뿐이더라...

---

그리고 애플리케이션을 고민한다. 일단 rest api가 뭔지부터 또 구글링을 엄청 한다.
그 와중에 golang으로 api 만드는게 아주 좋아보였다. 
나랑 같이 일하는 사람이 사실상 1명이다보니 빠르게 go를 공부해가며 개발 착수했다.

가장 기본이 되는 elasticsearch 조회, redis 조회 모듈부터 만들었다.
슬슬 go convention이라던가, 패키지 구조라던가, 디자인 패턴을 알아서 찾게 된다.

---

이제 api스럽게 web framework를 입힌다. 처음에 [go-gin](https://github.com/gin-gonic/gin)을, 
나중엔 [fasthttp](https://github.com/valyala/fasthttp)와 [fiber](https://github.com/gofiber/fiber)를 썼다.
설계도에 api 게이트웨이를 추가한다.
점점 latency를 생각하고 네트워크를 고려한다... 점점 답이 없다는 인상을 받는다.

---

요구사항 4~5번을 알게 됐다.. dynamic하게 config, source code 수정을 어떻게 하면 좋을지 구글링하다가
이젠 뭔가 신기술 없는지 마구잡이로 찾는다. 

[go-micro](https://micro.mu/)를 보니 msa가 분명 장점은 있는 것 같은데
비즈니스 환경은 모놀리식이 어울리는 것 같기도 하고... 어차피 프론트쪽에서 rpc 통신 못하니까 평범하게 갈까 생각도 든다.
그제야 깨달은건 api와 web은 좀 다르다는 것..;;

---

[knative](https://knative.dev/)를 발견한다. 역시 서버리스가 대세지.
여기에 ingress로는 [gloo](https://docs.solo.io/gloo/latest/)를 더하면 그림이 괜찮아보인다. 
그런데 현실적으로 회사에서 컨테이너 기반으로 개발하는 사람이 거의 없기 때문에 (근데 왜 k8s 환경으로....🙄?) 쉬운 방법이 낫겠지..
[kubeless](https://kubeless.io/)는 code 올리고 커맨드만 돌리면 api가 뜨니까 엄청 간편해보인다.
아직까지는 `kubeless`가 제일 적당한 것 같다!!

---

2월부터 3달동안 정말 많이 공부했지만 사실 cloud 환경 DevOps가 정착된 회사라면 보면서 금방 따라할 수 있는 정도인 것 같다.
이번에 피부로 따갑도록 느낀건, 내가 주어진 일을 열심히 하려해도 회사에서 최소한의 서포트도 없으니 정말 영혼 없이 회사 다니게 되더라.
(다시 한번 느끼지만 데이터 과학을 제대로 하려면 it 베이스 회사로 가야한다.😕)
가장 안타까운건 제일 큰 경력이 하필 서비스 개발이란게 나중엔 어떨지 몰라도 지금은 그리 만족스럽지 않다......
