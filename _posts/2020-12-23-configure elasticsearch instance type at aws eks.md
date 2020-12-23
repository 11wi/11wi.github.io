---
published: false
category: dev
---
2020년에 kubernetes용 elasticsearch가 정식 출시됐다. eks에서 사용하기 때문에 어떤 ec2 instance가 적합한지를 조사했는데 암만 찾아도 좋은 가이드는 없다.
찾다못해 직접 판단 기준을 세워보았고 그 과정과 결과를 공유하려한다. (찾아서 안 나오는 걸 내가 글로 쓰는게 의미가 있지😎) 물론 나는 초보자이기 떄문에 이보다 좋은 접근법이 무조건 있을 것이다.

## gridsearch로 찾기

master, data, coordinating의 특징을 정리하며 인스턴스 후보를 골랐다.

* all: node 간 통신을 위해 네트워크는 빠를수록 좋다.
* master: 하는 일은 노드 관리뿐이라 자원은 필요치 않고 죽지 않는게 중요하다.
* data: 데이터 처리 task를 실행하므로 disk io가 높고, ram도 필요하고, aggregation과 sorting을 처리할 cpu도 중요하다.
* coordinating: data node의 결과를 취합하므로 aggregation과 sorting에 필요한 cpu 성능과 네트워크 속도가 중요하다.

후보는

* master: t3, i3, m5
* data: m5, r5
* coordinating: m5, c5

## 판단 기준

위에 조합을 대상으로 esrally를 돌려 나온 결과값을 비교한다.
다만 cluster 너무 크면 크게 부하를 줘야하니 작은 cluster로 실험한다.

성능도 괜찮고 가격이 싼 조합을 최종 초이스한다. (안정성은 실험이 어려워 배제)

## 개략적인 결론

esrally 성능지표중 term=phrase>aggregation>index 차례로 우선순위를 두고 가격 대비 성능을 판단했다 (스토리지 타입은 eks console에서 선택이 불가하므로 pass했다.)
이유는 es 용도가 logging이 아닌 search며 주요 task로는 match가 가장 크고 heavy aggregation도 상당수 있기 때문이다.

1. intel, amd 간 비교(e.g. m5, m5a)는 intel이 가성비 우위
2. master는 작은 사이즈여도 성능에 문제 없어 t3 타입도 충분할 수 있다.
3. data node는 r5보다 m5 타입이 좋다.
4. coordinating node는 m5보다 c5 타입이 가성비가 더 좋을 수 있다.

종합하면 가성비를 위해선 master: t3 or m5, data: m5, coordinating: c5로 구성하는 것이 좋을 것이다.

덧붙여 ebs 대신 ssd 사용을 고려했지만 [포럼](https://discuss.elastic.co/t/deploying-eck-on-aws-eks-with-i3-and-d2-instances-and-local-volumes/235223)을 보고 접었다.
