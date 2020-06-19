---
published: true
category: dev
---
한창 k8s cluster와 elasticsearch, queryhandler를 정비하고 있다.
대충 그림은 다 나왔고 이제 detail을 챙기면서 chaos test와 tps 측정을 거치면 끝날 것 같다.
ingress로 istio를 쓰면서 나쁜 것 같진 않은데 k8s 기본 ingress와 참 달라서 힘들고, 인지도 대비 참조 문서량이 적다. 돌아보면 nginx가 제일 편하고 초보자 문서가 많다.

지금의 최고 난이도 문제는 request 100회를 날리면 대부분 http 200이지만 502가 10개 정도 뜬다는 것이다.
근데 이게 뭐땀시 저런지 도통 감이 없다..🙄

아무튼 istio endpoint로 1개 vip를 쓰고 있고, 사정상... 모든 api와 관리 ui도 여기에 싹 우겨넣었다. 
그러나 https를 요구하는 kubernetes dashboard는 쉽게 세팅되지 않았다. 암만 구글링해도 속 시원한 답은 없다. 그래서 내가 검색 문서를 만들어야지 안되겠다.

---

## kubernetes dashboard with istio ingressgateway - expose https & http both (tls passthrough and http redirected)

### expected behavior

with istio ingressgateway, can access https://dashboard.com and http://dashboard.com

### version
* istio-1.6.3
* official k8s dashboard-2.0.1

#### what todo

1. set custom certs in your dashboard deployment not occuring browser error with your domain https://github.com/kubernetes/dashboard/blob/v2.0.1/docs/user/certificate-management.md
2. istio gateway with `httpsRedirect: true` and `mode: PASSTHROUGH` [ref](https://istio.io/latest/docs/reference/config/networking/gateway/)

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: my-gateway
  namespace: some-config-namespace
spec:
  selector:
    app: my-gateway-controller
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - dashboard.com
    tls:
      httpsRedirect: true # sends 301 redirect for http requests
  - port:
      number: 443
      name: https
      protocol: HTTPS
    hosts:
    - dashboard.com
    tls:
      mode: PASSTHROUGH
```

3. istio virtualservice with `http` and `tls`


```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: some-route
spec:
  hosts:
  - dashboard.com
  http:
  - name: "foo"
    match:
    - uri:
        prefix: "/"
    route:
    - destination:
        host: <dashboard>
  tls:
  - match:
      sniHosts:
      - dashboard.com
    route:
    - destination:
        host: <dashboard>
```


it works perfect for me. test it using `curl -k -v`. you can see status code 200 for https, 301 for http.