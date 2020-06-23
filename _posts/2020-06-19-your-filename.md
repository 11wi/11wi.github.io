---
published: false
---
[2020~현재] 검색/추천 서비스 플랫폼 개발 - aws eks poc 진행, 검색/추천 서비스 애플리케이션 개발을 위한 on prem 환경 k8s 구축
[2018~2019] digital transform 전략에 따른 business analysis (R/python) 및 data product 개발

---

[devops 영역]

- 업무 전환 배경 -
기존 서비스 운영 인력을 제외하면 신규 개발 인력이 전무한 상황에서 data product 개발 업무의 개발 역량을 인정 받아 analyst에서 engineer로 파트 이동.

1. 검색/추천 서비스 플랫폼 개발
차세대 프로젝트로 볼 수 있으며 주요 과제는
* k8s container app으로 전환
* 검색 서비스 elasticsearch(1.x -> 7.x)와 그에 따른 queryhandler 버전 업그레이드
* monolithic에서 micro service 형태로 애플리케이션 구조 변경
* 개인화 서비스를 위한 추천 시나리오, ranking 로직 개발
* 언어 변경 (java -> golang)

프로젝트 인원: analyst에서 engineer로 함께 변경한 3년차 2명.

1-1. aws eks poc 진행
* 검색/추천 서비스 구조에 따른 필요 aws 서비스 poc 진행 (ec2, eks, efs, alb, iam policy, route53, vpc)
* 회사 보안정책에 따른 iam policy, role 생성
* k8s cluster 구성을 위한 eksctl 작성
* 서비스 요건에 맞는 elasticsearch 구성(helm, efs, ebs) 및 load test (jmeter)
* troubleshooting

1-2. on prem k8s 구축
전사 과제로 cloud 이관 계획이 있어 aws에서 poc 진행했으나 비용 문제로 on premise에 k8s 환경 세팅 및 서비스 api 개발.

* kubeadm, kubespary 사용. 
* master node의 HA 구성.
* metallb - load balancer 구성
* csi, cni 구성
* istio ingress 사용
* zipkin, prometheus 등 관리도구 구성

* knative framework 사용
* grpc/rest api 개발
* cluster, application troubleshooting

[business analyst 영역]
여러 부서의 DT 과제 수행

1. 상품 사이즈별 재고 비율 최적화
사이즈가 민감한 상품(의류, 신발) 기획시 사이즈별 예상 수요와 비율을 책정하는데 필요한 예측 데이터 적재. 이를 현업에서 활용할 수 잇는 UI 제공.

2. tv 방송 판매 매출 예측 및 시뮬레이션
영업이익의 가장 큰 portion을 차지하는 tv 방송 판매를 데이터 기반 의사결정으로 전환하고자 내부 DB를 feature로 사용하여 예측 모델 생성. 현업이 모델에 변수를 대입하여 시뮬레이션할 수 있는 UI 개발.

3. 상품/고객 feature 발굴
mobile push 메시지 마케팅으로 활용할 수 있는 상품 메타 데이터 스크래핑 후 feature로 변환하여 마케팅 시행한 결과 CR/CTR 실적 향상을 확인함.

4. 쇼핑호스트 배정 최적화
최적화 이론을 현장에 반영하여 formula 구축. ibm cplex와 google ortools로 최적화 연산하여 내부 운영 시스템에 api 제공.