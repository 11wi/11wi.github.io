---
category: data-science
---

# 데이터 사이언스 인강 완강하자 

수리통계적인 background를 보강하고자 인강을 찾아 3월에 신청했었는데
일도 바쁘고 몸도 아프고 해서 반절도 못 들었던 걸 이제 완강하려고 한다.
이렇게 글로 목표를 공언했으니 올해 안에는 마무리 해보려한다.

# endogeneity - 내생성

통계학 수업들으면서 계량경제학 수업도 들은 적이 있는데 굉장히 통계 수업하고 흡사했던 기억이 난다.
ML를 공부한다면 컴공, 통계, 수학을 떠올리나 계량경제가 applied science로서 어쩌면 더 좋은 궁합이 아닐까 싶다. 

많은 통계 모델이 uncorrelated error 전제로 하지만
endogeneity는 error와 독립변수 X가 독립이 아닌 경우를 말하며 
ML에서 본 용어는 아니지만 계량경제에서는 많이 보이는 문제다.
회귀분석의 경우 $$\epsilon \sim \mathcal{N}(0, \sigma)$$ 이나 
$$\epsilon \sim \mathcal{N}(X, \sigma)$$ 처럼 X값이 증가하면 residual가 증가한 경우를 예시로 생각할 수 있다.
이와 연관된 개념이 heteroscedasticity인데 수식으로 비교하면

$$ 
\begin{cases}
 endogeneity: E(e_i | x_i) = 0  \\
 heteroscedasticity: V(e_i | x_i) = \sigma
 \end{cases}
$$

endogenity는 first moment 문제이고 heteroscedasticity는 second moment 문제이다.
[endogenity 시뮬레이션](http://demonstrations.wolfram.com/EndogeneityBias/)

원인은 다양하게 설명이 있지만 결국 모델이 봤을때 X의 설명력이 부족해서 error로 떨어진 것이다. 
따라서 근본적인 솔루션은 feature를 보강하는 것이다.
새로운 feature를 발굴하던가 model로 feature를 만드는 등 feature engineering 고민이 필요하다.
(사실 이건 만병통치약 아닌가?..)