---
category: data-science
---


# function
## non linear 함수를 찾는 법
대부분의 data가 non linear function으로 fitting 잘된다는 사실은 자명하다.
이 function을 찾기 위해 미적분 개념이 필요하다.
taylors expansion은 어떤 함수 $f(x)$를 미분할 줄 안다면 근사식을 구할 수 있음을 보여준다.

$sin(x)=x-\frac{x^3}{3!}+\frac{x^5}{5!}-\frac{x^7}{7!}+\cdots $  

$e^x=1+x+\frac{x^2}{2!}+\frac{x^3}{3!}+\frac{x^4}{4!}+\cdots $

$f(x+h) = f(x) + f' (x)h + f'' (x)\frac{h^2}{2!} + f''' (x)\frac{h^3}{3!} $

이렇게 만든 근사식은 오차값이 존재한다.
하지만 modeling 자체가 현실을 function 형태로 유추하는 것이기에 오차값 유무보다는 
data pattern을 잘 표현하는 function을 선택했는지에 더 관심을 가지는 게 맞다.