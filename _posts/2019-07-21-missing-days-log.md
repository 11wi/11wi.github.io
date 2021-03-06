---
category: data-science
---



# 현실의 데이터 사이언스는 아름답지 않았다.

## 다시 포스트를 올린 계기

거의 1년 간 블로그를 잊고 있던 와중에 낯선 메일을 받았다. 
데이터 분석을 지망한다는 취업 준비생의 질문을 받았는데... 가장 먼저 부끄러움을 느꼈다. 
초심을 완벽히 잊고 있었음을 반성하게 됐다.  

지난 9개월을 변명하자면 굉장히 심신이 힘들었다. 현실의 데이터 분석은 
전혀 멋지지 않고 교실에서 배운 거랑은 매핑이 안된다. 
지금 느끼는 생생한 경험을 글로 남겨보려 한다.

## 그동안의 경험들 - 데이터 과학의 현실

_(지극히 특수한 케이스일 수 있음)_  
올해 일어난 큰 변화는 소속팀의 존재 이유는 **현업의 문제를 푸는 것**으로 정의된 것이다.
그리하여 

1. 오직 현업 요청 프로젝트만 진행
1. 2년차일지라도 사수 없이 프로젝트 담당

이 사소한 변화가 내게 현실을 알려줄 거라곤 생각 못했다.
몇가지 주요 챌린지만 쓰자면

1. 일단 일 요청이 많다. (현업 몇백 명)
1. 영업부서 과장급~팀장급 카운터 파트의 요청 (직급 차이)
1. 커뮤니케이션 (그들은 데이터를 모르고, 나는 영업을 모른다) 
1. 고객이 이해하기 쉬운 언어로 (only 쉬운 알고리즘, 로직보단 스토리)
1. 현업은 빠른 결과를 원한다 (야근)
1. 데이터를 활용해서 뭔가 했다고 보고해야 한다 (성과압박, 포장)
1. 고객님은 데이터에서 뭔가가 근사한게 나오길 원한다. (데이터는 only 운영데이터인데도) 

이외에도 이런저런 챌린지가 많아 스트레스가 엄청났었고 오늘만 잘 넘기기를 기도하고 다녔다.
(그 와중에도 고객님이 예쁘게 봐주셔서 인정은 받고 다녔다.)
이러한 어려움은 데이터 분석가로서 피할 수 없는 숙명이기도 하다는 것을 알리고 싶다.   

### 왜 이렇게 힘들고 어려울까?

#### 데이터 분석가는 현업이 아니지만 현업과 가까워야 한다.

데이터가 필요한 이유는 (1) 데이터 기반 의사결정, (2) 데이터 기반 서비스 2가지 이다.
이 2가지 아닌 방법으로 돈 벌고 있는 회사는 없는 것 같다.
결국 데이터가 실질적으로 활용되는 곳은 영업 현장이다.
분석가는 현업과 밀접하게 일해야되는 것이 맞다.   

그렇다면 데이터 분석가를 현장 중심으로 정의하면 이렇다. 
1. 컨설턴트와 유사한 포지션으로 사내에 들어와 
1. 데이터 기반 솔루션을 만들고 
1. 연관 부서에 sales하는 role에 가깝다. 

##### 예시: 추천서비스

sales라는 단어를 설명하기 위해 영업 부서의 추천 서비스를 예로 들어보자.
기존에도 잘 굴러가고 있는데 영업 한 번 해본 적도 없는 데이터 분석가가 와서 이래라 저래라 하면 당연히 신뢰가 가지 않는다.  
게다가 분석가는 처음부터 좋은 결과를 내놓기 매우 어렵다. 수차례의 trial-error를 겪으면서 더 좋아진다. 
그런데 영업 담당자는 당장의 실적이 문제다.
분석가의 실수는 본인의 실적 마이너스가 되버리니 구조적으로 협업이 어려울 수 밖에 없다.
담당자를 설득하지 못하면 분석가는 추천 모델을 테스트하는 기회조차 없을 수 있다.   
 

##### 예시: 데이터 기반 의사결정

데이터 기반 의사결정은 정말로 현업을 알아야만 한다.
의사결정은 '우리는 뭘 해야하나요?' 라는 질문에 답을 주는 것이다.
현업이 중요하게 생각하는 지표가 무엇인지, 그리고 할 수 있는 action이 무엇인지부터 알아야만
우리는 질문에 답할 수 있다.
실적을 높이기 위한 예측 모델에 현업이 컨트롤 할 수 없는 변수만 넣는다면?  
또는 예측 모델의 y값이 전혀 현업에게 중요하지 않다면?    


#### 분석가가 사용할 데이터도 문제다.

데이터를 확보하기 위해 오래 전부터 기획 - 생산 - 점검의 단계를 거쳐온 넷플릭스와 같은 회사와는 달리 
대부분의 회사는 기존에 가지고 있는 운영데이터 외에는 가치 있는 데이터가 소수다.
당연히 garbage in - garbage out이다. 좋은 데이터가 없는데 성과가 나오기 어렵다.  

데이터 공부 해봤다 하는 사람은 data cleaning이 중요하다고 들었겠지만 보다 더 큰 문제는 data sourcing, 데이터를 가져오는 것 그 자체다. 
뭐가 어디에 있는지, 이 데이터를 받을 수 있는 환경이 어디인지부터 확인하는 작업부터 쉽지 않다.


### 한탄

그냥 회사 차원에서 지원을 해줬으면 하는 경우도 있다.
내가 열심히 만든 데이터가 의미 없이 버려진다고 느낄 때도 있고  
자원이 부족해 한정된 자원 안에서 알고리즘을 scale down(up, out이 아니다)해서 작업하기도 한다.   
개인적으로 올 상반기는 내가 이 회사에서 의미있는 프로젝트를 하며 발전하고 있다는 느낌이 들지 않는 해였다. 


### 데이터 사이언스를 지향한다면
 
일단 SKT, 네이버 등 top tier 회사를 가야한다. 
왜냐하면 그래야 최소한 분석 환경에 대한 스트레스라도 안 받는다. (과제 시작하면 나는 맨날 분석 환경 걱정부터 한다)
쓸 수 있는 데이터도 많을 것이고 함께 일하는 동료나 다른 팀과 커뮤니케이션도 고통스럽지 않을 것이다.
전반적으로 데이터 문화가 어느 정도 수준에 올라야 한다. 특히 데이터가 직접적으로 매출에 크게 기여하면 좋다.  
왓챠와 같은 데이터에 뿌리를 둔 스타트업은 여기에 해당하지 않을까?  

데이터 사이언스 지망은 의미 없는 일, 비전도 없는 일을 특히나 싫어할 것이라고 생각한다. 
오래된 non IT 기업에서 데이터 분석가로 일한다면 십중팔구 싫어하는 것들을 많이 만날 것이라고 감히 예견한다.


## 지금은

살 만하다. 사회생활을 조금 더 알아가는 거라고 생각한다.
오늘 글을 쓰면서 더욱 정리가 된 느낌이 든다. 
이제 막 주어진 환경에서 나의 발전에 도움이 될 무엇을 향해 가고 있다.  
최근 공부한 게 있는데 이 곳에 공유할 계획이다.  

그리고 최우선은 언제나 심신건강이다. 
