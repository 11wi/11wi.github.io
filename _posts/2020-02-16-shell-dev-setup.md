---
category: dev
---


# shell 환경세팅

요즘은 aws-shell, kube-prompt는 기본으로 띄워놓고 일하니까 
iterm의 화면 분할 기능을 안 쓸 수가 없다.  

재설치를 위해 핵심만 올리면

## installed

* zsh
* oh my zsh(zsh plugin)
* zsh-syntax-highlighting
* iterm

## config

### oh my zsh 덕분에 `.zshrc` 1 파일로 설정 제어.  

```
# PATH
# .bash_profile에서 export 문

# theme
ZSH_THEME="clean"

# conda
conda init zsh

# zsh-syntax-highlighting
source /usr/local/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
```

### iterm preference

`General - Preferences - Browse` 경로에서 [config](https://raw.githubusercontent.com/11wi/11wi.github.io/master/attachments/iterm/com.googlecode.iterm2.plist) load.
![](/attachments/iterm.png)