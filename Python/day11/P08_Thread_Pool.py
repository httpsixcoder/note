"""
    该案例演示了线程池
"""
import concurrent.futures


def func(tname):
    global word
    for i,v in enumerate(word):
        word[i] = chr(ord(v)^1)
        print(f"{tname}:{word}\n",end="")
    return word

if __name__ == '__main__':
    word=list("idmmn!vnse")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(func,"线程1")
        executor.submit(func,"线程2")
        executor.submit(func,"线程3")
    print("".join(word))
