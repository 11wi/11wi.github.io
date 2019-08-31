---
category: data-science
---


회사 서버에서 돌리기 어려운 소스를 돌리고자
개인노트북 LG그램에 virtualbox 사용하여 ubuntu를 오랫만에 설치.
이전에 본 적이 없는 검은 화면만 뜨고 gnome 화면이 안 뜬다.
grub이라고 써있는 이 화면은 `help`말고 어떤 행동도 할 수 없게 만든다.

# grub
윈도우 부팅시 뜨는 검은 화면이랑 동일한 기능으로 보인다.
grub에서 부팅 방법은 [이렇게 해결.](https://www.linux.com/learn/how-rescue-non-booting-grub-2-linux)
update-grub 실행했지만 매번 끄고 다시 키면 동일한 상황이 발생하여
여러 솔루션을 찾았으나, 해결 실마리는 UEFI 부팅으로 추정.[링크](https://askubuntu.com/questions/1054006/pc-still-booting-on-gnu-grub-even-after-boot-repair)

# end
리눅스는 당연하게 생각했던 것을 하나하나 잡아줘야하다보니 생소한 느낌이 강하다.
지금까지 했듯이 구글링하면서 배우는 재미가 있는 게 참 다행이다.
고작 2년 전보다 노트북과 virtualbox가 정말 많이 좋아졌다는 게 체감된다.


 **+확실히 전에 써본 16버젼보다 18버젼이 쾌적하고 예쁘다. 16버젼에서
마우스 움직일 때마다 그래픽 깨짐 현상이 발생했는데 업데이트로 해결됨.**
++설치 instruction은 [여기서](https://www.linux.com/learn/how-rescue-non-booting-grub-2-linux)
