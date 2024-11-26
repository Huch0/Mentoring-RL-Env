# 나만의 강화학습 환경 만들기

OpenAI Gymnasium 라이브러리를 활용하여 커스텀 강화학습 환경을 만들어보는 프로젝트입니다.

목표 :

- 강화학습의 기본 개념 이해
- Gymnasium 기반 강화학습 환경 만들기
- StableBaselines3 를 활용하여 Deep Reinforcement Learning(DRL) agent를 해당 환경에서 학습하기

부산대 정보의생명공학대학 “멘토멘티 멘토링 프로그램”의 일환으로 진행되었습니다.
[https://justicementoring.site/introduce](https://justicementoring.site/introduce)

## 목차

- [나만의 강화학습 환경 만들기](#나만의-강화학습-환경-만들기)
  - [목차](#목차)
  - [요구사항](#요구사항)
  - [설치방법](#설치방법)
  - [프로젝트 구조](#프로젝트-구조)
    - [`/Algorithms`](#algorithms)
    - [`/AppleGameEnv`](#applegameenv)
    - [`/examples`](#examples)
  - [Reference](#reference)
  - [License](#license)

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

## 프로젝트 구조

### `/Algorithms`

강화학습 알고리즘들을 구현하고, 간단한 Grid World 환경에서 동작하는 모습을 시각화한 프로젝트입니다. `GridWorld.py`는 간단한 Grid World 환경을 제공하는 모듈이고, `RLAlgorithms.py`는 강화학습 알고리즘들을 구현한 모듈입니다. 구현한 알고리즘에는 Policy Iteration (DP)이 포함됩니다. `UI.py`는 pygame 라이브러리로 제작한 UI로, 사용자가 알고리즘과 에이전트와 상호작용할 수 있습니다. 이 프로젝트를 실행하는 main script는 다음과 같이 실행할 수 있습니다:

구현된 알고리즘:

- Policy Iteration (DP)
- Value Iteration (DP)
- ~~TD Learning~~
- ~~Monte Carlo Evaluation~~
- ~~SARSA($\lambda$)~~
- ~~Q-Learning~~

```bash
# Root 디렉토리에서 실행
python Algorithms/main.py

# Algorithms 디렉토리에서 실행
python main.py
```

### `/AppleGameEnv`

[사과 게임](https://en.gamesaien.com/game/fruit_box/)을 Gymnasium 환경으로 구현한 프로젝트입니다. `AppleGame.py`는 사과 게임의 내부 로직을 담당하는 모듈이고, `AppleGameEnv.py`는 사과 게임을 Gymnasium 환경으로 구현한 모듈입니다. StableBaselines3 에이전트가 이 환경에서 학습할 수 있습니다. `train.ipynb`는 StableBaselines3의 에이전트를 `AppleGameEnv` 환경에서 학습하는 script입니다. 사용자가 사과 게임을 직접 플레이할 수 있는 main script는 `main.py`로, 다음과 같이 실행할 수 있습니다:

```bash
# Root 디렉토리에서 실행
python AppleGameEnv/main.py

# AppleGameEnv 디렉토리에서 실행
python main.py
```

### `/examples`

Gymnasium과 StableBaselines3 라이브러리를 학습하기 위한 예제 코드들이 포함되어 있습니다.

## Reference

- Gymnasium: [https://gymnasium.farama.org/](https://gymnasium.farama.org/)
- StableBaselines3: [https://stable-baselines3.readthedocs.io/en/master/](https://stable-baselines3.readthedocs.io/en/master/)
- StableBaselines3 예제코드: [https://github.com/Stable-Baselines-Team/rl-colab-notebooks](https://github.com/Stable-Baselines-Team/rl-colab-notebooks)

## License

- MIT
