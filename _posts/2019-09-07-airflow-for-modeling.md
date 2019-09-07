---
category: data-science
---


# airflow in data science


찾아보면 airflow 글이 참 많다. data engineering 측면에서 굉장히 인기 있는 것 같다. 
사실 deep하게 써보지는 않았지만 내 입장에선 왜 인기가 있는지 잘 모르겠다.
기존에 써본 oozie 보다는 분명 기능적으로 좋은 부분이 있다.

data scientist 입장에서 보면 airflow가 data product을 만들기에 가장 적합해보인다.
query -> data process -> model -> deploy(는 mlflow겠지만) 과정을 하나의 python tool로 할 수 있는게 장점 같다.
하지만 이게 그렇게 좋냐고 물어보면 그렇게 좋은지는 잘 모르겠다.
추측이지만 진짜 data를 많이, 다양하게 활용하는 기업에서는 좋을 수 있겠다는 생각은 있다.


개인적으로 airflow를 써보며 얻은 건 dag 개념, 그로 인해 source code 품질이 상당히 좋아졌다는 점이다.

dag라는 걸 이해하기가 어려웠는데 이를 도와준게 [cookiecutter](https://github.com/drivendata/cookiecutter-data-science) 였다.
이 덕분에 기존에 마구잡이로 개발하던 습관을 전부 뜯어고치고 뭐든 구조화하는 개념에 익숙해진 것 같다. 

airflow는 debugging이 어렵다. 그래서 단순 code error가 발생하지 않게 먼저 꼼꼼히 개발하는게 필요한 것 같다.
이 때 필요한 건 내가 짠 코드는 틀릴 것이라고 생각하는 것. 
대부분 코드를 짜다보면 잘 되겠거니 믿고 넘어가는 부분이 생긴다.
그 믿음을 버려야된다. `assert` 같은 censor로 확인해야된다.

dag를 만들기 위해 code를 task 단위로 나누자고 마음 먹으면 처음엔 막막하다.
내가 무슨 기능을 만들었는지 기억도 잘 안나서 dependency가 있는 code를 나눠버리기도 한다.
하다보면 나중엔 한 눈에 보인다. module 단위로 기능이 잘 묶여 있어서 기억하기도 쉽다. 
구조화가 더욱 정교해져서 code 재사용 가능해지게 된다.
unittest도 가능해져서 더욱 code에 믿음이 간다.
