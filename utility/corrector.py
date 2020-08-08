import numpy as np

'''
qual을 넘어가면 전부 같은 값으로 취급되어야 함
max가 1을 넘지는 않게
min이 0보다 작지는 않게
rank correlation이 1
'''


def create_circle_corrector(qual):
    def corrector(x):
        return np.sqrt(qual ** 2 - (qual - np.minimum(x.astype(float), qual)) ** 2) / qual

    return corrector


def create_one_corrector():
    def corrector(x):
        return np.ones(x.shape)

    return corrector


def create_wrong_corrector():
    def corrector(x):
        return np.random.random(x.shape)

    return corrector


def create_sigmoid_corrector(qual=502):
    def corrector(x):
        if x >= qual:
            return 1
        else:
            return 1/(1 + np.exp((-x+200)/50))

    return corrector


def create_sigmoid_2_corrector(qual):
    def corrector(x):
        return 1/(1+ np.exp((0.8*qual-x) / (0.1*qual))) # 0.6으로 바꿔서 다시 해보기!!!

    return corrector


if __name__ == '__main__':
    x = np.arange(100)
    x = create_wrong_corrector()(x)
    assert(min(x) >= 0)
    assert(max(x) <= 1)

    for i in range(len(x) - 1):
        assert(x[i] <= x[i + 1])

    print('SUCCESS')
