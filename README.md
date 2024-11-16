# 나만의 강화학습 환경 만들기

OpenAI Gymnasium 라이브러리를 활용하여 커스텀 강화학습 환경을 만들어보는 프로젝트입니다.

목표 :

- 강화학습의 기본 개념 이해
- Gymnasium 기반 강화학습 환경 만들기
- StableBaselines3 를 활용하여 Deep Reinforcement Learning(DRL) agent를 해당 환경에서 학습하기

부산대 정보의생명공학대학 “멘토멘티 멘토링 프로그램”의 일환으로 진행되었습니다.
[https://justicementoring.site/introduce](https://justicementoring.site/introduce)

## 요구사항

- requirements.txt 참조

Windows 유저는 WSL2 환경에서 실행하는 것을 권장합니다.

- [WSL2 + Windows Terminal + Oh My Zsh + Powerlevel10k 설정 방법](https://gist.github.com/zachrank/fc71ed301e9823264ddac4fb77975735)

- [Homebrew 설치](https://brew.sh)

## 설치방법

- 파이썬 가상환경 설정

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

- 패키지 설치

    ```bash
    brew install swig
    pip install -r requirements.txt
    ```

- ffmpeg 설치 (Optional)

    ```bash
    brew install ffmpeg
    ```

  - moviepy 라이브러리를 활용하여 동영상을 생성할 때 필요합니다.

## Reference

- Gymnasium: [https://gymnasium.farama.org/](https://gymnasium.farama.org/)
- StableBaselines3: [https://stable-baselines3.readthedocs.io/en/master/](https://stable-baselines3.readthedocs.io/en/master/)

## License

- MIT
