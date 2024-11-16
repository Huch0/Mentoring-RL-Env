from AppleGameEnv import AppleGameEnv

# 환경 생성
env = AppleGameEnv(m=36, n=36, max_steps=200)

# 환경 초기화
obs, info = env.reset()
print("초기 상태 (Observation):")
print(obs)
print("초기 정보 (Info):", info)

# Step 테스트
done = False
while not done:
    # 랜덤한 행동 생성 (테스트용)
    action = env.action_space.sample()  # 예: 랜덤 좌표
    print(f"Action: {action}")

    obs, reward, terminated, truncated, info = env.step(action)
    print("Observation:")
    print(obs)
    print("Reward:", reward)
    print("Terminated:", terminated)
    print("Truncated:", truncated)
    print("Info:", info)

    # 게임 종료 여부 확인
    done = terminated or truncated

print("게임 종료!")
