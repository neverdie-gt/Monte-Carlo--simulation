#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
def random_spin_field(N,M):
    return np.random.choice([-1,1], size=(N,M))
random_spin_field(10,10)
# 랜덤으로 스핀의 방향에 따라 1,-1이 선택되는 행렬을 만드는 함수를 지정한다.

from PIL import Image

def display_spin_field(field):
    return Image.fromarray(np.uint8((field+1)*0.5*255)) #0 ... 255
display_spin_field(random_spin_field(200,200))
# 위의 행렬을 가시화해서 보여줄수 있도록 해주는 위젯인 pillow를 불러오고 바꿔주는 함수를 정의한다.

def ising_step(field, beta=0.4):#여기서 beta는 1/Kb*T을 의미한다.
    N, M=field.shape
    for n_offset in range(2):
        for m_offset in range(2):
            for n in range(n_offset, N, 2):
                for m in range(m_offset, M, 2):
                    _ising_update(field, n, m, beta)
    return field
# (N,M) 행렬을 쭉 도는데 순서대로 도는것이 아니라 랜덤적으로 선택하기위해 offset요소를 넣어서 for문을 만든다.
# 이부분이 스핀을 조정하는 칸을 선택하는 부

def _ising_update(field, n, m, beta):
    total=0
    N, M = field.shape
    for i in range(n-1, n+2):
        for j in range(m-1, m+2):
            if i == n and j == m:
                continue
            total += field[i % N, j % M]
    dE = field[n, m]*total
    if dE <= 0:
        field[n, m] *= -1
    elif np.exp(-dE * beta) > np.random.rand():
        field[n, m] *= -1

#몬테 카를로 시뮬레이션 방법으로 metropolis algorithm을 사용하여 선택한 부분의 주변의 스핀을 전부 더하고 자신의 스핀과 곱한 값을 dE로 놓자.
#그리고 dE가 0보다 작거나, 같다면 현재 스핀에 -1을 곱하여 스핀을 바꿔주고, 만약 그렇지 않은 경우에서도 확률 exp(-dE * beta)에 해당한다면 역시
#자신의 스핀에 -1 을 곱하여 스핀을 바꿔준다.

from ipywidgets import interact

def display_ising_sequence(image):
    def _show(frame=(0, len(images)-1)):
        return display_spin_field(images[frame])
    return interact(_show)

#파이썬에서 제공하는 위젯에서 ipywidgets에서 interact를 불어온다.
#그리고 위에서 정의한 함수들이 여러 이미지로 연속적으로 나타날수 있도록 위젯함수를 정의해준다.

images = [random_spin_field(200,200)]
for i in range(50):
    images.append(ising_step(images[-1].copy()))
display_ising_sequence(images)

#마침내 우리가 만들 2D의 사이즈를 결정하여 {(200,200)으로 하였다.} 위엣 설정한 위젯함수를 50번 진행하도록 돌리면 순서대로 드래그하여 
#아이징 모델이 변화하는것을 볼수 있다.


# In[ ]:




