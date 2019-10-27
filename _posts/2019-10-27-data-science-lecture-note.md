---
category: data-science
---


# attenutaed bias - 과소 추정

단순 회귀 모형을 상정하여 $Y=\tilde{X}\beta_{1}$에서 $\tilde{X}=X+w$라고 하자.
true $X$를 기준으로 $\hat{\beta}$은 $\frac {\sigma_{x}} {\sigma_{x} + \sigma_{w}}$만큼 작은 값을 가지는 과소 추정 문제 발생. 
(수식은 길어서 생략. 정규방정식의 $X^\prime X$로 second moment 문제가 된다는 것만)

직관적으로 보면 아주 당연하다는 생각.

---

# simultaneity - 동시성

개념은 서로가 서로의 설명변수인 관계. (피자를 먹으면 콜라가 먹고 싶고, 콜라를 먹으면 피자를 먹고 싶은 그런 느낌)  
핵심은 현상을 더욱 잘 설명하는 omitted variable을 찾으라.
* 양말과 냉장고 판매량은 인과관계가 없을텐데, 상관계수가 높아서 그냥 쓰는 경우. 사실은 둘이 동시에 프로모션을 했다. (회사 분석계에도 이런 프로모션 피처가 있으면 좋겠다😟) 
* 초콜릿 소비량과 노벨상 수상자의 상관계수처럼 그냥 상관계수만 높은 경우.

---

# sampling

모수: parameter  
인데 sample 개수와 모수를 혼동하시는 분이 많아서 나까지 흔들리고 있다😅

sample bias를 피하려면 1. random sampling, 2. apple to apple  
A/B test를 예로 들면 접속 순서대로 A,B,A,B.. 배정하면 random OK, 그룹 간 동질성이 있다고 할 수 있으므로 apple to apple OK.

---

# t test

$$\frac{\bar{X_1} - \bar{X_2}} {\sqrt{ {(N_1-1) s_1^2 + (N_2-1) s_2^2} \over {N_1+N_2 -2} } \sqrt{\frac{1}{N_1}+ \frac{1}{N_2}}} $$

t 검정 수식의 분모에 집중해 보자. 

1. pooled variance건 unpooled건 결국 분산의 합이다.
    * $V(\bar{X_1}) + V(\bar{X_2})$ 과 똑같다. 
1. balanced일수록 error가 적다.
    * $N_1=N_2$일 때 $\sqrt{\frac{1}{N_1}+ \frac{1}{N_2}}$가, 그리고 검정 에러가 최소화된다. A/B test에서 balanced sample size를 하는 이유가 여기있다!

---

📓이번주는 수리통계가 안 나와서 수월했다. 나쁜 추정에 대한 개념을 통해 내가 했던 지난 실수들을 새로운 맥락에서 볼 수 있는 것이 오늘의 성과.  